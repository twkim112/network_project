# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sample_df.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fsample_df.proto\"\x93\x01\n\tDataFrame\x12\x1f\n\x05index\x18\x01 \x03(\x0b\x32\x10.DataFrame.Index\x12\"\n\x07\x63olumns\x18\x02 \x03(\x0b\x32\x11.DataFrame.Column\x1a\x19\n\x05Index\x12\x10\n\x08\x64\x61tetime\x18\x01 \x01(\t\x1a&\n\x06\x43olumn\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06values\x18\x02 \x03(\x01\"\x07\n\x05\x45mpty2[\n\x10\x44\x61taFrameService\x12\"\n\x0cGetDataFrame\x12\x06.Empty\x1a\n.DataFrame\x12#\n\rSendDataFrame\x12\n.DataFrame\x1a\x06.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sample_df_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DATAFRAME']._serialized_start=20
  _globals['_DATAFRAME']._serialized_end=167
  _globals['_DATAFRAME_INDEX']._serialized_start=102
  _globals['_DATAFRAME_INDEX']._serialized_end=127
  _globals['_DATAFRAME_COLUMN']._serialized_start=129
  _globals['_DATAFRAME_COLUMN']._serialized_end=167
  _globals['_EMPTY']._serialized_start=169
  _globals['_EMPTY']._serialized_end=176
  _globals['_DATAFRAMESERVICE']._serialized_start=178
  _globals['_DATAFRAMESERVICE']._serialized_end=269
# @@protoc_insertion_point(module_scope)