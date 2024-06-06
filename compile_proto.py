import grpc_tools.protoc

grpc_tools.protoc.main((
    'grpc_tools.protoc',
    '--proto_path=.',
    '--python_out=.',
    '--grpc_python_out=.',
    './sample_df.proto',
))
