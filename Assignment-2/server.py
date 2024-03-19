import grpc
from concurrent import futures
import raft_pb2
import raft_pb2_grpc
import time
import random
import server_info
import threading
import counter

server_id = -1

FOLLOWER = 0
CANDIDATE = 1
LEADER = 2

shutdown = False

dataset = {}

class RaftServicer(raft_pb2_grpc.RaftServicer):
    def __init__(self):
        global server_id
        print("ID:", server_id)
        self.id = server_id
        self.current_term = 0
        self.voted_for = -1
        self.log = []
        self.commit_length = 0
        self.current_role = FOLLOWER
        self.current_leader = -1
        self.votes_received = []
        self.sent_length = {}
        self.ack_length = {}
        self.stubs = []
        self.stub_id = []
        self.log_index = 0
        self.file_write_index = 0
        self.log_file = "logfile" + str(self.id) + ".txt"
        with open("filename.txt", "w") as file:
            file.write("Log File\n")
        self.time_out = random.randint(5, 10)
        print("TIME_OUT", self.time_out)
        self.start_time = time.time()

    def send_information(self):
        for i in range(len(server_info.available_servers)):
            if(i == self.id):
                continue
            channel = grpc.insecure_channel(server_info.available_servers[i])
            self.stubs.append(raft_pb2_grpc.RaftStub(channel))
            self.stub_id.append(i)

        global shutdown
        while(not shutdown):
            if(self.current_role == LEADER):
                print("===================LEADER=====================")
                print("TERM:", self.current_term)
                heart_beat_message = raft_pb2.appendEntries(
                    term = self.current_term,
                    leaderId = self.current_leader,
                    leaderCommitIndex = self.commit_length,
                    entries = self.log
                )
                for i in range(server_info.N - 1):
                    stub = self.stubs[i]
                    try:
                        reponse = stub.HeartBeatAppendEntriesRPC(heart_beat_message)
                        print(reponse)
                    except grpc.RpcError as e:
                        print("LEADER: Node down, heartbeat not sent:", self.stub_id[i])
                        print(e)
                        print()
                        continue

            elif(self.current_role == CANDIDATE):
                print("===================CANDIDATE=====================")
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
                        print("CANDIDATE: Vote requested from", self.stub_id[i])
                        reponse = stub.ElectionRequestVoteRPC(request_vote_message)
                    except grpc.RpcError as e:
                        print("CANDIDATE: Node down, vote request not sent:", self.stub_id[i])
                        print(e)
                        continue
                    
                    if(reponse.term == self.current_term and reponse.voteGranted):
                        print("CANDIDATE: Vote Granted from", reponse.id)
                        self.votes_received.append(reponse.id)
                        if(len(self.votes_received) > (server_info.N / 2)):
                                print("CANDIDATE: Majority votes received")
                                self.current_leader = self.id
                                self.current_role = LEADER
                                self.voted_for = -1
                                self.votes_received = []
                                print("CANDIDATE: Elected as Leader")
                
                                for i in range(server_info.N - 1):
                                    print("CANDIDATE: Sent leader ack to", self.stub_id[i])
                                    stub = self.stubs[i]

                                    self.sent_length[self.stub_id[i]] = len(self.log)
                                    self.ack_length[self.stub_id[i]] = 0
                                    try:
                                        reponse = stub.HeartBeatAppendEntriesRPC(raft_pb2.appendEntries(leaderId = self.id))
                                    except grpc.RpcError as e:
                                        print("CANDIDATE: Node down, vote request not sent:", self.stub_id[i])
                                        print(e)
                                        continue
                                break
                    elif( reponse.term > self.current_term ):
                        self.current_term = reponse.term
                        self.current_role = FOLLOWER
                        self.voted_for = -1
                        self.votes_received = []
                        print("CANDIDATE: Stepping Down to Follower")
                    print(reponse)
            else:
                print("===================FOLLOWER=====================")
                if((time.time() - self.start_time) >= self.time_out):
                    self.current_role = CANDIDATE
            with open(self.log_file, "a") as file:
                while(self.file_write_index < len(self.log)):
                    item = self.log[self.file_write_index]
                    file.write(str(item) + "\n")  
                    self.file_write_index+=1
            time.sleep(0.001)

    def ElectionRequestVoteRPC(self, request, context):
        print("FOLLOWER: Vote Request")
        print(request)
        if(self.current_term < request.term):
            print("FOLLOWER: Vote Granted")
            self.current_term = request.term
            self.current_role = FOLLOWER
            self.voted_for = -1
        last_term = 0
        if(len(self.log) > 0):
            last_term = self.log[-1]
        logOk = (request.lastLogTerm > last_term) or (request.lastLogTerm == last_term and request.lastLogIndex >= len(self.log))
        if(request.term == self.current_term and logOk and (self.voted_for == request.cid or self.voted_for == -1)):
            self.voted_for = request.cid
            return raft_pb2.requestVoteReply(term = self.current_term, voteGranted = True, id = self.id)
        else:
            print("FOLLOWER: Vote Denied")
            return raft_pb2.requestVoteReply(term = self.current_term, voteGranted = False, id = self.id)
    
    def HeartBeatAppendEntriesRPC(self, request, context):
        print("FOLLOWER: HeartBeat from leader")
        self.start_time = time.time()
        self.current_leader = request.leaderId
        self.current_term = request.term
        if(request.entries != []):
            self.log = request.entries #implement later appending logs instead of copying

        while(request.leaderCommitIndex > self.commit_length):
            print("FOLLOWER: Log Fast Forward")
            print("FOLLOWER: INDEX:", self.log_index)
            print("FOLLOWER: To commit operation:", self.log[self.log_index].operation)
            print("FOLLOWER: Leader CommitIndex", request.leaderCommitIndex, self.commit_length, self.log_index)
            if(self.log[self.log_index].operation == "SET"):
                global dataset
                print("FOLLOWER: To commit operation varName:", self.log[self.log_index].varName)
                print("FOLLOWER: To commit operation varValue:", self.log[self.log_index].varValue)
                dataset[self.log[self.log_index].varName] = self.log[self.log_index].varValue
                self.commit_length+=1
            self.log_index += 1
            print("FOLLOWER: Leader CommitIndex", request.leaderCommitIndex, self.commit_length, self.log_index)
        print(request)
        return raft_pb2.appendEntriesReply(term = self.current_term, success = True)
    
    def ServeClient(self, request, context):
        if(self.current_leader != self.id):
            print("FOLLOWER: CLIENT REQUEST")
            return raft_pb2.ServeClientReply(LeaderID = self.current_leader, Success = False)
        else:
            print("LEADER: CLIENT REQUEST")
            req = request.Request.split()
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
                        print("LEADER: Node down, append entries was not:", self.stub_id[i])
                        print(e)
                        continue
                    majority += 1
                    print("MAJORITY", majority)
                    self.ack_length[self.stub_id[i]] = len(self.log)
                if(majority > server_info.N/2):
                    dataset[req[1]] = req[2]
                    self.commit_length += 1
                    return raft_pb2.ServeClientReply(Data = req[2], LeaderID = self.current_leader, Success = True)
                else:
                    return raft_pb2.ServeClientReply(Data = "LEADER: Could not append to majority nodes.", LeaderID = self.current_leader, Success = False)
            else:
                if(req[1] not in dataset):
                    return raft_pb2.ServeClientReply(Data="Value not found", LeaderID = self.current_leader, Success = False)
                self.log.append(raft_pb2.log(operation=req[0], varName=req[1], varValue=dataset[req[1]], term=self.current_term))
                return raft_pb2.ServeClientReply(Data = dataset[req[1]], LeaderID = self.current_leader, Success = True)

def serve():
    global server_id 
    server_id = 2
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_servicer_object = RaftServicer()
    raft_pb2_grpc.add_RaftServicer_to_server(raft_servicer_object, server)
    server.add_insecure_port(server_info.port_number[server_id])

    send_info_thread = threading.Thread(target=raft_servicer_object.send_information)
    send_info_thread.start()

    server.start()
    print("Server started. Listening on port", server_info.port_number[server_id])

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Received Ctrl+C. Shutting down the server gracefully...")
        global shutdown
        shutdown = True
        send_info_thread.join()
        server.stop(None)

if __name__ == '__main__':
    serve()
