#
# Autogenerated by Thrift Compiler (0.11.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:new_style
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys
import evernote.edam.type.ttypes

from thrift.transport import TTransport
all_structs = []


class EDAMErrorCode(object):
    """
    Numeric codes indicating the type of error that occurred on the
    service.
    <dl>
      <dt>UNKNOWN</dt>
        <dd>No information available about the error</dd>
      <dt>BAD_DATA_FORMAT</dt>
        <dd>The format of the request data was incorrect</dd>
      <dt>PERMISSION_DENIED</dt>
        <dd>Not permitted to perform action</dd>
      <dt>INTERNAL_ERROR</dt>
        <dd>Unexpected problem with the service</dd>
      <dt>DATA_REQUIRED</dt>
        <dd>A required parameter/field was absent</dd>
      <dt>LIMIT_REACHED</dt>
        <dd>Operation denied due to data model limit</dd>
      <dt>QUOTA_REACHED</dt>
        <dd>Operation denied due to user storage limit</dd>
      <dt>INVALID_AUTH</dt>
        <dd>Username and/or password incorrect</dd>
      <dt>AUTH_EXPIRED</dt>
        <dd>Authentication token expired</dd>
      <dt>DATA_CONFLICT</dt>
        <dd>Change denied due to data model conflict</dd>
      <dt>ENML_VALIDATION</dt>
        <dd>Content of submitted note was malformed</dd>
      <dt>SHARD_UNAVAILABLE</dt>
        <dd>Service shard with account data is temporarily down</dd>
      <dt>LEN_TOO_SHORT</dt>
        <dd>Operation denied due to data model limit, where something such
            as a string length was too short</dd>
      <dt>LEN_TOO_LONG</dt>
        <dd>Operation denied due to data model limit, where something such
            as a string length was too long</dd>
      <dt>TOO_FEW</dt>
        <dd>Operation denied due to data model limit, where there were
            too few of something.</dd>
      <dt>TOO_MANY</dt>
        <dd>Operation denied due to data model limit, where there were
            too many of something.</dd>
      <dt>UNSUPPORTED_OPERATION</dt>
        <dd>Operation denied because it is currently unsupported.</dd>
      <dt>TAKEN_DOWN</dt>
        <dd>Operation denied because access to the corresponding object is
            prohibited in response to a take-down notice.</dd>
      <dt>RATE_LIMIT_REACHED</dt>
        <dd>Operation denied because the calling application has reached
            its hourly API call limit for this user.</dd>
      <dt>BUSINESS_SECURITY_LOGIN_REQUIRED</dt>
        <dd>Access to a business account has been denied because the user must complete
           additional steps in order to comply with business security requirements.</dd>
      <dt>DEVICE_LIMIT_REACHED</dt>
        <dd>Operation denied because the user has exceeded their maximum allowed
           number of devices.</dd>
    </dl>
    """
    UNKNOWN = 1
    BAD_DATA_FORMAT = 2
    PERMISSION_DENIED = 3
    INTERNAL_ERROR = 4
    DATA_REQUIRED = 5
    LIMIT_REACHED = 6
    QUOTA_REACHED = 7
    INVALID_AUTH = 8
    AUTH_EXPIRED = 9
    DATA_CONFLICT = 10
    ENML_VALIDATION = 11
    SHARD_UNAVAILABLE = 12
    LEN_TOO_SHORT = 13
    LEN_TOO_LONG = 14
    TOO_FEW = 15
    TOO_MANY = 16
    UNSUPPORTED_OPERATION = 17
    TAKEN_DOWN = 18
    RATE_LIMIT_REACHED = 19
    BUSINESS_SECURITY_LOGIN_REQUIRED = 20
    DEVICE_LIMIT_REACHED = 21

    _VALUES_TO_NAMES = {
        1: "UNKNOWN",
        2: "BAD_DATA_FORMAT",
        3: "PERMISSION_DENIED",
        4: "INTERNAL_ERROR",
        5: "DATA_REQUIRED",
        6: "LIMIT_REACHED",
        7: "QUOTA_REACHED",
        8: "INVALID_AUTH",
        9: "AUTH_EXPIRED",
        10: "DATA_CONFLICT",
        11: "ENML_VALIDATION",
        12: "SHARD_UNAVAILABLE",
        13: "LEN_TOO_SHORT",
        14: "LEN_TOO_LONG",
        15: "TOO_FEW",
        16: "TOO_MANY",
        17: "UNSUPPORTED_OPERATION",
        18: "TAKEN_DOWN",
        19: "RATE_LIMIT_REACHED",
        20: "BUSINESS_SECURITY_LOGIN_REQUIRED",
        21: "DEVICE_LIMIT_REACHED",
    }

    _NAMES_TO_VALUES = {
        "UNKNOWN": 1,
        "BAD_DATA_FORMAT": 2,
        "PERMISSION_DENIED": 3,
        "INTERNAL_ERROR": 4,
        "DATA_REQUIRED": 5,
        "LIMIT_REACHED": 6,
        "QUOTA_REACHED": 7,
        "INVALID_AUTH": 8,
        "AUTH_EXPIRED": 9,
        "DATA_CONFLICT": 10,
        "ENML_VALIDATION": 11,
        "SHARD_UNAVAILABLE": 12,
        "LEN_TOO_SHORT": 13,
        "LEN_TOO_LONG": 14,
        "TOO_FEW": 15,
        "TOO_MANY": 16,
        "UNSUPPORTED_OPERATION": 17,
        "TAKEN_DOWN": 18,
        "RATE_LIMIT_REACHED": 19,
        "BUSINESS_SECURITY_LOGIN_REQUIRED": 20,
        "DEVICE_LIMIT_REACHED": 21,
    }


class EDAMInvalidContactReason(object):
    """
    An enumeration that provides a reason for why a given contact was invalid, for example,
    as thrown via an EDAMInvalidContactsException.

    <dl>
      <dt>BAD_ADDRESS</dt>
        <dd>The contact information does not represent a valid address for a recipient.
            Clients should be validating and normalizing contacts, so receiving this
            error code commonly represents a client error.
            </dd>
      <dt>DUPLICATE_CONTACT</dt>
        <dd>If the method throwing this exception accepts a list of contacts, this error
            code indicates that the given contact is a duplicate of another contact in
            the list.  Note that the server may clean up contacts, and that this cleanup
            occurs before checking for duplication.  Receiving this error is commonly
            an indication of a client issue, since client should be normalizing contacts
            and removing duplicates. All instances that are duplicates are returned.  For
            example, if a list of 5 contacts has the same e-mail address twice, the two
            conflicting e-mail address contacts will be returned.
            </dd>
      <dt>NO_CONNECTION</dt>
        <dd>Indicates that the given contact, an Evernote type contact, is not connected
            to the user for which the call is being made. It is possible that clients are
            out of sync with the server and should re-synchronize their identities and
            business user state. See Identity.userConnected for more information on user
            connections.
            </dd>
    </dl>

    Note that if multiple reasons may apply, only one is returned. The precedence order
    is BAD_ADDRESS, DUPLICATE_CONTACT, NO_CONNECTION, meaning that if a contact has a bad
    address and is also duplicated, it will be returned as a BAD_ADDRESS.
    """
    BAD_ADDRESS = 0
    DUPLICATE_CONTACT = 1
    NO_CONNECTION = 2

    _VALUES_TO_NAMES = {
        0: "BAD_ADDRESS",
        1: "DUPLICATE_CONTACT",
        2: "NO_CONNECTION",
    }

    _NAMES_TO_VALUES = {
        "BAD_ADDRESS": 0,
        "DUPLICATE_CONTACT": 1,
        "NO_CONNECTION": 2,
    }


class EDAMUserException(TException):
    """
    This exception is thrown by EDAM procedures when a call fails as a result of
    a problem that a caller may be able to resolve.  For example, if the user
    attempts to add a note to their account which would exceed their storage
    quota, this type of exception may be thrown to indicate the source of the
    error so that they can choose an alternate action.

    This exception would not be used for internal system errors that do not
    reflect user actions, but rather reflect a problem within the service that
    the user cannot resolve.

    errorCode:  The numeric code indicating the type of error that occurred.
      must be one of the values of EDAMErrorCode.

    parameter:  If the error applied to a particular input parameter, this will
      indicate which parameter.

    Attributes:
     - errorCode
     - parameter
    """


    def __init__(self, errorCode=None, parameter=None,):
        self.errorCode = errorCode
        self.parameter = parameter

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.errorCode = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.parameter = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('EDAMUserException')
        if self.errorCode is not None:
            oprot.writeFieldBegin('errorCode', TType.I32, 1)
            oprot.writeI32(self.errorCode)
            oprot.writeFieldEnd()
        if self.parameter is not None:
            oprot.writeFieldBegin('parameter', TType.STRING, 2)
            oprot.writeString(self.parameter.encode('utf-8') if sys.version_info[0] == 2 else self.parameter)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.errorCode is None:
            raise TProtocolException(message='Required field errorCode is unset!')
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class EDAMSystemException(TException):
    """
    This exception is thrown by EDAM procedures when a call fails as a result of
    a problem in the service that could not be changed through caller action.

    errorCode:  The numeric code indicating the type of error that occurred.
      must be one of the values of EDAMErrorCode.

    message:  This may contain additional information about the error

    rateLimitDuration:  Indicates the minimum number of seconds that an application should
      expect subsequent API calls for this user to fail. The application should not retry
      API requests for the user until at least this many seconds have passed. Present only
      when errorCode is RATE_LIMIT_REACHED,

    Attributes:
     - errorCode
     - message
     - rateLimitDuration
    """


    def __init__(self, errorCode=None, message=None, rateLimitDuration=None,):
        self.errorCode = errorCode
        self.message = message
        self.rateLimitDuration = rateLimitDuration

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.errorCode = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.message = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.rateLimitDuration = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('EDAMSystemException')
        if self.errorCode is not None:
            oprot.writeFieldBegin('errorCode', TType.I32, 1)
            oprot.writeI32(self.errorCode)
            oprot.writeFieldEnd()
        if self.message is not None:
            oprot.writeFieldBegin('message', TType.STRING, 2)
            oprot.writeString(self.message.encode('utf-8') if sys.version_info[0] == 2 else self.message)
            oprot.writeFieldEnd()
        if self.rateLimitDuration is not None:
            oprot.writeFieldBegin('rateLimitDuration', TType.I32, 3)
            oprot.writeI32(self.rateLimitDuration)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.errorCode is None:
            raise TProtocolException(message='Required field errorCode is unset!')
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class EDAMNotFoundException(TException):
    """
    This exception is thrown by EDAM procedures when a caller asks to perform
    an operation on an object that does not exist.  This may be thrown based on an invalid
    primary identifier (e.g. a bad GUID), or when the caller refers to an object
    by another unique identifier (e.g. a User's email address).

    identifier:  A description of the object that was not found on the server.
      For example, "Note.notebookGuid" when a caller attempts to create a note in a
      notebook that does not exist in the user's account.

    key:  The value passed from the client in the identifier, which was not
      found. For example, the GUID that was not found.

    Attributes:
     - identifier
     - key
    """


    def __init__(self, identifier=None, key=None,):
        self.identifier = identifier
        self.key = key

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.identifier = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.key = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('EDAMNotFoundException')
        if self.identifier is not None:
            oprot.writeFieldBegin('identifier', TType.STRING, 1)
            oprot.writeString(self.identifier.encode('utf-8') if sys.version_info[0] == 2 else self.identifier)
            oprot.writeFieldEnd()
        if self.key is not None:
            oprot.writeFieldBegin('key', TType.STRING, 2)
            oprot.writeString(self.key.encode('utf-8') if sys.version_info[0] == 2 else self.key)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class EDAMInvalidContactsException(TException):
    """
    An exception thrown when the provided Contacts fail validation. For instance,
    email domains could be invalid, phone numbers might not be valid for SMS,
    etc.

    We will not provide individual reasons for each Contact's validation failure.
    The presence of the Contact in this exception means that the user must figure
    out how to take appropriate action to fix this Contact.

    <dl>
      <dt>contacts</dt>
      <dd>The list of Contacts that are considered invalid by the service</dd>

      <dt>parameter</dt>
      <dd>If the error applied to a particular input parameter, this will
      indicate which parameter.</dd>

      <dt>reasons</dt>
      <dd>If supplied, the list of reasons why the server considered a contact invalid,
      matching, in order, the list returned in the contacts field.</dd>
    </dl>

    Attributes:
     - contacts
     - parameter
     - reasons
    """


    def __init__(self, contacts=None, parameter=None, reasons=None,):
        self.contacts = contacts
        self.parameter = parameter
        self.reasons = reasons

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.LIST:
                    self.contacts = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = evernote.edam.type.ttypes.Contact()
                        _elem5.read(iprot)
                        self.contacts.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.parameter = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.LIST:
                    self.reasons = []
                    (_etype9, _size6) = iprot.readListBegin()
                    for _i10 in range(_size6):
                        _elem11 = iprot.readI32()
                        self.reasons.append(_elem11)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('EDAMInvalidContactsException')
        if self.contacts is not None:
            oprot.writeFieldBegin('contacts', TType.LIST, 1)
            oprot.writeListBegin(TType.STRUCT, len(self.contacts))
            for iter12 in self.contacts:
                iter12.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.parameter is not None:
            oprot.writeFieldBegin('parameter', TType.STRING, 2)
            oprot.writeString(self.parameter.encode('utf-8') if sys.version_info[0] == 2 else self.parameter)
            oprot.writeFieldEnd()
        if self.reasons is not None:
            oprot.writeFieldBegin('reasons', TType.LIST, 3)
            oprot.writeListBegin(TType.I32, len(self.reasons))
            for iter13 in self.reasons:
                oprot.writeI32(iter13)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.contacts is None:
            raise TProtocolException(message='Required field contacts is unset!')
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(EDAMUserException)
EDAMUserException.thrift_spec = (
    None,  # 0
    (1, TType.I32, 'errorCode', None, None, ),  # 1
    (2, TType.STRING, 'parameter', 'UTF8', None, ),  # 2
)
all_structs.append(EDAMSystemException)
EDAMSystemException.thrift_spec = (
    None,  # 0
    (1, TType.I32, 'errorCode', None, None, ),  # 1
    (2, TType.STRING, 'message', 'UTF8', None, ),  # 2
    (3, TType.I32, 'rateLimitDuration', None, None, ),  # 3
)
all_structs.append(EDAMNotFoundException)
EDAMNotFoundException.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'identifier', 'UTF8', None, ),  # 1
    (2, TType.STRING, 'key', 'UTF8', None, ),  # 2
)
all_structs.append(EDAMInvalidContactsException)
EDAMInvalidContactsException.thrift_spec = (
    None,  # 0
    (1, TType.LIST, 'contacts', (TType.STRUCT, [evernote.edam.type.ttypes.Contact, None], False), None, ),  # 1
    (2, TType.STRING, 'parameter', 'UTF8', None, ),  # 2
    (3, TType.LIST, 'reasons', (TType.I32, None, False), None, ),  # 3
)
fix_spec(all_structs)
del all_structs
