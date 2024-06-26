# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import raft_pb2 as raft__pb2


class RaftStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ElectionRequestVoteRPC = channel.unary_unary(
                '/Raft/ElectionRequestVoteRPC',
                request_serializer=raft__pb2.requestVote.SerializeToString,
                response_deserializer=raft__pb2.requestVoteReply.FromString,
                )
        self.HeartBeatAppendEntriesRPC = channel.unary_unary(
                '/Raft/HeartBeatAppendEntriesRPC',
                request_serializer=raft__pb2.appendEntries.SerializeToString,
                response_deserializer=raft__pb2.appendEntriesReply.FromString,
                )
        self.ServeClient = channel.unary_unary(
                '/Raft/ServeClient',
                request_serializer=raft__pb2.ServeClientArgs.SerializeToString,
                response_deserializer=raft__pb2.ServeClientReply.FromString,
                )


class RaftServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ElectionRequestVoteRPC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HeartBeatAppendEntriesRPC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ServeClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RaftServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ElectionRequestVoteRPC': grpc.unary_unary_rpc_method_handler(
                    servicer.ElectionRequestVoteRPC,
                    request_deserializer=raft__pb2.requestVote.FromString,
                    response_serializer=raft__pb2.requestVoteReply.SerializeToString,
            ),
            'HeartBeatAppendEntriesRPC': grpc.unary_unary_rpc_method_handler(
                    servicer.HeartBeatAppendEntriesRPC,
                    request_deserializer=raft__pb2.appendEntries.FromString,
                    response_serializer=raft__pb2.appendEntriesReply.SerializeToString,
            ),
            'ServeClient': grpc.unary_unary_rpc_method_handler(
                    servicer.ServeClient,
                    request_deserializer=raft__pb2.ServeClientArgs.FromString,
                    response_serializer=raft__pb2.ServeClientReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Raft', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Raft(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ElectionRequestVoteRPC(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Raft/ElectionRequestVoteRPC',
            raft__pb2.requestVote.SerializeToString,
            raft__pb2.requestVoteReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def HeartBeatAppendEntriesRPC(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Raft/HeartBeatAppendEntriesRPC',
            raft__pb2.appendEntries.SerializeToString,
            raft__pb2.appendEntriesReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ServeClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Raft/ServeClient',
            raft__pb2.ServeClientArgs.SerializeToString,
            raft__pb2.ServeClientReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
