# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: raft.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nraft.proto\"S\n\x0brequestVote\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0b\n\x03\x63id\x18\x02 \x01(\x05\x12\x14\n\x0clastLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0blastLogTerm\x18\x04 \x01(\x05\"v\n\x10requestVoteReply\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x13\n\x0bvoteGranted\x18\x02 \x01(\x08\x12\n\n\x02id\x18\x03 \x01(\x05\x12\x15\n\x07\x65ntries\x18\x04 \x03(\x0b\x32\x04.log\x12\x1c\n\x14leaderLeaseStartTime\x18\x05 \x01(\x02\"I\n\x03log\x12\x11\n\toperation\x18\x01 \x01(\t\x12\x0f\n\x07varName\x18\x02 \x01(\t\x12\x10\n\x08varValue\x18\x03 \x01(\t\x12\x0c\n\x04term\x18\x04 \x01(\x05\"\x8c\x01\n\rappendEntries\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x10\n\x08leaderId\x18\x02 \x01(\x05\x12\x14\n\x0cprevLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0bprevLogTerm\x18\x04 \x01(\x05\x12\x15\n\x07\x65ntries\x18\x05 \x03(\x0b\x32\x04.log\x12\x19\n\x11leaderCommitIndex\x18\x06 \x01(\x05\"3\n\x12\x61ppendEntriesReply\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x08\"\"\n\x0fServeClientArgs\x12\x0f\n\x07Request\x18\x01 \x01(\t\"C\n\x10ServeClientReply\x12\x0c\n\x04\x44\x61ta\x18\x01 \x01(\t\x12\x10\n\x08LeaderID\x18\x02 \x01(\x05\x12\x0f\n\x07Success\x18\x03 \x01(\x08\x32\xbd\x01\n\x04Raft\x12;\n\x16\x45lectionRequestVoteRPC\x12\x0c.requestVote\x1a\x11.requestVoteReply\"\x00\x12\x42\n\x19HeartBeatAppendEntriesRPC\x12\x0e.appendEntries\x1a\x13.appendEntriesReply\"\x00\x12\x34\n\x0bServeClient\x12\x10.ServeClientArgs\x1a\x11.ServeClientReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'raft_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REQUESTVOTE']._serialized_start=14
  _globals['_REQUESTVOTE']._serialized_end=97
  _globals['_REQUESTVOTEREPLY']._serialized_start=99
  _globals['_REQUESTVOTEREPLY']._serialized_end=217
  _globals['_LOG']._serialized_start=219
  _globals['_LOG']._serialized_end=292
  _globals['_APPENDENTRIES']._serialized_start=295
  _globals['_APPENDENTRIES']._serialized_end=435
  _globals['_APPENDENTRIESREPLY']._serialized_start=437
  _globals['_APPENDENTRIESREPLY']._serialized_end=488
  _globals['_SERVECLIENTARGS']._serialized_start=490
  _globals['_SERVECLIENTARGS']._serialized_end=524
  _globals['_SERVECLIENTREPLY']._serialized_start=526
  _globals['_SERVECLIENTREPLY']._serialized_end=593
  _globals['_RAFT']._serialized_start=596
  _globals['_RAFT']._serialized_end=785
# @@protoc_insertion_point(module_scope)
