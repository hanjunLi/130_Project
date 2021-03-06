# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import rpc_interface_pb2 as rpc__interface__pb2


class ParsePDFStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetFeature = channel.unary_unary(
        '/ParsePDF/GetFeature',
        request_serializer=rpc__interface__pb2.Chunk.SerializeToString,
        response_deserializer=rpc__interface__pb2.jsonStr.FromString,
        )


class ParsePDFServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetFeature(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ParsePDFServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetFeature': grpc.unary_unary_rpc_method_handler(
          servicer.GetFeature,
          request_deserializer=rpc__interface__pb2.Chunk.FromString,
          response_serializer=rpc__interface__pb2.jsonStr.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ParsePDF', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
