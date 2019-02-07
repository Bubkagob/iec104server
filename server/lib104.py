import signal
import sys
import time
from enum import Enum
from itertools import groupby
from ctypes import util, CFUNCTYPE, POINTER, CDLL, cdll
from ctypes import Structure
from ctypes import c_float, c_int, c_void_p, c_char_p, c_bool, c_uint8


iec60870 = CDLL('/usr/local/lib/liblib60870.so')
# iec60870 = cdll.LoadLibrary('iec60870')


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


# CS101_CauseOfTransmission
class CS101CauseOfTransmission(Enum):
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
    def from_string(type, format="NA"):
        if type == "MSP" and format == "NA":
            return IEC608705TypeID.M_SP_NA_1.value
        if type == "MME" and format == "NC":
            return IEC608705TypeID.M_ME_NC_1.value
        return IEC608705TypeID.NONE.value


# CS104_ServerMode
class CS104ServerMode(Enum):
    CS104_MODE_SINGLE_REDUNDANCY_GROUP = 0
    CS104_MODE_CONNECTION_IS_REDUNDANCY_GROUP = 1
    CS104_MODE_MULTIPLE_REDUNDANCY_GROUPS = 2


# CS104_PeerConnectionEvent
class CS104PeerConnectionEvent(Enum):
    CS104_CON_EVENT_CONNECTION_OPENED = 0
    CS104_CON_EVENT_CONNECTION_CLOSED = 1
    CS104_CON_EVENT_ACTIVATED = 2
    CS104_CON_EVENT_DEACTIVATED = 3


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


# SinglePointInformation_create
iec60870.SinglePointInformation_create.argtypes = [
    c_void_p, c_int, c_bool, c_void_p
]
iec60870.SinglePointInformation_create.restype = c_void_p

# MeasuredValueScaled_getValue
iec60870.MeasuredValueScaled_getValue.argtypes = [c_void_p]
iec60870.MeasuredValueScaled_getValue.restype = c_int

# SinglePointInformation_getValue
iec60870.SinglePointInformation_getValue.argtypes = [c_void_p]
iec60870.SinglePointInformation_getValue.restype = c_bool

# SinglePointInformation_getQuality
iec60870.SinglePointInformation_getQuality.argtypes = [c_void_p]
iec60870.SinglePointInformation_getQuality.restype = c_void_p

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
iec60870.CS104_Slave_getConnectionParameters.restype = POINTER(CS104_APCIParameters)

# CS104_Slave_getAppLayerParameters
iec60870.CS104_Slave_getAppLayerParameters.argtypes = [c_void_p]
iec60870.CS104_Slave_getAppLayerParameters.restype = POINTER(CS101_AppLayerParameters)

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


# connection_request_handler proto
connection_request_handler_proto = CFUNCTYPE(
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


def asdu_handler(parameter, connection, asdu):
    print("ASDU HANDLER!")
    if iec60870.CS101_ASDU_getTypeID(asdu) == IEC608705TypeID.C_SC_NA_1.value:
        print("received single command C_SC_NA_1")
        if iec60870.CS101_ASDU_getCOT(asdu) == CS101CauseOfTransmission.CS101_COT_ACTIVATION.value:
            print("received CS101_COT_ACTIVATION")

    return True


def event_handler(parameter, connection, event):
    if event == CS104PeerConnectionEvent.CS104_CON_EVENT_CONNECTION_OPENED.value:
        print("Connection opened")
    elif event == CS104PeerConnectionEvent.CS104_CON_EVENT_CONNECTION_CLOSED.value:
        print("Connection closed")
    elif event == CS104PeerConnectionEvent.CS104_CON_EVENT_ACTIVATED.value:
        print("Connection activated")
    elif event == CS104PeerConnectionEvent.CS104_CON_EVENT_DEACTIVATED.value:
        print("Connection deactivated")


def connection_req_handler(parameter, ip):
    # print("Parameter ", parameter)
    print("Accepted connection from ", ip.decode())
    return True


def interrogation_handler_old(parameter, connection, asdu, qoi):
    if qoi is int(20):
        print("Station Interrogation")
        al_parameters = iec60870.IMasterConnection_getApplicationLayerParameters(connection)
        iec60870.IMasterConnection_sendACT_CON(connection, asdu, False)

        new_asdu = iec60870.CS101_ASDU_create(
            al_parameters,
            False,
            CS101CauseOfTransmission.CS101_COT_INTERROGATED_BY_STATION.value,
            0,
            1,
            False,
            False
        )

        io = iec60870.SinglePointInformation_create(
            None,
            101,
            True,
            QualityDescriptor.IEC60870_QUALITY_GOOD.value
        )
        iec60870.CS101_ASDU_addInformationObject(new_asdu, io)
        print("VALUE", iec60870.SinglePointInformation_getValue(io))
        print("ADDR", iec60870.InformationObject_getObjectAddress(io))
        io = iec60870.SinglePointInformation_create(
            None,
            102,
            False,
            QualityDescriptor.IEC60870_QUALITY_GOOD.value
        )
        iec60870.CS101_ASDU_addInformationObject(new_asdu, io)
        print("VALUE2", iec60870.SinglePointInformation_getValue(io))
        print("ADDR2", iec60870.InformationObject_getObjectAddress(io))
        io = iec60870.SinglePointInformation_create(
            None,
            103,
            True,
            QualityDescriptor.IEC60870_QUALITY_GOOD.value
        )
        iec60870.CS101_ASDU_addInformationObject(new_asdu, io)
        print("VALUE3", iec60870.SinglePointInformation_getValue(io))
        print("ADDR3", iec60870.InformationObject_getObjectAddress(io))
        # iec60870.InformationObject_destroy(io)

        # Send that shit
        iec60870.IMasterConnection_sendASDU(connection, new_asdu)
        # iec60870.CS101_ASDU_destroy(new_asdu)
    return True


def interrogation_handler(parameter, connection, asdu, qoi):
    if qoi is int(20):
        print("Station Interrogation")

    return True


def main():
    slave = iec60870.CS104_Slave_create(100, 100)
    iec60870.CS104_Slave_setLocalAddress(slave, b"0.0.0.0")
    iec60870.CS104_Slave_setServerMode(
        slave, CS104ServerMode.CS104_MODE_MULTIPLE_REDUNDANCY_GROUPS.value)
    connection_parameters = iec60870.CS104_Slave_getAppLayerParameters(slave)

    # set interrogation handler
    inter_handler = interrogation_handler_proto(interrogation_handler)
    iec60870.CS104_Slave_setInterrogationHandler(slave, inter_handler, c_int())

    # set asdu handler
    asdu_handler_wrapped = asdu_handler_proto(asdu_handler)
    iec60870.CS104_Slave_setASDUHandler(slave, asdu_handler_wrapped, c_int())

    # set connection request handler
    con_req_handler = connection_request_handler_proto(connection_req_handler)
    iec60870.CS104_Slave_setConnectionRequestHandler(slave, con_req_handler, c_int())

    # set event handler
    event_handler_wrapped = event_handler_proto(event_handler)
    iec60870.CS104_Slave_setConnectionEventHandler(slave, event_handler_wrapped, c_int())

    # start server
    iec60870.CS104_Slave_start(slave)

    while True:
        time.sleep(1)


class Server104():

    def __init__(self, config):
        print("Init Server 104")
        self.tags = None
        self.vclient = None
        self.slave = iec60870.CS104_Slave_create(100, 100)
        iec60870.CS104_Slave_setLocalAddress(self.slave, b"0.0.0.0")
        iec60870.CS104_Slave_setServerMode(
            self.slave, CS104ServerMode.CS104_MODE_CONNECTION_IS_REDUNDANCY_GROUP.value)
        self.al_parameters = iec60870.CS104_Slave_getAppLayerParameters(self.slave)
        self.apci_parameters = iec60870.CS104_Slave_getConnectionParameters(self.slave)
        self.apci_parameters[0].k = config.k
        self.apci_parameters[0].w = config.w
        self.apci_parameters[0].t0 = config.t0
        self.apci_parameters[0].t1 = config.t1
        self.apci_parameters[0].t2 = config.t2
        self.apci_parameters[0].t3 = config.t3
        self.apci_parameters = iec60870.CS104_Slave_getConnectionParameters(self.slave)
        print("HERE2", self.apci_parameters[0].k)
        print("HERE2", self.apci_parameters[0].w)
        print("HERE2", self.apci_parameters[0].t0)
        print("HERE2", self.apci_parameters[0].t1)
        print("HERE2", self.apci_parameters[0].t2)
        print("HERE2", self.apci_parameters[0].t3)

        # set asdu handler
        self.asdu_hand = asdu_handler_proto(self.asdu_handler)
        iec60870.CS104_Slave_setASDUHandler(self.slave, self.asdu_hand, c_int())

        # set interrogation handler
        self.con_req_handler = connection_request_handler_proto(connection_req_handler)
        iec60870.CS104_Slave_setConnectionRequestHandler(self.slave, self.con_req_handler, c_int())

        # set interrogation handler
        self.inter_handler = interrogation_handler_proto(self.interrogation_handler)
        iec60870.CS104_Slave_setInterrogationHandler(self.slave, self.inter_handler, c_int())

    def _create_asdu(self,
                     is_sequence=False,
                     cot=CS101CauseOfTransmission.CS101_COT_PERIODIC.value):
        return iec60870.CS101_ASDU_create(self.al_parameters, is_sequence,
                                          cot, 0, 1, False, False)

    def _get_iec_iobject(self, io):
        if io.type is IEC608705TypeID.M_SP_NA_1.value:
            return iec60870.SinglePointInformation_create(
                None, int(io.ioa), bool(io.value),
                QualityDescriptor(io.quality).value)
        if io.type is IEC608705TypeID.M_ME_NC_1.value:
            return iec60870.MeasuredValueScaled_create(
                None, int(io.ioa), int(io.value),
                QualityDescriptor(io.quality).value)

    def start(self):
        print("Start Server 104")
        iec60870.CS104_Slave_start(self.slave)

    def stop(self):
        print("Stop Server 104")
        iec60870.CS104_Slave_stop(self.slave)

    def asdu_handler(self, parameter, connection, asdu):
        # print("asdu handler")
        asdu_count = iec60870.CS101_ASDU_getNumberOfElements(asdu)
        # print("Number of elements = ", asdu_count)
        if iec60870.CS101_ASDU_getCOT(asdu) == CS101CauseOfTransmission.CS101_COT_ACTIVATION.value:
            print("received CS101_COT_ACTIVATION")
            iec_io = iec60870.CS101_ASDU_getElement(asdu, 0)
            io_address = iec60870.InformationObject_getObjectAddress(iec_io)
            io_type = iec60870.InformationObject_getType(iec_io)
            if iec60870.CS101_ASDU_getTypeID(asdu) == IEC608705TypeID.C_SE_NA_1.value:
                print("received set point normalized(int) value C_SE_NA_1")
                value = iec60870.SetpointCommandNormalized_getValue(iec_io)
                print("Value SP =", value)
                self.vclient.set("test.f3.r10", int(value), 0)
            if iec60870.CS101_ASDU_getTypeID(asdu) == IEC608705TypeID.C_SE_NC_1.value:
                print("received set point float value C_SE_NC_1")
                value = iec60870.SetpointCommandShort_getValue(iec_io)
                print("Value SP =", value)

            iec60870.CS101_ASDU_setCOT(
                asdu, CS101CauseOfTransmission.CS101_COT_ACTIVATION_CON.value)
            iec60870.InformationObject_destroy(iec_io)
            iec60870.IMasterConnection_sendASDU(connection, asdu)
            return True
        return False

    def interrogation_handler(self, parameter, connection, asdu, qoi):
        print("ASDU", iec60870.CS101_ASDU_getCOT(asdu))
        if qoi is int(20):
            print("Station Interrogation internal")
            for key, group in groupby(self.tags.values(), key=lambda x: x.type):
                print(key, group)
                new_asdu = self._create_asdu(
                    is_sequence=True,
                    cot=CS101CauseOfTransmission.CS101_COT_INTERROGATED_BY_STATION.value)
                for io in group:
                    print("IO--->", io.type, io.name, io.value, io.quality)
                    iec_io = self._get_iec_iobject(io)
                    iec60870.CS101_ASDU_addInformationObject(new_asdu, iec_io)
                    iec60870.InformationObject_destroy(iec_io)
                iec60870.CS104_Slave_enqueueASDU(self.slave, new_asdu)
                iec60870.CS101_ASDU_destroy(new_asdu)

        return True

    def send(self, io):
        new_asdu = self._create_asdu()
        iec_io = self._get_iec_iobject(io)
        iec60870.CS101_ASDU_addInformationObject(new_asdu, iec_io)
        print("ADDR-", iec60870.InformationObject_getObjectAddress(iec_io))
        iec60870.InformationObject_destroy(iec_io)
        iec60870.CS104_Slave_enqueueASDU(self.slave, new_asdu)
        iec60870.CS101_ASDU_destroy(new_asdu)

    def write(self, io_object):
        print(io_object)
        print("IOA Type To Write ---", io_object.type)
        print("Write value to Client")
        new_asdu = iec60870.CS101_ASDU_create(
            self.al_parameters,
            False,
            CS101CauseOfTransmission.CS101_COT_PERIODIC.value,
            0,
            1,
            False,
            False
        )

        if io_object.type == "MME":

            io = iec60870.MeasuredValueScaled_create(
                None, int(io_object.ioa), int(value),
                QualityDescriptor(quality).value)

        elif io_object.type == "MSP":

            io = iec60870.SinglePointInformation_create(
                None, int(io_object.ioa), bool(value),
                QualityDescriptor(quality).value
            )

        # iec60870.CS101_ASDU_addInformationObject(new_asdu, io)
        # print("VALUE-", iec60870.SinglePointInformation_getValue(io))
        # print("ADDR-", iec60870.InformationObject_getObjectAddress(io))
        # iec60870.InformationObject_destroy(io)
        iec60870.CS104_Slave_enqueueASDU(self.slave, new_asdu)
        iec60870.CS101_ASDU_destroy(new_asdu)


if __name__ == '__main__':
    main()
