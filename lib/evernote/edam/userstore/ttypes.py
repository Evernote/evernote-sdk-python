#
# Autogenerated by Thrift Compiler
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:new_style
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
import evernote.edam.type.ttypes
import evernote.edam.error.ttypes


from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class PublicUserInfo(object):
  """
   This structure is used to provide publicly-available user information
   about a particular account.
  <dl>
   <dt>userId:</dt>
     <dd>
     The unique numeric user identifier for the user account.
     </dd>
   <dt>shardId:</dt>
     <dd>
     DEPRECATED - Client applications should have no need to use this field.
     </dd>
   <dt>privilege:</dt>
     <dd>
     The privilege level of the account, to determine whether
     this is a Premium or Free account.
     </dd>
   <dt>noteStoreUrl:</dt>
     <dd>
     This field will contain the full URL that clients should use to make
     NoteStore requests to the server shard that contains that user's data.
     I.e. this is the URL that should be used to create the Thrift HTTP client
     transport to send messages to the NoteStore service for the account.
     </dd>
   <dt>webApiUrlPrefix:</dt>
     <dd>
     This field will contain the initial part of the URLs that should be used
     to make requests to Evernote's thin client "web API", which provide
     optimized operations for clients that aren't capable of manipulating
     the full contents of accounts via the full Thrift data model. Clients
     should concatenate the relative path for the various servlets onto the
     end of this string to construct the full URL, as documented on our
     developer web site.
     </dd>
   </dl>
  
  Attributes:
   - userId
   - shardId
   - privilege
   - username
   - noteStoreUrl
   - webApiUrlPrefix
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'userId', None, None, ), # 1
    (2, TType.STRING, 'shardId', None, None, ), # 2
    (3, TType.I32, 'privilege', None, None, ), # 3
    (4, TType.STRING, 'username', None, None, ), # 4
    (5, TType.STRING, 'noteStoreUrl', None, None, ), # 5
    (6, TType.STRING, 'webApiUrlPrefix', None, None, ), # 6
  )

  def __init__(self, userId=None, shardId=None, privilege=None, username=None, noteStoreUrl=None, webApiUrlPrefix=None,):
    self.userId = userId
    self.shardId = shardId
    self.privilege = privilege
    self.username = username
    self.noteStoreUrl = noteStoreUrl
    self.webApiUrlPrefix = webApiUrlPrefix

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.userId = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.shardId = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.privilege = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.username = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.STRING:
          self.noteStoreUrl = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.STRING:
          self.webApiUrlPrefix = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('PublicUserInfo')
    if self.userId is not None:
      oprot.writeFieldBegin('userId', TType.I32, 1)
      oprot.writeI32(self.userId)
      oprot.writeFieldEnd()
    if self.shardId is not None:
      oprot.writeFieldBegin('shardId', TType.STRING, 2)
      oprot.writeString(self.shardId)
      oprot.writeFieldEnd()
    if self.privilege is not None:
      oprot.writeFieldBegin('privilege', TType.I32, 3)
      oprot.writeI32(self.privilege)
      oprot.writeFieldEnd()
    if self.username is not None:
      oprot.writeFieldBegin('username', TType.STRING, 4)
      oprot.writeString(self.username)
      oprot.writeFieldEnd()
    if self.noteStoreUrl is not None:
      oprot.writeFieldBegin('noteStoreUrl', TType.STRING, 5)
      oprot.writeString(self.noteStoreUrl)
      oprot.writeFieldEnd()
    if self.webApiUrlPrefix is not None:
      oprot.writeFieldBegin('webApiUrlPrefix', TType.STRING, 6)
      oprot.writeString(self.webApiUrlPrefix)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    if self.userId is None:
      raise TProtocol.TProtocolException(message='Required field userId is unset!')
    if self.shardId is None:
      raise TProtocol.TProtocolException(message='Required field shardId is unset!')
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.items()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class AuthenticationResult(object):
  """
   When an authentication (or re-authentication) is performed, this structure
   provides the result to the client.
  <dl>
   <dt>currentTime:</dt>
     <dd>
     The server-side date and time when this result was
     generated.
     </dd>
   <dt>authenticationToken:</dt>
     <dd>
     Holds an opaque, ASCII-encoded token that can be
     used by the client to perform actions on a NoteStore.
     </dd>
   <dt>expiration:</dt>
     <dd>
     Holds the server-side date and time when the
     authentication token will expire.
     This time can be compared to "currentTime" to produce an expiration
     time that can be reconciled with the client's local clock.
     </dd>
   <dt>user:</dt>
     <dd>
     Holds the information about the account which was
     authenticated if this was a full authentication.  May be absent if this
     particular authentication did not require user information.
     </dd>
   <dt>publicUserInfo:</dt>
     <dd>
     If this authentication result was achieved without full permissions to
     access the full User structure, this field may be set to give back
     a more limited public set of data.
     </dd>
   <dt>noteStoreUrl:</dt>
     <dd>
     This field will contain the full URL that clients should use to make
     NoteStore requests to the server shard that contains that user's data.
     I.e. this is the URL that should be used to create the Thrift HTTP client
     transport to send messages to the NoteStore service for the account.
     </dd>
   <dt>webApiUrlPrefix:</dt>
     <dd>
     This field will contain the initial part of the URLs that should be used
     to make requests to Evernote's thin client "web API", which provide
     optimized operations for clients that aren't capable of manipulating
     the full contents of accounts via the full Thrift data model. Clients
     should concatenate the relative path for the various servlets onto the
     end of this string to construct the full URL, as documented on our
     developer web site.
     </dd>
   <dt>secondFactorRequired:</dt>
     <dd>
     If set to true, this field indicates that the user has enabled two-factor
     authentication and must enter their second factor in order to complete
     authentication. In this case the value of authenticationResult will be
     a short-lived authentication token that may only be used to make a
     subsequent call to completeTwoFactorAuthentication.
     </dd>
   <dt>secondFactorDeliveryHint:</dt>
     <dd>
     When secondFactorRequired is set to true, this field may contain a string
     describing the second factor delivery method that the user has configured.
     This will typically be an obfuscated mobile device number, such as
     "(xxx) xxx-x095". This string can be displayed to the user to remind them
     how to obtain the required second factor.
     TODO do we need to differentiate between SMS and voice delivery?
     </dd>
   </dl>
  
  Attributes:
   - currentTime
   - authenticationToken
   - expiration
   - user
   - publicUserInfo
   - noteStoreUrl
   - webApiUrlPrefix
   - secondFactorRequired
   - secondFactorDeliveryHint
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'currentTime', None, None, ), # 1
    (2, TType.STRING, 'authenticationToken', None, None, ), # 2
    (3, TType.I64, 'expiration', None, None, ), # 3
    (4, TType.STRUCT, 'user', (evernote.edam.type.ttypes.User, evernote.edam.type.ttypes.User.thrift_spec), None, ), # 4
    (5, TType.STRUCT, 'publicUserInfo', (PublicUserInfo, PublicUserInfo.thrift_spec), None, ), # 5
    (6, TType.STRING, 'noteStoreUrl', None, None, ), # 6
    (7, TType.STRING, 'webApiUrlPrefix', None, None, ), # 7
    (8, TType.BOOL, 'secondFactorRequired', None, None, ), # 8
    (9, TType.STRING, 'secondFactorDeliveryHint', None, None, ), # 9
  )

  def __init__(self, currentTime=None, authenticationToken=None, expiration=None, user=None, publicUserInfo=None, noteStoreUrl=None, webApiUrlPrefix=None, secondFactorRequired=None, secondFactorDeliveryHint=None,):
    self.currentTime = currentTime
    self.authenticationToken = authenticationToken
    self.expiration = expiration
    self.user = user
    self.publicUserInfo = publicUserInfo
    self.noteStoreUrl = noteStoreUrl
    self.webApiUrlPrefix = webApiUrlPrefix
    self.secondFactorRequired = secondFactorRequired
    self.secondFactorDeliveryHint = secondFactorDeliveryHint

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.currentTime = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.authenticationToken = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I64:
          self.expiration = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRUCT:
          self.user = evernote.edam.type.ttypes.User()
          self.user.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.STRUCT:
          self.publicUserInfo = PublicUserInfo()
          self.publicUserInfo.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.STRING:
          self.noteStoreUrl = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.STRING:
          self.webApiUrlPrefix = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.BOOL:
          self.secondFactorRequired = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 9:
        if ftype == TType.STRING:
          self.secondFactorDeliveryHint = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('AuthenticationResult')
    if self.currentTime is not None:
      oprot.writeFieldBegin('currentTime', TType.I64, 1)
      oprot.writeI64(self.currentTime)
      oprot.writeFieldEnd()
    if self.authenticationToken is not None:
      oprot.writeFieldBegin('authenticationToken', TType.STRING, 2)
      oprot.writeString(self.authenticationToken)
      oprot.writeFieldEnd()
    if self.expiration is not None:
      oprot.writeFieldBegin('expiration', TType.I64, 3)
      oprot.writeI64(self.expiration)
      oprot.writeFieldEnd()
    if self.user is not None:
      oprot.writeFieldBegin('user', TType.STRUCT, 4)
      self.user.write(oprot)
      oprot.writeFieldEnd()
    if self.publicUserInfo is not None:
      oprot.writeFieldBegin('publicUserInfo', TType.STRUCT, 5)
      self.publicUserInfo.write(oprot)
      oprot.writeFieldEnd()
    if self.noteStoreUrl is not None:
      oprot.writeFieldBegin('noteStoreUrl', TType.STRING, 6)
      oprot.writeString(self.noteStoreUrl)
      oprot.writeFieldEnd()
    if self.webApiUrlPrefix is not None:
      oprot.writeFieldBegin('webApiUrlPrefix', TType.STRING, 7)
      oprot.writeString(self.webApiUrlPrefix)
      oprot.writeFieldEnd()
    if self.secondFactorRequired is not None:
      oprot.writeFieldBegin('secondFactorRequired', TType.BOOL, 8)
      oprot.writeBool(self.secondFactorRequired)
      oprot.writeFieldEnd()
    if self.secondFactorDeliveryHint is not None:
      oprot.writeFieldBegin('secondFactorDeliveryHint', TType.STRING, 9)
      oprot.writeString(self.secondFactorDeliveryHint)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    if self.currentTime is None:
      raise TProtocol.TProtocolException(message='Required field currentTime is unset!')
    if self.authenticationToken is None:
      raise TProtocol.TProtocolException(message='Required field authenticationToken is unset!')
    if self.expiration is None:
      raise TProtocol.TProtocolException(message='Required field expiration is unset!')
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.items()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class BootstrapSettings(object):
  """
   This structure describes a collection of bootstrap settings.
  <dl>
   <dt>serviceHost:</dt>
     <dd>
     The hostname and optional port for composing Evernote web service URLs.
     This URL can be used to access the UserStore and related services,
     but must not be used to compose the NoteStore URL. Client applications
     must handle serviceHost values that include only the hostname
     (e.g. www.evernote.com) or both the hostname and port (e.g. www.evernote.com:8080).
     If no port is specified, or if port 443 is specified, client applications must
     use the scheme "https" when composing URLs. Otherwise, a client must use the
     scheme "http".
   </dd>
   <dt>marketingUrl:</dt>
     <dd>
     The URL stem for the Evernote corporate marketing website, e.g. http://www.evernote.com.
     This stem can be used to compose website URLs. For example, the URL of the Evernote
     Trunk is composed by appending "/about/trunk/" to the value of marketingUrl.
     </dd>
   <dt>supportUrl:</dt>
     <dd>
     The full URL for the Evernote customer support website, e.g. https://support.evernote.com.
     </dd>
   <dt>accountEmailDomain:</dt>
     <dd>
     The domain used for an Evernote user's incoming email address, which allows notes to
     be emailed into an account. E.g. m.evernote.com.
     </dd>
   <dt>enableFacebookSharing:</dt>
     <dd>
     Whether the client application should enable sharing of notes on Facebook.
     </dd>
   <dt>enableGiftSubscriptions:</dt>
     <dd>
     Whether the client application should enable gift subscriptions.
     </dd>
   <dt>enableSupportTickets:</dt>
     <dd>
     Whether the client application should enable in-client creation of support tickets.
     </dd>
   <dt>enableSharedNotebooks:</dt>
     <dd>
     Whether the client application should enable shared notebooks.
     </dd>
   <dt>enableSingleNoteSharing:</dt>
     <dd>
     Whether the client application should enable single note sharing.
     </dd>
   <dt>enableSponsoredAccounts:</dt>
     <dd>
     Whether the client application should enable sponsored accounts.
     </dd>
   <dt>enableTwitterSharing:</dt>
     <dd>
     Whether the client application should enable sharing of notes on Twitter.
     </dd>
   </dl>
  
  Attributes:
   - serviceHost
   - marketingUrl
   - supportUrl
   - accountEmailDomain
   - enableFacebookSharing
   - enableGiftSubscriptions
   - enableSupportTickets
   - enableSharedNotebooks
   - enableSingleNoteSharing
   - enableSponsoredAccounts
   - enableTwitterSharing
   - enableLinkedInSharing
   - enablePublicNotebooks
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'serviceHost', None, None, ), # 1
    (2, TType.STRING, 'marketingUrl', None, None, ), # 2
    (3, TType.STRING, 'supportUrl', None, None, ), # 3
    (4, TType.STRING, 'accountEmailDomain', None, None, ), # 4
    (5, TType.BOOL, 'enableFacebookSharing', None, None, ), # 5
    (6, TType.BOOL, 'enableGiftSubscriptions', None, None, ), # 6
    (7, TType.BOOL, 'enableSupportTickets', None, None, ), # 7
    (8, TType.BOOL, 'enableSharedNotebooks', None, None, ), # 8
    (9, TType.BOOL, 'enableSingleNoteSharing', None, None, ), # 9
    (10, TType.BOOL, 'enableSponsoredAccounts', None, None, ), # 10
    (11, TType.BOOL, 'enableTwitterSharing', None, None, ), # 11
    (12, TType.BOOL, 'enableLinkedInSharing', None, None, ), # 12
    (13, TType.BOOL, 'enablePublicNotebooks', None, None, ), # 13
  )

  def __init__(self, serviceHost=None, marketingUrl=None, supportUrl=None, accountEmailDomain=None, enableFacebookSharing=None, enableGiftSubscriptions=None, enableSupportTickets=None, enableSharedNotebooks=None, enableSingleNoteSharing=None, enableSponsoredAccounts=None, enableTwitterSharing=None, enableLinkedInSharing=None, enablePublicNotebooks=None,):
    self.serviceHost = serviceHost
    self.marketingUrl = marketingUrl
    self.supportUrl = supportUrl
    self.accountEmailDomain = accountEmailDomain
    self.enableFacebookSharing = enableFacebookSharing
    self.enableGiftSubscriptions = enableGiftSubscriptions
    self.enableSupportTickets = enableSupportTickets
    self.enableSharedNotebooks = enableSharedNotebooks
    self.enableSingleNoteSharing = enableSingleNoteSharing
    self.enableSponsoredAccounts = enableSponsoredAccounts
    self.enableTwitterSharing = enableTwitterSharing
    self.enableLinkedInSharing = enableLinkedInSharing
    self.enablePublicNotebooks = enablePublicNotebooks

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.serviceHost = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.marketingUrl = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.supportUrl = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.accountEmailDomain = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.BOOL:
          self.enableFacebookSharing = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.BOOL:
          self.enableGiftSubscriptions = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.BOOL:
          self.enableSupportTickets = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.BOOL:
          self.enableSharedNotebooks = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 9:
        if ftype == TType.BOOL:
          self.enableSingleNoteSharing = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 10:
        if ftype == TType.BOOL:
          self.enableSponsoredAccounts = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 11:
        if ftype == TType.BOOL:
          self.enableTwitterSharing = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 12:
        if ftype == TType.BOOL:
          self.enableLinkedInSharing = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 13:
        if ftype == TType.BOOL:
          self.enablePublicNotebooks = iprot.readBool();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('BootstrapSettings')
    if self.serviceHost is not None:
      oprot.writeFieldBegin('serviceHost', TType.STRING, 1)
      oprot.writeString(self.serviceHost)
      oprot.writeFieldEnd()
    if self.marketingUrl is not None:
      oprot.writeFieldBegin('marketingUrl', TType.STRING, 2)
      oprot.writeString(self.marketingUrl)
      oprot.writeFieldEnd()
    if self.supportUrl is not None:
      oprot.writeFieldBegin('supportUrl', TType.STRING, 3)
      oprot.writeString(self.supportUrl)
      oprot.writeFieldEnd()
    if self.accountEmailDomain is not None:
      oprot.writeFieldBegin('accountEmailDomain', TType.STRING, 4)
      oprot.writeString(self.accountEmailDomain)
      oprot.writeFieldEnd()
    if self.enableFacebookSharing is not None:
      oprot.writeFieldBegin('enableFacebookSharing', TType.BOOL, 5)
      oprot.writeBool(self.enableFacebookSharing)
      oprot.writeFieldEnd()
    if self.enableGiftSubscriptions is not None:
      oprot.writeFieldBegin('enableGiftSubscriptions', TType.BOOL, 6)
      oprot.writeBool(self.enableGiftSubscriptions)
      oprot.writeFieldEnd()
    if self.enableSupportTickets is not None:
      oprot.writeFieldBegin('enableSupportTickets', TType.BOOL, 7)
      oprot.writeBool(self.enableSupportTickets)
      oprot.writeFieldEnd()
    if self.enableSharedNotebooks is not None:
      oprot.writeFieldBegin('enableSharedNotebooks', TType.BOOL, 8)
      oprot.writeBool(self.enableSharedNotebooks)
      oprot.writeFieldEnd()
    if self.enableSingleNoteSharing is not None:
      oprot.writeFieldBegin('enableSingleNoteSharing', TType.BOOL, 9)
      oprot.writeBool(self.enableSingleNoteSharing)
      oprot.writeFieldEnd()
    if self.enableSponsoredAccounts is not None:
      oprot.writeFieldBegin('enableSponsoredAccounts', TType.BOOL, 10)
      oprot.writeBool(self.enableSponsoredAccounts)
      oprot.writeFieldEnd()
    if self.enableTwitterSharing is not None:
      oprot.writeFieldBegin('enableTwitterSharing', TType.BOOL, 11)
      oprot.writeBool(self.enableTwitterSharing)
      oprot.writeFieldEnd()
    if self.enableLinkedInSharing is not None:
      oprot.writeFieldBegin('enableLinkedInSharing', TType.BOOL, 12)
      oprot.writeBool(self.enableLinkedInSharing)
      oprot.writeFieldEnd()
    if self.enablePublicNotebooks is not None:
      oprot.writeFieldBegin('enablePublicNotebooks', TType.BOOL, 13)
      oprot.writeBool(self.enablePublicNotebooks)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    if self.serviceHost is None:
      raise TProtocol.TProtocolException(message='Required field serviceHost is unset!')
    if self.marketingUrl is None:
      raise TProtocol.TProtocolException(message='Required field marketingUrl is unset!')
    if self.supportUrl is None:
      raise TProtocol.TProtocolException(message='Required field supportUrl is unset!')
    if self.accountEmailDomain is None:
      raise TProtocol.TProtocolException(message='Required field accountEmailDomain is unset!')
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.items()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class BootstrapProfile(object):
  """
   This structure describes a collection of bootstrap settings.
  <dl>
   <dt>name:</dt>
     <dd>
     The unique name of the profile, which is guaranteed to remain consistent across
     calls to getBootstrapInfo.
     </dd>
   <dt>settings:</dt>
     <dd>
     The settings for this profile.
     </dd>
   </dl>
  
  Attributes:
   - name
   - settings
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'name', None, None, ), # 1
    (2, TType.STRUCT, 'settings', (BootstrapSettings, BootstrapSettings.thrift_spec), None, ), # 2
  )

  def __init__(self, name=None, settings=None,):
    self.name = name
    self.settings = settings

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.name = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRUCT:
          self.settings = BootstrapSettings()
          self.settings.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('BootstrapProfile')
    if self.name is not None:
      oprot.writeFieldBegin('name', TType.STRING, 1)
      oprot.writeString(self.name)
      oprot.writeFieldEnd()
    if self.settings is not None:
      oprot.writeFieldBegin('settings', TType.STRUCT, 2)
      self.settings.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    if self.name is None:
      raise TProtocol.TProtocolException(message='Required field name is unset!')
    if self.settings is None:
      raise TProtocol.TProtocolException(message='Required field settings is unset!')
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.items()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class BootstrapInfo(object):
  """
   This structure describes a collection of bootstrap profiles.
  <dl>
   <dt>profiles:</dt>
     <dd>
     List of one or more bootstrap profiles, in descending
     preference order.
     </dd>
   </dl>
  
  Attributes:
   - profiles
  """

  thrift_spec = (
    None, # 0
    (1, TType.LIST, 'profiles', (TType.STRUCT,(BootstrapProfile, BootstrapProfile.thrift_spec)), None, ), # 1
  )

  def __init__(self, profiles=None,):
    self.profiles = profiles

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.LIST:
          self.profiles = []
          (_etype3, _size0) = iprot.readListBegin()
          for _i4 in range(_size0):
            _elem5 = BootstrapProfile()
            _elem5.read(iprot)
            self.profiles.append(_elem5)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('BootstrapInfo')
    if self.profiles is not None:
      oprot.writeFieldBegin('profiles', TType.LIST, 1)
      oprot.writeListBegin(TType.STRUCT, len(self.profiles))
      for iter6 in self.profiles:
        iter6.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    if self.profiles is None:
      raise TProtocol.TProtocolException(message='Required field profiles is unset!')
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.items()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
