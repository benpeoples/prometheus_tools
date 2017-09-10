# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: time.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import nanopb_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='time.proto',
  package='',
  serialized_pb=_b('\n\ntime.proto\x1a\x0cnanopb.proto\"\xd7\x02\n\x0bTimeTrigger\x12\x12\n\ntrigger_id\x18\x01 \x02(\r\x12\x12\n\nstart_date\x18\x02 \x01(\x07\x12\x10\n\x08\x65nd_date\x18\x03 \x01(\x07\x12\x13\n\x0b\x64\x61y_of_week\x18\x04 \x01(\x05\x12*\n\nstart_type\x18\x05 \x01(\x0e\x32\x16.TimeTrigger.time_type\x12\r\n\x05start\x18\x06 \x01(\x05\x12(\n\x08\x65nd_type\x18\x07 \x01(\x0e\x32\x16.TimeTrigger.time_type\x12\x0b\n\x03\x65nd\x18\x08 \x01(\x05\x12\x10\n\x08priority\x18\n \x01(\r\x12\x15\n\x06\x61\x63tion\x18\x14 \x01(\tB\x05\x92?\x02\x08x\"^\n\ttime_type\x12\x08\n\x04TIME\x10\x00\x12\x0b\n\x07SUNRISE\x10\x01\x12\n\n\x06SUNSET\x10\x02\x12\x08\n\x04NOON\x10\x03\x12\x0c\n\x08MIDNIGHT\x10\x04\x12\n\n\x06RANDOM\x10\x05\x12\n\n\x06MANUAL\x10\x06')
  ,
  dependencies=[nanopb_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_TIMETRIGGER_TIME_TYPE = _descriptor.EnumDescriptor(
  name='time_type',
  full_name='TimeTrigger.time_type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TIME', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUNRISE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUNSET', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NOON', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MIDNIGHT', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RANDOM', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MANUAL', index=6, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=278,
  serialized_end=372,
)
_sym_db.RegisterEnumDescriptor(_TIMETRIGGER_TIME_TYPE)


_TIMETRIGGER = _descriptor.Descriptor(
  name='TimeTrigger',
  full_name='TimeTrigger',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trigger_id', full_name='TimeTrigger.trigger_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='start_date', full_name='TimeTrigger.start_date', index=1,
      number=2, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end_date', full_name='TimeTrigger.end_date', index=2,
      number=3, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='day_of_week', full_name='TimeTrigger.day_of_week', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='start_type', full_name='TimeTrigger.start_type', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='start', full_name='TimeTrigger.start', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end_type', full_name='TimeTrigger.end_type', index=6,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end', full_name='TimeTrigger.end', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='priority', full_name='TimeTrigger.priority', index=8,
      number=10, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='action', full_name='TimeTrigger.action', index=9,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\222?\002\010x'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TIMETRIGGER_TIME_TYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=29,
  serialized_end=372,
)

_TIMETRIGGER.fields_by_name['start_type'].enum_type = _TIMETRIGGER_TIME_TYPE
_TIMETRIGGER.fields_by_name['end_type'].enum_type = _TIMETRIGGER_TIME_TYPE
_TIMETRIGGER_TIME_TYPE.containing_type = _TIMETRIGGER
DESCRIPTOR.message_types_by_name['TimeTrigger'] = _TIMETRIGGER

TimeTrigger = _reflection.GeneratedProtocolMessageType('TimeTrigger', (_message.Message,), dict(
  DESCRIPTOR = _TIMETRIGGER,
  __module__ = 'time_pb2'
  # @@protoc_insertion_point(class_scope:TimeTrigger)
  ))
_sym_db.RegisterMessage(TimeTrigger)


_TIMETRIGGER.fields_by_name['action'].has_options = True
_TIMETRIGGER.fields_by_name['action']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\222?\002\010x'))
# @@protoc_insertion_point(module_scope)
