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
        # self.commit_length = 0
        self.current_role = FOLLOWER
        self.current_leader = -1
        self.votes_received = []
        # self.sent_length = 0
        # self.ack_length = 0
        self.time_out = random.randint(5, 10)
        print("TIME_OUT", self.time_out)
        self.start_time = time.time()

    def send_information(self):
        stubs = []
        for i in range(len(server_info.available_servers)):
            if(i == self.id):
                continue
            channel = grpc.insecure_channel(server_info.available_servers[i])
            stub = stubs.append(raft_pb2_grpc.RaftStub(channel))

        global shutdown
        while(not shutdown):
            if(self.current_role == LEADER):
                heart_beat_message = raft_pb2.appendEntries(
                    term = self.current_term,
                    leaderId = self.current_leader,
                    prevLogIndex = -1,
                    prevLogTerm = -1,
                    entries = self.log,
                    leaderCommitIndex = -1
                )
                for stub in stubs:
                    try:
                        reponse = stub.HeartBeatAppendEntriesRPC(heart_beat_message)
                        print(reponse)
                    except grpc.RpcError as e:
                        print("LEADER: Node down, heartbeat not sent.")
                        print(e)
                        print()
                        continue

            elif(self.current_role == CANDIDATE):
                #slide 112 to do
                self.current_term += 1
                self.voted_for = self.id
                self.votes_received.append(self.id)

                request_vote_message = raft_pb2.requestVote(
                    term = self.current_term,
                    cid = self.id,
                    lastLogIndex = -1,
                    lastLogTerm = -1
                )
                for stub in stubs:
                    try:
                        reponse = stub.ElectionRequestVoteRPC(request_vote_message)
                    except grpc.RpcError as e:
                        print("CANDIDATE: Node down, vote request not sent.")
                        print(e)
                        continue

                    if( reponse.term > self.current_term ):
                        self.current_term = reponse.term
                        self.current_role = FOLLOWER
                        print("CANDIDATE: Stepping Down to Follower")

                    else:
                        if(reponse.voteGranted and (reponse.id not in self.votes_received)):
                            self.votes_received.append(reponse.id)
                            print("CANDIDATE: vote received from", reponse.id)
                        if(len(self.votes_received) > (server_info.N / 2)):
                            self.current_leader = self.id
                            self.current_role = LEADER
                            print("CANDIDATE: Elected as Leader")
                            break
                     
                    print(reponse)
            else:
                if((time.time() - self.start_time) >= self.time_out):
                    self.current_role = CANDIDATE
            time.sleep(0.001)

    def ElectionRequestVoteRPC(self, request, context):
        print("FOLLOWER: Vote Request")
        print(request)
        if(self.current_term < request.term):
            print("FOLLOWER: Vote Granted")
            self.current_term = request.term
            return raft_pb2.requestVoteReply(term = self.current_term, voteGranted = True, id = self.id)
        else:
            print("FOLLOWER: Vote Denied")
            return raft_pb2.requestVoteReply(term = self.current_term, voteGranted = False, id = self.id)
    
    def HeartBeatAppendEntriesRPC(self, request, context):
        self.start_time = time.time()
        self.current_leader = request.leaderId
        self.current_term = request.term
        print("FOLLOWER: HeartBeat from leader")
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
                dataset[req[1]] = req[2]
                return raft_pb2.ServeClientReply(Data = req[2], LeaderID = self.current_leader, Success = True)
            else:
                return raft_pb2.ServeClientReply(Data = dataset[req[1]], LeaderID = self.current_leader, Success = True)

def serve():
    global server_id 
    server_id = counter.get_next_id()
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