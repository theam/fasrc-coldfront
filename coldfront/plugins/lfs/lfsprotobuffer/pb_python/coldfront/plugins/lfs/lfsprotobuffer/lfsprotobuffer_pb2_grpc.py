# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from coldfront.plugins.lfs.lfsprotobuffer import lfsprotobuffer_pb2 as coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2


class GroupsStub(object):
    """The Groups service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetGroupById = channel.unary_unary(
                '/myprotobuffer.Groups/GetGroupById',
                request_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupRequestById.SerializeToString,
                response_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupResp.FromString,
                )
        self.GetGroupByName = channel.unary_unary(
                '/myprotobuffer.Groups/GetGroupByName',
                request_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupRequestByName.SerializeToString,
                response_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupResp.FromString,
                )
        self.ListGroups = channel.unary_stream(
                '/myprotobuffer.Groups/ListGroups',
                request_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.voidNoParam.SerializeToString,
                response_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupResp.FromString,
                )


class GroupsServicer(object):
    """The Groups service definition.
    """

    def GetGroupById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGroupByName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListGroups(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GroupsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetGroupById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetGroupById,
                    request_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupRequestById.FromString,
                    response_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupResp.SerializeToString,
            ),
            'GetGroupByName': grpc.unary_unary_rpc_method_handler(
                    servicer.GetGroupByName,
                    request_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupRequestByName.FromString,
                    response_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupResp.SerializeToString,
            ),
            'ListGroups': grpc.unary_stream_rpc_method_handler(
                    servicer.ListGroups,
                    request_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.voidNoParam.FromString,
                    response_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupResp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'myprotobuffer.Groups', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Groups(object):
    """The Groups service definition.
    """

    @staticmethod
    def GetGroupById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/myprotobuffer.Groups/GetGroupById',
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupRequestById.SerializeToString,
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetGroupByName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/myprotobuffer.Groups/GetGroupByName',
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupRequestByName.SerializeToString,
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListGroups(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/myprotobuffer.Groups/ListGroups',
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.voidNoParam.SerializeToString,
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.GroupResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class FilesystemsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetFilesystemById = channel.unary_unary(
                '/myprotobuffer.Filesystems/GetFilesystemById',
                request_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemRequestById.SerializeToString,
                response_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemResp.FromString,
                )
        self.GetFilesystemByName = channel.unary_unary(
                '/myprotobuffer.Filesystems/GetFilesystemByName',
                request_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemRequestByName.SerializeToString,
                response_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemResp.FromString,
                )
        self.ListFilesystems = channel.unary_stream(
                '/myprotobuffer.Filesystems/ListFilesystems',
                request_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.voidNoParam.SerializeToString,
                response_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemResp.FromString,
                )


class FilesystemsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetFilesystemById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFilesystemByName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListFilesystems(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FilesystemsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetFilesystemById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFilesystemById,
                    request_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemRequestById.FromString,
                    response_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemResp.SerializeToString,
            ),
            'GetFilesystemByName': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFilesystemByName,
                    request_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemRequestByName.FromString,
                    response_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemResp.SerializeToString,
            ),
            'ListFilesystems': grpc.unary_stream_rpc_method_handler(
                    servicer.ListFilesystems,
                    request_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.voidNoParam.FromString,
                    response_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemResp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'myprotobuffer.Filesystems', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Filesystems(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetFilesystemById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/myprotobuffer.Filesystems/GetFilesystemById',
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemRequestById.SerializeToString,
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFilesystemByName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/myprotobuffer.Filesystems/GetFilesystemByName',
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemRequestByName.SerializeToString,
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListFilesystems(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/myprotobuffer.Filesystems/ListFilesystems',
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.voidNoParam.SerializeToString,
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.FilesystemResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class QuotasStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetQuotas = channel.unary_stream(
                '/myprotobuffer.Quotas/GetQuotas',
                request_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaRequest.SerializeToString,
                response_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaResp.FromString,
                )
        self.GetQuotaById = channel.unary_unary(
                '/myprotobuffer.Quotas/GetQuotaById',
                request_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaRequestById.SerializeToString,
                response_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaResp.FromString,
                )
        self.GetQuotasByDate = channel.unary_stream(
                '/myprotobuffer.Quotas/GetQuotasByDate',
                request_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaRequestByDate.SerializeToString,
                response_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaResp.FromString,
                )
        self.ListQuotas = channel.unary_stream(
                '/myprotobuffer.Quotas/ListQuotas',
                request_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.voidNoParam.SerializeToString,
                response_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaResp.FromString,
                )


class QuotasServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetQuotas(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetQuotaById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetQuotasByDate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListQuotas(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QuotasServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetQuotas': grpc.unary_stream_rpc_method_handler(
                    servicer.GetQuotas,
                    request_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaRequest.FromString,
                    response_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaResp.SerializeToString,
            ),
            'GetQuotaById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetQuotaById,
                    request_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaRequestById.FromString,
                    response_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaResp.SerializeToString,
            ),
            'GetQuotasByDate': grpc.unary_stream_rpc_method_handler(
                    servicer.GetQuotasByDate,
                    request_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaRequestByDate.FromString,
                    response_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaResp.SerializeToString,
            ),
            'ListQuotas': grpc.unary_stream_rpc_method_handler(
                    servicer.ListQuotas,
                    request_deserializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.voidNoParam.FromString,
                    response_serializer=coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaResp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'myprotobuffer.Quotas', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Quotas(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetQuotas(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/myprotobuffer.Quotas/GetQuotas',
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaRequest.SerializeToString,
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetQuotaById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/myprotobuffer.Quotas/GetQuotaById',
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaRequestById.SerializeToString,
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetQuotasByDate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/myprotobuffer.Quotas/GetQuotasByDate',
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaRequestByDate.SerializeToString,
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListQuotas(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/myprotobuffer.Quotas/ListQuotas',
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.voidNoParam.SerializeToString,
            coldfront_dot_plugins_dot_lfs_dot_lfsprotobuffer_dot_lfsprotobuffer__pb2.QuotaResp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
