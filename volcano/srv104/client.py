
import logging
from ctypes import c_int
from volcano.srv104.libiec import iec60870, connection_request_handler_proto_client
from volcano.srv104.libiec import asdu_handler_proto_client, CS101_CauseOfTransmission
from volcano.srv104.libiec import QualifierOfInterrogation, IEC608705TypeID
from volcano.srv104.tag import Tag, ClientStorage


class Client104():

    def __init__(self, ip="127.0.0.1"):
        self.ip: bytes = ip.encode()
        self.port: int = 2404
        self.storage: ClientStorage = ClientStorage()
        self.is_connected = None
        self.logger = logging.getLogger(__name__)

        # create connection
        self.connection = iec60870.CS104_Connection_create(
            self.ip, self.port)

        # set connection handler
        self.logger.debug("set connection handler")
        self.con_handler = connection_request_handler_proto_client(
            self.connection_req_handler)
        iec60870.CS104_Connection_setConnectionHandler(
            self.connection, self.con_handler, c_int())

        # set asdu handler
        self.logger.debug("set asdu handler")
        self.asdu_handler = asdu_handler_proto_client(
            self.asdu_received_handler)
        iec60870.CS104_Connection_setASDUReceivedHandler(
            self.connection, self.asdu_handler, c_int())

    def start(self):

        self.is_connected = iec60870.CS104_Connection_connect(self.connection)
        iec60870.CS104_Connection_sendStartDT(self.connection)
        self.logger.debug("Structure param running={0}".format(
            self.connection[0].receiveCount))
        self.logger.debug("Client Connected")

    def stop(self):
        self.logger.debug("Stopping client/Close connection")
        iec60870.CS104_Connection_close(self.connection)
        self.logger.debug("Stopping client/Destroy connection")
        iec60870.CS104_Connection_destroy(self.connection)

    def send_gi(self):
        return iec60870.CS104_Connection_sendInterrogationCommand(
            self.connection,
            CS101_CauseOfTransmission.CS101_COT_ACTIVATION.value,
            1,
            QualifierOfInterrogation.IEC60870_QOI_STATION.value
        )

    def con_destroy(self):
        self.logger.debug("Destroy connection")
        iec60870.CS104_Connection_destroy(self.connection)

    def close(self):
        self.logger.debug("Just Close connection")
        iec60870.CS104_Connection_close(self.connection)

    def iterate_all(self):
        for k, v in self.storage.items:
            print(k, " --- ", v.value, v.type, v.ioa)

    @property
    def connected(self) -> bool:
        return self.is_connected

    def asdu_received_handler(self, parameter, ioa, asdu):
        asdu_type = iec60870.CS101_ASDU_getTypeID(asdu)
        asdu_len = iec60870.CS101_ASDU_getNumberOfElements(asdu)
        for idx in range(asdu_len):
            io = iec60870.CS101_ASDU_getElement(asdu, idx)
            ioa = iec60870.InformationObject_getObjectAddress(io)
            if asdu_type == IEC608705TypeID.M_SP_NA_1.value:
                value = iec60870.SinglePointInformation_getValue(io)
                quality = iec60870.SinglePointInformation_getQuality(io)
                iec60870.SinglePointInformation_destroy(io)
            if asdu_type == IEC608705TypeID.M_ME_NC_1.value:
                value = iec60870.MeasuredValueShort_getValue(io)
                quality = iec60870.MeasuredValueShort_getQuality(io)
                iec60870.MeasuredValueShort_destroy(io)
            self.storage.update(Tag(ioa, asdu_type, value, quality))
        return True

    def connection_req_handler(self, parameter, connection, event):
        if int(event) == 0:
            self.logger.debug("Connection established {0}".format(event))
        elif int(event) == 1:
            self.logger.debug("Connection closed {0}".format(event))
        elif int(event) == 2:
            self.logger.debug(
                "Connection startDT CON RECEIVED {0}".format(event))
        elif int(event) == 3:
            self.logger.debug(
                "Connection stopDT CON RECEIVED {0}".format(event))
        return True
