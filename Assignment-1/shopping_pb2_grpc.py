# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import shopping_pb2 as shopping__pb2


class MarketPlaceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterSeller = channel.unary_unary(
                '/MarketPlace/RegisterSeller',
                request_serializer=shopping__pb2.SellerInfo.SerializeToString,
                response_deserializer=shopping__pb2.stringReply.FromString,
                )
        self.SellItem = channel.unary_unary(
                '/MarketPlace/SellItem',
                request_serializer=shopping__pb2.Item.SerializeToString,
                response_deserializer=shopping__pb2.stringReply.FromString,
                )
        self.UpdateItem = channel.unary_unary(
                '/MarketPlace/UpdateItem',
                request_serializer=shopping__pb2.ItemUpdate.SerializeToString,
                response_deserializer=shopping__pb2.stringReply.FromString,
                )
        self.DeleteItem = channel.unary_unary(
                '/MarketPlace/DeleteItem',
                request_serializer=shopping__pb2.ItemDelete.SerializeToString,
                response_deserializer=shopping__pb2.stringReply.FromString,
                )
        self.DisplaySellerItems = channel.unary_unary(
                '/MarketPlace/DisplaySellerItems',
                request_serializer=shopping__pb2.SellerInfo.SerializeToString,
                response_deserializer=shopping__pb2.ItemList.FromString,
                )
        self.SearchItem = channel.unary_stream(
                '/MarketPlace/SearchItem',
                request_serializer=shopping__pb2.Item.SerializeToString,
                response_deserializer=shopping__pb2.Item.FromString,
                )
        self.BuyItem = channel.unary_unary(
                '/MarketPlace/BuyItem',
                request_serializer=shopping__pb2.BuyRequest.SerializeToString,
                response_deserializer=shopping__pb2.stringReply.FromString,
                )
        self.AddToWishList = channel.unary_unary(
                '/MarketPlace/AddToWishList',
                request_serializer=shopping__pb2.WishListRequest.SerializeToString,
                response_deserializer=shopping__pb2.stringReply.FromString,
                )
        self.RateItem = channel.unary_unary(
                '/MarketPlace/RateItem',
                request_serializer=shopping__pb2.RateRequest.SerializeToString,
                response_deserializer=shopping__pb2.stringReply.FromString,
                )


class MarketPlaceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RegisterSeller(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SellItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DisplaySellerItems(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BuyItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddToWishList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RateItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MarketPlaceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterSeller': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterSeller,
                    request_deserializer=shopping__pb2.SellerInfo.FromString,
                    response_serializer=shopping__pb2.stringReply.SerializeToString,
            ),
            'SellItem': grpc.unary_unary_rpc_method_handler(
                    servicer.SellItem,
                    request_deserializer=shopping__pb2.Item.FromString,
                    response_serializer=shopping__pb2.stringReply.SerializeToString,
            ),
            'UpdateItem': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateItem,
                    request_deserializer=shopping__pb2.ItemUpdate.FromString,
                    response_serializer=shopping__pb2.stringReply.SerializeToString,
            ),
            'DeleteItem': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteItem,
                    request_deserializer=shopping__pb2.ItemDelete.FromString,
                    response_serializer=shopping__pb2.stringReply.SerializeToString,
            ),
            'DisplaySellerItems': grpc.unary_unary_rpc_method_handler(
                    servicer.DisplaySellerItems,
                    request_deserializer=shopping__pb2.SellerInfo.FromString,
                    response_serializer=shopping__pb2.ItemList.SerializeToString,
            ),
            'SearchItem': grpc.unary_stream_rpc_method_handler(
                    servicer.SearchItem,
                    request_deserializer=shopping__pb2.Item.FromString,
                    response_serializer=shopping__pb2.Item.SerializeToString,
            ),
            'BuyItem': grpc.unary_unary_rpc_method_handler(
                    servicer.BuyItem,
                    request_deserializer=shopping__pb2.BuyRequest.FromString,
                    response_serializer=shopping__pb2.stringReply.SerializeToString,
            ),
            'AddToWishList': grpc.unary_unary_rpc_method_handler(
                    servicer.AddToWishList,
                    request_deserializer=shopping__pb2.WishListRequest.FromString,
                    response_serializer=shopping__pb2.stringReply.SerializeToString,
            ),
            'RateItem': grpc.unary_unary_rpc_method_handler(
                    servicer.RateItem,
                    request_deserializer=shopping__pb2.RateRequest.FromString,
                    response_serializer=shopping__pb2.stringReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'MarketPlace', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MarketPlace(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RegisterSeller(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MarketPlace/RegisterSeller',
            shopping__pb2.SellerInfo.SerializeToString,
            shopping__pb2.stringReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SellItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MarketPlace/SellItem',
            shopping__pb2.Item.SerializeToString,
            shopping__pb2.stringReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MarketPlace/UpdateItem',
            shopping__pb2.ItemUpdate.SerializeToString,
            shopping__pb2.stringReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MarketPlace/DeleteItem',
            shopping__pb2.ItemDelete.SerializeToString,
            shopping__pb2.stringReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DisplaySellerItems(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MarketPlace/DisplaySellerItems',
            shopping__pb2.SellerInfo.SerializeToString,
            shopping__pb2.ItemList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SearchItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/MarketPlace/SearchItem',
            shopping__pb2.Item.SerializeToString,
            shopping__pb2.Item.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BuyItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MarketPlace/BuyItem',
            shopping__pb2.BuyRequest.SerializeToString,
            shopping__pb2.stringReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddToWishList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MarketPlace/AddToWishList',
            shopping__pb2.WishListRequest.SerializeToString,
            shopping__pb2.stringReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RateItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MarketPlace/RateItem',
            shopping__pb2.RateRequest.SerializeToString,
            shopping__pb2.stringReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
