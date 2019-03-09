import logging
from itertools import groupby
from ctypes import c_int

from volcano.srv104.libiec import iec60870, CS101_CauseOfTransmission, IEC608705TypeID
from volcano.srv104.libiec import QualityDescriptor, CS104ServerMode
from volcano.srv104.libiec import event_handler_proto, CS104PeerConnectionEvent
from volcano.srv104.libiec import CS104_APCIParameters, CS101_AppLayerParameters
from volcano.srv104.libiec import asdu_handler_proto, interrogation_handler_proto
from volcano.srv104.libiec import connection_request_handler_proto_server


class Server104():
    def __init__(self, config):
        self.pool = None
        self.vclient = None
        self.log = logging.getLogger(__name__)
        self.log.debug("Init Server 104")
        self.slave = iec60870.CS104_Slave_create(100, 100)
        iec60870.CS104_Slave_setLocalAddress(self.slave, b"0.0.0.0")
        iec60870.CS104_Slave_setServerMode(
            self.slave, CS104ServerMode.CS104_MODE_CONNECTION_IS_REDUNDANCY_GROUP.value)
        self.al_parameters = iec60870.CS104_Slave_getAppLayerParameters(
            self.slave)
        self.apci_parameters = iec60870.CS104_Slave_getConnectionParameters(
            self.slave)
        self.apci_parameters[0].k = config.k
        self.apci_parameters[0].w = config.w
        self.apci_parameters[0].t0 = config.t0
        self.apci_parameters[0].t1 = config.t1
        self.apci_parameters[0].t2 = config.t2
        self.apci_parameters[0].t3 = config.t3
        self.apci_parameters = iec60870.CS104_Slave_getConnectionParameters(
            self.slave)

        # set event handler
        self.event_handler_wrapped = event_handler_proto(self.event_handler)
        iec60870.CS104_Slave_setConnectionEventHandler(
            self.slave, self.event_handler_wrapped, c_int())

        # set asdu handler
        self.asdu_hand = asdu_handler_proto(self.asdu_handler)
        iec60870.CS104_Slave_setASDUHandler(
            self.slave, self.asdu_hand, c_int())

        # set interrogation handler
        self.con_req_handler = connection_request_handler_proto_server(
            self.connection_req_handler)
        iec60870.CS104_Slave_setConnectionRequestHandler(
            self.slave, self.con_req_handler, c_int())

        # set interrogation handler
        self.inter_handler = interrogation_handler_proto(
            self.interrogation_handler)
        iec60870.CS104_Slave_setInterrogationHandler(
            self.slave, self.inter_handler, c_int())

    def _create_asdu(self,
                     is_sequence=False,
                     cot=CS101_CauseOfTransmission.CS101_COT_PERIODIC.value):
        return iec60870.CS101_ASDU_create(self.al_parameters, is_sequence,
                                          cot, 0, 1, False, False)

    def _get_iec_iobject(self, io):
        if io.type is IEC608705TypeID.M_SP_NA_1.value:
            return iec60870.SinglePointInformation_create(
                None, int(io.ioa), bool(io.value),
                QualityDescriptor(io.quality).value)
        if io.type is IEC608705TypeID.M_ME_NC_1.value:
            return iec60870.MeasuredValueShort_create(
                None, int(io.ioa), float(io.value),
                QualityDescriptor(io.quality).value)

    def start(self):
        self.log.debug("Start Server 104")
        iec60870.CS104_Slave_start(self.slave)

    def stop(self):
        self.log.debug("Stop Server 104")
        iec60870.CS104_Slave_stop(self.slave)

    def asdu_handler(self, parameter, connection, asdu):
        asdu_count = iec60870.CS101_ASDU_getNumberOfElements(asdu)
        if iec60870.CS101_ASDU_getCOT(asdu) == CS101_CauseOfTransmission.CS101_COT_ACTIVATION.value:
            self.log.debug("received CS101_COT_ACTIVATION")
            command_io = iec60870.CS101_ASDU_getElement(asdu, 0)
            command_type = iec60870.InformationObject_getType(command_io)
            command_ioa = iec60870.InformationObject_getObjectAddress(
                command_io)
            if command_ioa in self.pool.ioaddresses():
                self.log.debug("Command can be done!")

                io = self.pool.get_io_by_addr(command_ioa)
                self.log.debug("TYPES: {0} vs {1}".format(
                    command_type, io.type))
                if iec60870.CS101_ASDU_getTypeID(asdu) == IEC608705TypeID.C_SE_NA_1.value:
                    self.log.debug(
                        "received set point normalized(int) value C_SE_NA_1")
                    value = iec60870.SetpointCommandNormalized_getValue(
                        command_io)
                    self.log.debug("Value SP = {0}".format(value))
                    self.vclient.set(io.name, int(value), 0)
                if iec60870.CS101_ASDU_getTypeID(asdu) == IEC608705TypeID.C_SE_NC_1.value:
                    self.log.debug("received set point float value C_SE_NC_1")
                    value = iec60870.SetpointCommandShort_getValue(command_io)
                    self.log.debug("Value SP = {0}".format(value))
                    self.vclient.set(io.name, float(value), 0)

                iec60870.CS101_ASDU_setCOT(
                    asdu, CS101_CauseOfTransmission.CS101_COT_ACTIVATION_CON.value)
                iec60870.InformationObject_destroy(command_io)
                iec60870.IMasterConnection_sendASDU(connection, asdu)
                return True
        return False

    def connection_req_handler(self, parameter, ip):
        # print("Parameter ", parameter)
        self.log.debug("Accepted connection from {0}".format(ip.decode()))
        return True

    def event_handler(self, parameter, connection, event):
        if event == CS104PeerConnectionEvent.CS104_CON_EVENT_CONNECTION_OPENED.value:
            self.log.debug("Connection opened {0}".format(event))
        elif event == CS104PeerConnectionEvent.CS104_CON_EVENT_CONNECTION_CLOSED.value:
            self.log.debug("Connection closed {0}".format(event))
        elif event == CS104PeerConnectionEvent.CS104_CON_EVENT_ACTIVATED.value:
            self.log.debug("Connection activated {0}".format(event))
        elif event == CS104PeerConnectionEvent.CS104_CON_EVENT_DEACTIVATED.value:
            self.log.debug("Connection deactivated {0}".format(event))

    def interrogation_handler(self, parameter, connection, asdu, qoi):
        self.log.debug("ASDU {0}".format(iec60870.CS101_ASDU_getCOT(asdu)))
        if qoi is int(20):
            self.log.debug("Station Interrogation internal")
            for key, group in groupby(self.pool.get_measures(), key=lambda x: x.type):
                new_asdu = self._create_asdu(
                    is_sequence=True,
                    cot=CS101_CauseOfTransmission.CS101_COT_INTERROGATED_BY_STATION.value)
                for io in group:
                    self.log.debug("IO---> {0}, {1}, {2}, {3}".format(io.type,
                                                                      io.name, io.value, io.quality))
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
        self.log.debug("send to {0}".format(
            iec60870.InformationObject_getObjectAddress(iec_io)))
        iec60870.InformationObject_destroy(iec_io)
        iec60870.CS104_Slave_enqueueASDU(self.slave, new_asdu)
        iec60870.CS101_ASDU_destroy(new_asdu)

    # def write(self, io_object):
    #     print(io_object)
    #     print("IOA Type To Write ---", io_object.type)
    #     print("Write value to Client")

        # iec60870.CS101_ASDU_addInformationObject(new_asdu, io)
        # print("VALUE-", iec60870.SinglePointInformation_getValue(io))
        # print("ADDR-", iec60870.InformationObject_getObjectAddress(io))
        # iec60870.InformationObject_destroy(io)
        # iec60870.CS104_Slave_enqueueASDU(self.slave, new_asdu)
        # iec60870.CS101_ASDU_destroy(new_asdu)
