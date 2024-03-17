import grpc
from concurrent import futures
import raft_pb2
import raft_pb2_grpc
import time
import random
import server_info
import threading

ID=0

FOLLOWER = 0
CANDIDATE = 1
LEADER = 2
STATE = -1


class RaftServicer(raft_pb2_grpc.RaftServicer):
    def __init__(self):
        self.id = ID
        self.current_term = 0
        self.voted_for = -1
        self.log = []
        # self.commit_length = 0
        self.current_role = FOLLOWER
        self.current_leader = -1
        self.votes_received = []
        # self.sent_length = 0
        # self.ack_length = 0

    def send_information(self):
        stubs = []
        for i in range(len(server_info.available_servers)):
            if(i == self.id):
                continue
            channel = grpc.insecure_channel(server_info.available_servers[i])
            stub = stubs.append(raft_pb2_grpc.RaftStub(channel))

        while(True):
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
                    reponse = stub.HeartBeatAppendEntriesRPC(heart_beat_message)
                    print(reponse)

            elif(self.current_role == CANDIDATE):
                request_vote_message = raft_pb2.requestVote(
                    term = self.current_term,
                    cid = self.id,
                    lastLogIndex = -1,
                    lastLogTerm = -1
                )
                for stub in stubs:
                    reponse = stub.ElectionRequestVoteRPC(request_vote_message)
                    print(reponse)
            time.sleep(0.01)
    
    def ElectionRequestVoteRPC(self, request, context):
        print("follower here")
        print(request.cid)
        return raft_pb2.requestVoteReply(term = 10000, voteGranted = True)
    
    def HeartBeatAppendEntriesRPC(self, request, context):
        return raft_pb2.appendEntriesReply()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_servicer_object = RaftServicer()
    raft_pb2_grpc.add_RaftServicer_to_server(raft_servicer_object, server)
    server.add_insecure_port('[::]:50051')

    send_info_thread = threading.Thread(target=raft_servicer_object.send_information)
    send_info_thread.start()

    server.start()
    print("Server started. Listening on port 50052")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Received Ctrl+C. Shutting down the server gracefully...")
        send_info_thread.join()
        server.stop(None)

if __name__ == '__main__':
    serve()
