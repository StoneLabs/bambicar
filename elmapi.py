import logging
from obd.elm327 import ELM327
from obd.utils import scan_serial, OBDStatus

logger = logging.getLogger(__name__)


class ELMAPI:
    interface = None
    
    def __init__(self, portname=None, baudrate=None, protocol=None):
        portnames = []

        if portname == None:
            logger.info("Using scan_serial to select port")
            portnames = scan_serial()

            logger.info("Available ports: " + str(portnames))
            if not portnames:
                logger.warning("No OBD-II adapters found")
                exit(1)
        else:
            portnames = [portname]

        for port in portnames:
            logger.info("Attempting to use port: " + str(port))
            interface = ELM327(port, baudrate, protocol)

            if interface.status() == OBDStatus.CAR_CONNECTED:
                break # success! stop searching for serial

        if interface.status() != OBDStatus.CAR_CONNECTED:
            print("Could not connect to any of the given ports")
            exit(1)

            print("Connection succesfull")
            print(" Port:\t\t" + interface.port_name())
            print(" Protocol id:\t" + interface.protocol_id())
            print(" Protocol name:\t" + interface.protocol_name())
            if interface.protocol_id() in ["6", "7", "8", "9"]:
                print(" Protocol mode:\t[ CAN ]")
            else:
                print(" Protocol mode:\t[NOCAN]")