# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import kmeans_pb2 as kmeans__pb2


class KMeansStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Map = channel.unary_unary(
                '/KMeans/Map',
                request_serializer=kmeans__pb2.mapInfo.SerializeToString,
                response_deserializer=kmeans__pb2.reply.FromString,
                )
        self.Reduce = channel.unary_unary(
                '/KMeans/Reduce',
                request_serializer=kmeans__pb2.reduceInfo.SerializeToString,
                response_deserializer=kmeans__pb2.keyValDict.FromString,
                )
        self.GetPartition = channel.unary_unary(
                '/KMeans/GetPartition',
                request_serializer=kmeans__pb2.reduceInfo.SerializeToString,
                response_deserializer=kmeans__pb2.keyValDict.FromString,
                )


class KMeansServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Map(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Reduce(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPartition(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KMeansServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Map': grpc.unary_unary_rpc_method_handler(
                    servicer.Map,
                    request_deserializer=kmeans__pb2.mapInfo.FromString,
                    response_serializer=kmeans__pb2.reply.SerializeToString,
            ),
            'Reduce': grpc.unary_unary_rpc_method_handler(
                    servicer.Reduce,
                    request_deserializer=kmeans__pb2.reduceInfo.FromString,
                    response_serializer=kmeans__pb2.keyValDict.SerializeToString,
            ),
            'GetPartition': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPartition,
                    request_deserializer=kmeans__pb2.reduceInfo.FromString,
                    response_serializer=kmeans__pb2.keyValDict.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'KMeans', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class KMeans(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Map(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KMeans/Map',
            kmeans__pb2.mapInfo.SerializeToString,
            kmeans__pb2.reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Reduce(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KMeans/Reduce',
            kmeans__pb2.reduceInfo.SerializeToString,
            kmeans__pb2.keyValDict.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPartition(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KMeans/GetPartition',
            kmeans__pb2.reduceInfo.SerializeToString,
            kmeans__pb2.keyValDict.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)