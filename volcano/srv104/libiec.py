from enum import Enum
from ctypes import util, CFUNCTYPE, POINTER, CDLL, cdll
from ctypes import Structure
from ctypes import c_float, c_int, c_void_p, c_char_p, c_char, c_bool, c_uint8
from ctypes import c_uint64, c_uint32

iec60870 = CDLL('/usr/local/lib/liblib60870.so')
# print(CDLL('liblib60870.so'))
# print(cdll.LoadLibrary("liblib60870.so"))
# iec60870 = CDLL(util.find_library('liblib60870'))
# iec60870 = cdll.LoadLibrary(util.find_library('liblib60870'))

HOST_NAME_MAX = 64


class Server104Config():
    def __init__(self):
        self.ip_address = "0.0.0.0"
        self.port = 2404
        self.t0 = 10
        self.t1 = 15
        self.t2 = 10
        self.t3 = 20
        self.k = 12
        self.w = 8
        self.cot_size = 2

    def validate(self):
        return self.ip_address\
            and self.port\
            and self.t0\
            and self.t1\
            and self.t2\
            and self.t3\
            and self.cot_size


# sSocket
class sSocket(Structure):
    _fields_ = [
        ('fd', c_int),
        ('connectTimeout', c_uint32)
    ]


# SentASDU
class SentASDU(Structure):
    _fields_ = [
        ('sentTime', c_uint64),
        ('seqNo', c_int)
    ]


# CS104_APCIParameters
class CS104_APCIParameters(Structure):
    _fields_ = [
        ('k', c_int),  # 12
        ('w', c_int),  # 8
        ('t0', c_int),  # 10
        ('t1', c_int),  # 15
        ('t2', c_int),  # 10
        ('t3', c_int)  # 20
    ]


# CS101_AppLayerParameters
class CS101_AppLayerParameters(Structure):
    _fields_ = [
        ('sizeOfTypeId', c_int),
        ('sizeOfVSQ', c_int),
        ('sizeOfCOT', c_int),
        ('originatorAddress', c_int),
        ('sizeOfCA', c_int),
        ('sizeOfIOA', c_int),
        ('maxSizeOfASDU', c_int)
    ]


# CS104_Connection
class CS104_Connection(Structure):
    _fields_ = [
        ('hostname', c_char * (HOST_NAME_MAX + 1)),
        ('tcpPort', c_int),
        ('sCS104_APCIParameters', CS104_APCIParameters),
        ('sCS101_AppLayerParameters', CS101_AppLayerParameters),
        ('connectTimeoutInMs', c_int),
        ('sMessage', c_uint8 * 6),
        ('sentASDUs', SentASDU),
        ('maxSentASDUs', c_int),
        ('oldestSentASDU', c_int),
        ('newestSentASDU', c_int),
        ('sentASDUsLock', c_void_p),
        ('connectionHandlingThread', c_void_p),
        ('receiveCount', c_int),
        ('sendCount', c_int),
        ('unconfirmedReceivedIMessages', c_int),
        ('timeoutT2Trigger', c_bool),
        ('lastConfirmationTime', c_uint64),
        ('nextT3Timeout', c_uint64),
        ('outstandingTestFCConMessages', c_int),
        ('uMessageTimeout', c_uint64),
        ('socket', sSocket),
        ('running', c_bool),
        ('failure', c_bool),
        ('close', c_bool)
    ]


# CS104PeerConnectionEvent
class CS104PeerConnectionEvent(Enum):
    CS104_CON_EVENT_CONNECTION_OPENED = 0
    CS104_CON_EVENT_CONNECTION_CLOSED = 1
    CS104_CON_EVENT_ACTIVATED = 2
    CS104_CON_EVENT_DEACTIVATED = 3


# QualityDescriptor
class QualityDescriptor(Enum):
    IEC60870_QUALITY_GOOD = 0
    IEC60870_QUALITY_OVERFLOW = 0x01
    IEC60870_QUALITY_NOT_INIT = 0x02
    IEC60870_QUALITY_RESERVED = 0x04
    IEC60870_QUALITY_ELAPSED_TIME_INVALID = 0x08
    IEC60870_QUALITY_BLOCKED = 0x10
    IEC60870_QUALITY_SUBSTITUTED = 0x20
    IEC60870_QUALITY_NON_TOPICAL = 0x40
    IEC60870_QUALITY_INVALID = 0x80


class QualifierOfInterrogation(Enum):
    IEC60870_QOI_STATION = 20
    IEC60870_QOI_GROUP_1 = 21
    IEC60870_QOI_GROUP_2 = 22
    IEC60870_QOI_GROUP_3 = 23
    IEC60870_QOI_GROUP_4 = 24
    IEC60870_QOI_GROUP_5 = 25
    IEC60870_QOI_GROUP_6 = 26
    IEC60870_QOI_GROUP_7 = 27
    IEC60870_QOI_GROUP_8 = 28
    IEC60870_QOI_GROUP_9 = 29
    IEC60870_QOI_GROUP_10 = 30
    IEC60870_QOI_GROUP_11 = 31
    IEC60870_QOI_GROUP_12 = 32
    IEC60870_QOI_GROUP_13 = 33
    IEC60870_QOI_GROUP_14 = 34
    IEC60870_QOI_GROUP_15 = 35
    IEC60870_QOI_GROUP_16 = 36


# CS101_CauseOfTransmission
class CS101_CauseOfTransmission(Enum):
    CS101_COT_PERIODIC = 1
    CS101_COT_BACKGROUND_SCAN = 2
    CS101_COT_SPONTANEOUS = 3
    CS101_COT_INITIALIZED = 4
    CS101_COT_REQUEST = 5
    CS101_COT_ACTIVATION = 6
    CS101_COT_ACTIVATION_CON = 7
    CS101_COT_DEACTIVATION = 8
    CS101_COT_DEACTIVATION_CON = 9
    CS101_COT_ACTIVATION_TERMINATION = 10
    CS101_COT_RETURN_INFO_REMOTE = 11
    CS101_COT_RETURN_INFO_LOCAL = 12
    CS101_COT_FILE_TRANSFER = 13
    CS101_COT_AUTHENTICATION = 14
    CS101_COT_MAINTENANCE_OF_AUTH_SESSION_KEY = 15
    CS101_COT_MAINTENANCE_OF_USER_ROLE_AND_UPDATE_KEY = 16
    CS101_COT_INTERROGATED_BY_STATION = 20
    CS101_COT_INTERROGATED_BY_GROUP_1 = 21
    CS101_COT_INTERROGATED_BY_GROUP_2 = 22
    CS101_COT_INTERROGATED_BY_GROUP_3 = 23
    CS101_COT_INTERROGATED_BY_GROUP_4 = 24
    CS101_COT_INTERROGATED_BY_GROUP_5 = 25
    CS101_COT_INTERROGATED_BY_GROUP_6 = 26
    CS101_COT_INTERROGATED_BY_GROUP_7 = 27
    CS101_COT_INTERROGATED_BY_GROUP_8 = 28
    CS101_COT_INTERROGATED_BY_GROUP_9 = 29
    CS101_COT_INTERROGATED_BY_GROUP_10 = 30
    CS101_COT_INTERROGATED_BY_GROUP_11 = 31
    CS101_COT_INTERROGATED_BY_GROUP_12 = 32
    CS101_COT_INTERROGATED_BY_GROUP_13 = 33
    CS101_COT_INTERROGATED_BY_GROUP_14 = 34
    CS101_COT_INTERROGATED_BY_GROUP_15 = 35
    CS101_COT_INTERROGATED_BY_GROUP_16 = 36
    CS101_COT_REQUESTED_BY_GENERAL_COUNTER = 37
    CS101_COT_REQUESTED_BY_GROUP_1_COUNTER = 38
    CS101_COT_REQUESTED_BY_GROUP_2_COUNTER = 39
    CS101_COT_REQUESTED_BY_GROUP_3_COUNTER = 40
    CS101_COT_REQUESTED_BY_GROUP_4_COUNTER = 41
    CS101_COT_UNKNOWN_TYPE_ID = 44
    CS101_COT_UNKNOWN_COT = 45
    CS101_COT_UNKNOWN_CA = 46
    CS101_COT_UNKNOWN_IOA = 47


# IEC60870_5_TypeID
class IEC608705TypeID(Enum):
    NONE = 0
    M_SP_NA_1 = 1
    M_SP_TA_1 = 2
    M_DP_NA_1 = 3
    M_DP_TA_1 = 4
    M_ST_NA_1 = 5
    M_ST_TA_1 = 6
    M_BO_NA_1 = 7
    M_BO_TA_1 = 8
    M_ME_NA_1 = 9
    M_ME_TA_1 = 10
    M_ME_NB_1 = 11
    M_ME_TB_1 = 12
    M_ME_NC_1 = 13
    M_ME_TC_1 = 14
    M_IT_NA_1 = 15
    M_IT_TA_1 = 16
    M_EP_TA_1 = 17
    M_EP_TB_1 = 18
    M_EP_TC_1 = 19
    M_PS_NA_1 = 20
    M_ME_ND_1 = 21
    M_SP_TB_1 = 30
    M_DP_TB_1 = 31
    M_ST_TB_1 = 32
    M_BO_TB_1 = 33
    M_ME_TD_1 = 34
    M_ME_TE_1 = 35
    M_ME_TF_1 = 36
    M_IT_TB_1 = 37
    M_EP_TD_1 = 38
    M_EP_TE_1 = 39
    M_EP_TF_1 = 40
    C_SC_NA_1 = 45
    C_DC_NA_1 = 46
    C_RC_NA_1 = 47
    C_SE_NA_1 = 48
    C_SE_NB_1 = 49
    C_SE_NC_1 = 50
    C_BO_NA_1 = 51
    C_SC_TA_1 = 58
    C_DC_TA_1 = 59
    C_RC_TA_1 = 60
    C_SE_TA_1 = 61
    C_SE_TB_1 = 62
    C_SE_TC_1 = 63
    C_BO_TA_1 = 64
    M_EI_NA_1 = 70
    C_IC_NA_1 = 100
    C_CI_NA_1 = 101
    C_RD_NA_1 = 102
    C_CS_NA_1 = 103
    C_TS_NA_1 = 104
    C_RP_NA_1 = 105
    C_CD_NA_1 = 106
    C_TS_TA_1 = 107
    P_ME_NA_1 = 110
    P_ME_NB_1 = 111
    P_ME_NC_1 = 112
    P_AC_NA_1 = 113
    F_FR_NA_1 = 120
    F_SR_NA_1 = 121
    F_SC_NA_1 = 122
    F_LS_NA_1 = 123
    F_AF_NA_1 = 124
    F_SG_NA_1 = 125
    F_DR_TA_1 = 126
    F_SC_NB_1 = 127

    @staticmethod
    def from_node(node):
        if node.tag == "MSP" and node.get("Format") == "NA":
            return IEC608705TypeID.M_SP_NA_1.value
        if node.tag == "MME" and node.get("Format") == "NC":
            return IEC608705TypeID.M_ME_NC_1.value
        if node.tag == "CSE" and node.get("Format") == "NA":
            return IEC608705TypeID.C_SE_NA_1.value
        if node.tag == "CSE" and node.get("Format") == "NC":
            return IEC608705TypeID.C_SE_NC_1.value
        return IEC608705TypeID.NONE.value


# CS104_ServerMode
class CS104ServerMode(Enum):
    CS104_MODE_SINGLE_REDUNDANCY_GROUP = 0
    CS104_MODE_CONNECTION_IS_REDUNDANCY_GROUP = 1
    CS104_MODE_MULTIPLE_REDUNDANCY_GROUPS = 2


# CS104_Connection_close
iec60870.CS104_Connection_close.argtypes = [c_void_p]
iec60870.CS104_Connection_close.restype = c_void_p

# CS104_Connection_destroy
iec60870.CS104_Connection_destroy.argtypes = [c_void_p]
iec60870.CS104_Connection_destroy.restype = c_void_p

# CS104_Connection_connect
iec60870.CS104_Connection_connect.argtypes = [c_void_p]
iec60870.CS104_Connection_connect.restype = c_bool

# Thread_sleep
iec60870.Thread_sleep.argtypes = [c_int]
iec60870.Thread_sleep.restype = c_void_p

# CS104_Connection_create
iec60870.CS104_Connection_create.argtypes = [c_char_p, c_int]
iec60870.CS104_Connection_create.restype = POINTER(CS104_Connection)

# CS104_Connection_setConnectionHandler
iec60870.CS104_Connection_setConnectionHandler.argtypes = [
    c_void_p, c_void_p, c_int]
iec60870.CS104_Connection_setConnectionHandler.restype = c_void_p


# ###################################################################
#                                                               Server
# ###################################################################

# SetpointCommandShort_getValue
iec60870.SetpointCommandShort_getValue.argtypes = [c_void_p]
iec60870.SetpointCommandShort_getValue.restype = c_float

# SetpointCommandNormalized_getValue
iec60870.SetpointCommandNormalized_getValue.argtypes = [c_void_p]
iec60870.SetpointCommandNormalized_getValue.restype = c_float

# CS101_ASDU_getTypeID
iec60870.CS101_ASDU_getTypeID.argtypes = [c_void_p]
iec60870.CS101_ASDU_getTypeID.restype = c_int

# CS101_ASDU_getCOT
iec60870.CS101_ASDU_getCOT.argtypes = [c_void_p]
iec60870.CS101_ASDU_getCOT.restype = c_int

# CS101_ASDU_setCOT
iec60870.CS101_ASDU_setCOT.argtypes = [c_void_p, c_int]
iec60870.CS101_ASDU_setCOT.restype = c_void_p

# InformationObject_getType
iec60870.InformationObject_getType.argtypes = [c_void_p]
iec60870.InformationObject_getType.restype = c_int

# CS101_ASDU_getNumberOfElements
iec60870.CS101_ASDU_getNumberOfElements.argtypes = [c_void_p]
iec60870.CS101_ASDU_getNumberOfElements.restype = c_int

# CS101_ASDU_getElement
iec60870.CS101_ASDU_getElement.argtypes = [c_void_p, c_int]
iec60870.CS101_ASDU_getElement.restype = c_void_p

# InformationObject_getObjectAddress
iec60870.InformationObject_getObjectAddress.argtypes = [c_void_p]
iec60870.InformationObject_getObjectAddress.restype = c_int

# CS101_ASDU_destroy
iec60870.CS101_ASDU_destroy.argtypes = [c_void_p]
iec60870.CS101_ASDU_destroy.restype = c_void_p

# IMasterConnection_sendASDU
iec60870.IMasterConnection_sendASDU.argtypes = [c_void_p, c_void_p]
iec60870.IMasterConnection_sendASDU.restype = c_void_p

# InformationObject_destroy
iec60870.InformationObject_destroy.argtypes = [c_void_p]
iec60870.InformationObject_destroy.restype = c_void_p

# CS101_ASDU_addInformationObject
iec60870.CS101_ASDU_addInformationObject.argtypes = [c_void_p, c_void_p]
iec60870.CS101_ASDU_addInformationObject.restype = c_bool

# MeasuredValueScaled_create
iec60870.MeasuredValueScaled_create.argtypes = [
    c_void_p, c_int, c_int, c_void_p
]
iec60870.MeasuredValueScaled_create.restype = c_void_p

# MeasuredValueShort_create
iec60870.MeasuredValueShort_create.argtypes = [
    c_void_p, c_int, c_float, c_void_p
]
iec60870.MeasuredValueShort_create.restype = c_void_p

# MeasuredValueShort_getValue
iec60870.MeasuredValueShort_getValue.argtypes = [c_void_p]
iec60870.MeasuredValueShort_getValue.restype = c_float

# MeasuredValueShort_destroy
iec60870.MeasuredValueShort_destroy.argtypes = [c_void_p]
iec60870.MeasuredValueShort_destroy.restype = c_void_p


# SinglePointInformation_create
iec60870.SinglePointInformation_create.argtypes = [
    c_void_p, c_int, c_bool, c_void_p
]
iec60870.SinglePointInformation_create.restype = c_void_p

# MeasuredValueShort_getQuality
iec60870.MeasuredValueShort_getQuality.argtypes = [c_void_p]
iec60870.MeasuredValueShort_getQuality.restype = c_int

# MeasuredValueScaled_getValue
iec60870.MeasuredValueScaled_getValue.argtypes = [c_void_p]
iec60870.MeasuredValueScaled_getValue.restype = c_int

# SinglePointInformation_getValue
iec60870.SinglePointInformation_getValue.argtypes = [c_void_p]
iec60870.SinglePointInformation_getValue.restype = c_bool

# SinglePointInformation_getQuality
iec60870.SinglePointInformation_getQuality.argtypes = [c_void_p]
iec60870.SinglePointInformation_getQuality.restype = c_int

# SinglePointInformation_destroy
iec60870.SinglePointInformation_destroy.argtypes = [c_void_p]
iec60870.SinglePointInformation_destroy.restype = c_void_p

# CS101_ASDU_create
iec60870.CS101_ASDU_create.argtypes = [
    c_void_p, c_bool, c_void_p, c_int, c_int, c_bool, c_bool]
iec60870.CS101_ASDU_create.restype = c_void_p

# IMasterConnection_getApplicationLayerParameters
iec60870.IMasterConnection_sendACT_CON.argtypes = [c_void_p, c_void_p, c_bool]
iec60870.IMasterConnection_sendACT_CON.restype = c_void_p

# IMasterConnection_getApplicationLayerParameters
iec60870.IMasterConnection_getApplicationLayerParameters.argtypes = [c_void_p]
iec60870.IMasterConnection_getApplicationLayerParameters.restype = c_void_p

# CS104_Slave
iec60870.CS104_Slave_create.argtypes = [c_int, c_int]
iec60870.CS104_Slave_create.restype = c_void_p

# CS104_Slave_setLocalAddress
iec60870.CS104_Slave_setLocalAddress.argtypes = [c_void_p, c_char_p]
iec60870.CS104_Slave_setLocalAddress.restype = c_void_p

# CS104_Slave_setServerModes
iec60870.CS104_Slave_setServerMode.argtypes = [c_void_p, c_int]
iec60870.CS104_Slave_setServerMode.restype = c_void_p

# CS104_APCIParameters
iec60870.CS104_Slave_getConnectionParameters.argtypes = [c_void_p]
iec60870.CS104_Slave_getConnectionParameters.restype = POINTER(
    CS104_APCIParameters)

# CS104_Slave_getAppLayerParameters
iec60870.CS104_Slave_getAppLayerParameters.argtypes = [c_void_p]
iec60870.CS104_Slave_getAppLayerParameters.restype = POINTER(
    CS101_AppLayerParameters)

# CS104_Slave_start
iec60870.CS104_Slave_start.argtypes = [c_void_p]
iec60870.CS104_Slave_start.restype = c_void_p

# CS104_Slave_stop
iec60870.CS104_Slave_stop.argtypes = [c_void_p]
iec60870.CS104_Slave_stop.restype = c_void_p

# CS104_Slave_enqueueASDU
iec60870.CS104_Slave_enqueueASDU.argtypes = [c_void_p, c_void_p]
iec60870.CS104_Slave_enqueueASDU.restype = c_void_p

# CS104_Slave_isRunning
iec60870.CS104_Slave_isRunning.argtypes = [c_void_p]
iec60870.CS104_Slave_isRunning.restype = c_bool

# CS104_Slave_setConnectionRequestHandler
iec60870.CS104_Slave_setConnectionRequestHandler.argtypes = [
    c_void_p, c_void_p, c_int]
iec60870.CS104_Slave_setConnectionRequestHandler.restype = c_void_p

# CS104_Slave_setInterrogationHandler
iec60870.CS104_Slave_setInterrogationHandler.argtypes = [
    c_void_p, c_void_p, c_int]
iec60870.CS104_Slave_setInterrogationHandler.restype = c_void_p

# CS104_Slave_setConnectionEventHandler
iec60870.CS104_Slave_setConnectionEventHandler.argtypes = [
    c_void_p, c_void_p, c_int]
iec60870.CS104_Slave_setConnectionEventHandler.restype = c_void_p

# CS104_Slave_setASDUHandler
iec60870.CS104_Slave_setASDUHandler.argtypes = [c_void_p, c_void_p, c_int]
iec60870.CS104_Slave_setASDUHandler.restype = c_int

# CS104_Connection_sendInterrogationCommand
iec60870.CS104_Connection_sendInterrogationCommand.argtypes = [
    c_void_p, c_int, c_int, c_int]
iec60870.CS104_Connection_sendInterrogationCommand.restype = c_bool

# CS104_Connection_sendStartDT
iec60870.CS104_Connection_sendStartDT.argtypes = [c_void_p]
iec60870.CS104_Connection_sendStartDT.restype = c_void_p

# CS104_Connection_setASDUReceivedHandler
iec60870.CS104_Connection_setASDUReceivedHandler.argtypes = [
    c_void_p, c_void_p, c_int]
iec60870.CS104_Connection_setASDUReceivedHandler.restype = c_void_p


# connection_request_handler proto client
connection_request_handler_proto_client = CFUNCTYPE(
    c_bool,
    POINTER(c_void_p),
    POINTER(c_void_p),
    c_int
)

# connection_request_handler proto server
connection_request_handler_proto_server = CFUNCTYPE(
    c_bool,
    POINTER(c_void_p),
    c_char_p
)

# interrogation handler proto
interrogation_handler_proto = CFUNCTYPE(
    c_bool,
    POINTER(c_void_p),
    POINTER(c_void_p),
    POINTER(c_void_p),
    c_uint8
)

# asdu_handler_proto_client
asdu_handler_proto_client = CFUNCTYPE(
    c_bool,
    POINTER(c_void_p),
    c_int,
    POINTER(c_void_p)
)

# asdu handler proto
asdu_handler_proto = CFUNCTYPE(
    c_bool,
    POINTER(c_void_p),
    POINTER(c_void_p),
    POINTER(c_void_p)
)

# event handler proto
event_handler_proto = CFUNCTYPE(
    c_void_p,
    POINTER(c_void_p),
    POINTER(c_void_p),
    c_uint8
)
