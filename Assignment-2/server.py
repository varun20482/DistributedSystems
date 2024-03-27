import grpc
from concurrent import futures
import raft_pb2
import raft_pb2_grpc
import time
import random
import server_info
import threading
import counter
import os
import sys
import pickle

# Save the reference to the original stdout
original_stdout = sys.stdout
folder = ""
server_id = -1

FOLLOWER = 0
CANDIDATE = 1
LEADER = 2

LEASE_TIMER = 10

shutdown = False

dataset = {}

class RaftServicer(raft_pb2_grpc.RaftServicer):
    def __init__(self):
        global server_id
        print("ID:", server_id, flush=True)
        global folder
        self.folder_name = folder
        self.id = server_id
        self.voted_for = -1
        self.log = []

        if os.path.exists(self.folder_name + '/log.pkl'):
            with open(self.folder_name + '/log.pkl', 'rb') as f:
                self.log = pickle.load(f)

        self.current_term = 0
        if(len(self.log) != 0):
            self.current_term = self.log[-1].term

        self.commit_length = 0
        for log in self.log:
            if(log.operation == "SET"):
                self.commit_length += 1

        self.current_role = FOLLOWER
        self.current_leader = -1
        self.votes_received = []
        self.sent_length = {}
        self.ack_length = {}
        self.stubs = []
        self.stub_id = []
        self.log_index = 0
        self.file_write_index = 0
        self.lease_start_time = 0
        self.lease_of_leader = -1
        self.log_file = self.folder_name + "/logfile.txt"
        self.metadata_file = self.folder_name + "/metadata.txt"
        with open(self.log_file, "w") as file:
            file.write("Log File\n")
        with open(self.metadata_file, "w") as file:
            file.write("Meta Data File\n")
        self.time_out = random.randint(5, 10)
        print("TIME_OUT", self.time_out, flush=True)
        self.start_time = time.time()

    def send_information(self):
        time.sleep(60)
        self.start_time = time.time()
        for i in range(len(server_info.available_servers)):
            if(i == self.id):
                continue
            channel = grpc.insecure_channel(server_info.available_servers[i])
            self.stubs.append(raft_pb2_grpc.RaftStub(channel))
            self.stub_id.append(i)

        global shutdown
        while(not shutdown):
            if(self.current_role == LEADER):
                print("===================LEADER=====================", flush=True)
                print("Leader:", self.id, "sending renewal and heartbeat.", flush=True)
                heart_beat_message = raft_pb2.appendEntries(
                    term = self.current_term,
                    leaderId = self.current_leader,
                    leaderCommitIndex = self.commit_length,
                    entries = []
                )
                if(self.lease_of_leader == -1):
                    self.lease_of_leader = self.id
                    self.lease_start_time = time.time()
                    print("LEADER: ID:", self.id, "old leader lease expired. New lease started.", flush=True)
                else:
                    if(self.lease_of_leader != self.id):
                        print("LEADER: ID:", self.id, "waiting for old leader lease to time out.", flush=True)
                renewed = False
                majority = 1
                for i in range(server_info.N - 1):
                    stub = self.stubs[i]
                    try:
                        reponse = stub.HeartBeatAppendEntriesRPC(heart_beat_message)
                        majority += 1
                        print("Heart Beat sent to node:", self.stub_id[i], flush=True)
                        print("Heart beat response from:", self.stub_id[i], flush=True)
                        print("Term of node:", self.stub_id[i], "is", reponse.term, flush=True)
                        print("Heart Beat Success:", reponse.success, flush=True)
                        print(flush=True)
                    except grpc.RpcError as e:
                        print("LEADER: Node down, heartbeat not sent:", self.stub_id[i], flush=True)
                        # print(e)
                        print(flush=True)
                        continue

                    if(not renewed and majority > server_info.N / 2 and self.lease_of_leader == self.id):
                        renewed = True
                        self.lease_start_time = time.time()
                        print("LEADER: ID:", self.id, "renewing lease.", flush=True)

            elif(self.current_role == CANDIDATE):
                print("===================CANDIDATE=====================", flush=True)
                self.current_term += 1
                self.voted_for = self.id
                self.votes_received.append(self.id)
                last_term = 0
                if(len(self.log) > 0):
                    last_term = self.log[-1].term
                request_vote_message = raft_pb2.requestVote(
                    term = self.current_term,
                    cid = self.id,
                    lastLogIndex = len(self.log),
                    lastLogTerm = last_term
                )
                for i in range(server_info.N - 1):
                    stub = self.stubs[i]
                    try:
                        print("CANDIDATE: Vote requested from", self.stub_id[i], flush=True)
                        reponse = stub.ElectionRequestVoteRPC(request_vote_message)
                    except grpc.RpcError as e:
                        print("CANDIDATE: Node down, vote request not sent:", self.stub_id[i], flush=True)
                        # print(e)
                        continue
                    highest_timer = max(self.lease_start_time, reponse.leaderLeaseStartTime)
                    if(reponse.term == self.current_term and reponse.voteGranted):
                        print("CANDIDATE: Vote Granted from", reponse.id, flush=True)
                        self.votes_received.append(reponse.id)
                        if(len(self.votes_received) > (server_info.N / 2)):
                                print("CANDIDATE: Majority votes received", flush=True)
                                self.lease_start_time = highest_timer
                                self.current_leader = self.id
                                self.current_role = LEADER
                                self.voted_for = -1
                                self.votes_received = []
                                print("CANDIDATE: Elected as Leader", flush=True)
                                print("Node:", self.id, "elected as leader for Term:", self.current_term, flush=True)
                                self.log.append(raft_pb2.log(operation = "NO-OP", term = self.current_term))

                                for i in range(server_info.N - 1):
                                    print("CANDIDATE: Sent leader ack to", self.stub_id[i], flush=True)
                                    stub = self.stubs[i]
                                    self.sent_length[self.stub_id[i]] = len(self.log)
                                    self.ack_length[self.stub_id[i]] = 0
                                    try:
                                        reponse = stub.HeartBeatAppendEntriesRPC(
                                            raft_pb2.appendEntries(term = self.current_term,
                                            leaderId = self.id,
                                            prevLogIndex = len(self.log),
                                            prevLogTerm = self.current_term,
                                            entries = self.log,
                                            leaderCommitIndex = self.commit_length)
                                            )
                                    except grpc.RpcError as e:
                                        print("CANDIDATE: Node down, vote request not sent:", self.stub_id[i], flush=True)
                                        # print(e)
                                        continue
                                break
                    elif( reponse.term > self.current_term ):
                        self.current_term = reponse.term
                        index = 0
                        while index < len(reponse.entries):
                            if index >= len(self.log):
                                break  
                            if reponse.entries[index].term == self.log[index].term:
                                index += 1
                            else:
                                break
                        self.log = self.log[:index] + reponse.entries[index:]
                        self.current_role = FOLLOWER
                        self.start_time = time.time()
                        self.voted_for = -1
                        self.votes_received = []
                        print("CANDIDATE: Stepping Down to Follower", flush=True)
                        break
                    print(reponse, flush=True)
                if(self.current_role == CANDIDATE):
                    self.current_role = FOLLOWER
                    self.start_time = time.time()
                    self.voted_for = -1
                    self.votes_received = []
            else:
                print("===================FOLLOWER IN TIMEOUT=====================", flush=True)
                if((time.time() - self.start_time) >= self.time_out):
                    print("Node ID:", self.id, "Election Timer Timed out. Starting Election.", flush=True)
                    self.current_role = CANDIDATE
            with open(self.log_file, "a") as file:
                while(self.file_write_index < len(self.log)):
                    item = self.log[self.file_write_index]
                    file.write(str(item) + "\n")  
                    self.file_write_index+=1
            if(self.lease_of_leader != -1):
                if(time.time() - self.lease_start_time >= LEASE_TIMER):
                    if(self.current_role == LEADER):
                        print("LEADER: ID:", self.id," Lease renewal FAILED. Stepping Down.", flush=True)
                        self.current_role = FOLLOWER
                        self.start_time = time.time()
                    self.lease_of_leader = -1
            time.sleep(1)

    def ElectionRequestVoteRPC(self, request, context):
        print("FOLLOWER: Vote Request", flush=True)
        if(self.current_term < request.term):
            print("FOLLOWER: Vote Granted to node", request.cid, "for term:", request.term, flush=True)
            if(self.current_role == LEADER):
                print("LEADER: ID:", self.id, "Stepping down to follower.", flush=True)
            self.current_term = request.term
            self.current_role = FOLLOWER
            self.start_time = time.time()
            self.voted_for = -1
        last_term = 0
        if(len(self.log) > 0):
            last_term = self.log[-1].term
        logOk = (request.lastLogTerm > last_term) or (request.lastLogTerm == last_term and request.lastLogIndex >= len(self.log))
        if(request.term == self.current_term and logOk and (self.voted_for == -1)):
            self.voted_for = request.cid
            return raft_pb2.requestVoteReply(term = self.current_term, voteGranted = True, id = self.id, leaderLeaseStartTime = self.lease_start_time)
        else:
            print("FOLLOWER: Vote Denied to node", request.cid, "for term:", request.term, flush=True)
            return raft_pb2.requestVoteReply(term = self.current_term, voteGranted = False, id = self.id, entries = self.log, leaderLeaseStartTime = self.lease_start_time)
    
    def HeartBeatAppendEntriesRPC(self, request, context):
        print("FOLLOWER: HeartBeat from leader id:", request.leaderId, flush=True)
        self.start_time = time.time()
        self.current_leader = request.leaderId
        self.lease_start_time = time.time()
        self.lease_of_leader = request.leaderId
        if(self.current_term < request.term):
            self.current_term = request.term
            self.current_role = FOLLOWER
            self.start_time = time.time()
        self.current_term = request.term
        if(len(request.entries) > len(self.log)):
            print("FOLLOWER: ID:", self.id, "accepted append entries RPC from ", request.leaderId, flush=True)
            index = 0
            while index < len(request.entries):
                if index >= len(self.log):
                    break  
                if request.entries[index].term == self.log[index].term:
                    index += 1
                else:
                    break
            self.log = self.log[:index] + request.entries[index:]

        elif(len(request.entries) < len(self.log) and request.entries != []):
            print("FOLLOWER: ID:", self.id, "rejected append entries RPC from ", request.leaderId, flush=True)

        while(request.leaderCommitIndex > self.commit_length):
            print("FOLLOWER: Log Fast Forward", flush=True)
            print("FOLLOWER: Node ID:", self.id, flush=True)
            print("FOLLOWER: INDEX:", self.log_index, flush=True)
            print("FOLLOWER: To commit operation:", self.log[self.log_index].operation, flush=True)
            print("FOLLOWER: Leader CommitIndex", request.leaderCommitIndex, self.commit_length, self.log_index, flush=True)
            if(self.log[self.log_index].operation == "SET"):
                global dataset
                print("FOLLOWER: To commit operation varName:", self.log[self.log_index].varName, flush=True)
                print("FOLLOWER: To commit operation varValue:", self.log[self.log_index].varValue, flush=True)
                dataset[self.log[self.log_index].varName] = self.log[self.log_index].varValue
                self.commit_length+=1
                with open(self.metadata_file, "a") as file:
                    file.write(f"FOLLOWER: ID: {self.id} TERM: {self.current_term}\n")
                    file.write(f"FOLLOWER: To commit operation varName: {self.log[self.log_index].varName}\n")
                    file.write(f"FOLLOWER: To commit operation varValue: {self.log[self.log_index].varValue}\n")
                    file.write(f"FOLLOWER: Commit length: {self.commit_length}\n")
                    file.write(f"FOLLOWER: Commit Time: {time.time()}\n")

            self.log_index += 1
            print("FOLLOWER: Leader CommitIndex", request.leaderCommitIndex, self.commit_length, self.log_index, flush=True)
        return raft_pb2.appendEntriesReply(term = self.current_term, success = True)
    
    def ServeClient(self, request, context):
        if(self.current_leader != self.id):
            print("FOLLOWER: CLIENT REQUEST", flush=True)
            return raft_pb2.ServeClientReply(Data = "FOLLOWER: Operations can be perfomed only by the leader.", LeaderID = self.current_leader, Success = False)
        else:
            print("LEADER: CLIENT REQUEST", flush=True)
            if(self.lease_of_leader != self.id):
                return raft_pb2.ServeClientReply(Data = "LEADER: The old leader lease has not timed out.", LeaderID = self.current_leader, Success = False)
            req = request.Request.split()
            print("LEADER: ID:", self.id, "received a", request.Request, "request", flush=True)
            if( req[0] == "SET" ):
                self.log.append(raft_pb2.log(operation=req[0], varName=req[1], varValue=req[2], term=self.current_term))
                heart_beat_message = raft_pb2.appendEntries(
                    term = self.current_term,
                    leaderId = self.current_leader,
                    prevLogIndex = len(self.log),
                    prevLogTerm = self.current_term,
                    entries = self.log,
                    leaderCommitIndex = self.commit_length
                )
                majority = 1
                for i in range(server_info.N - 1):
                    stub = self.stubs[i]
                    self.sent_length[self.stub_id[i]] = len(self.log)
                    try:
                        reponse = stub.HeartBeatAppendEntriesRPC(heart_beat_message)
                    except grpc.RpcError as e:
                        print("LEADER: Node down, append entries was not:", self.stub_id[i], flush=True)
                        # print(e)
                        continue
                    majority += 1
                    print("MAJORITY", majority, flush=True)
                    self.ack_length[self.stub_id[i]] = len(self.log)
                if(majority > server_info.N/2):
                    print("LEADER: ID:", self.id, "commited the entry", request.Request, "to the state machine.", flush=True)
                    dataset[req[1]] = req[2]
                    self.commit_length += 1
                    with open(self.metadata_file, "a") as file:
                        file.write(f"LEADER: ID: {self.id} TERM: {self.current_term}\n")
                        file.write(f"LEADER: To commit operation varName: {req[1]}\n")
                        file.write(f"LEADER: To commit operation varValue: {req[2]}\n")
                        file.write(f"LEADER: Commit length: {self.commit_length}\n")
                        file.write(f"LEADER: Commit Time: {time.time()}\n")

                    return raft_pb2.ServeClientReply(Data = req[2], LeaderID = self.current_leader, Success = True)
                else:
                    return raft_pb2.ServeClientReply(Data = "LEADER: Could not append to majority nodes.", LeaderID = self.current_leader, Success = False)
            else:
                if(req[1] not in dataset):
                    return raft_pb2.ServeClientReply(Data="Value not found", LeaderID = self.current_leader, Success = False)
                # self.log.append(raft_pb2.log(operation=req[0], varName=req[1], varValue=dataset[req[1]], term=self.current_term))
                return raft_pb2.ServeClientReply(Data = dataset[req[1]], LeaderID = self.current_leader, Success = True)

def serve():
    global server_id 
    server_id = counter.get_next_id()
    global folder
    folder = "node_" + str(server_id)
    os.makedirs(folder, exist_ok=True)
    
    if os.path.exists(folder + '/database.pkl'):
        with open(folder + '/database.pkl', 'rb') as f:
            global dataset
            dataset = pickle.load(f)

    with open(folder + "/dump.txt", 'w') as f:
        sys.stdout = f
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        raft_servicer_object = RaftServicer()
        raft_pb2_grpc.add_RaftServicer_to_server(raft_servicer_object, server)
        server.add_insecure_port(server_info.port_number[server_id])

        send_info_thread = threading.Thread(target=raft_servicer_object.send_information)
        send_info_thread.start()

        server.start()
        print("Server started. Listening on port", server_info.port_number[server_id], flush=True)

        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            print("Received Ctrl+C. Shutting down the server gracefully...", flush=True)
            global shutdown
            shutdown = True
            send_info_thread.join()
            server.stop(None)
            with open(raft_servicer_object.folder_name + '/log.pkl', 'wb') as f:
                pickle.dump(raft_servicer_object.log, f)
            with open(raft_servicer_object.folder_name + '/database.pkl', 'wb') as f:
                pickle.dump(dataset, f)
        sys.stdout = original_stdout

if __name__ == '__main__':
    serve()
