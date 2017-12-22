import logging
import serial
import errno
import sys
import glob
from elm327 import ELM327, OBDStatus

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger("ELMAPI")

def try_port(portStr):
    """returns boolean for port availability"""
    try:
        s = serial.Serial(portStr)
        s.close() # explicit close 'cause of delayed GC in java
        return True

    except serial.SerialException:
        pass
    except OSError as e:
        if e.errno != errno.ENOENT: # permit "no such file or directory" errors
            raise e

    return False

def scan_serial():
    """scan for available ports. return a list of serial names"""
    available = []

    possible_ports = []

    if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        possible_ports += glob.glob("/dev/rfcomm[0-9]*")
        possible_ports += glob.glob("/dev/ttyUSB[0-9]*")
    elif sys.platform.startswith('win'):
        possible_ports += ["\\.\COM%d" % i for i in range(256)]

    elif sys.platform.startswith('darwin'):
        exclude = [
            '/dev/tty.Bluetooth-Incoming-Port',
            '/dev/tty.Bluetooth-Modem'
        ]
        possible_ports += [port for port in glob.glob('/dev/tty.*') if port not in exclude]

    for port in possible_ports:
        if try_port(port):
            available.append(port)

    return available

def enableDebug():
    logger.setLevel(logging.DEBUG)

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
            self.interface = ELM327(port, baudrate, protocol)

            if self.interface.status() == OBDStatus.CAR_CONNECTED:
                break # success! stop searching for serial

        if self.interface.status() != OBDStatus.CAR_CONNECTED:
            logger.warning("Could not connect to any of the given ports")
            exit(1)

        logger.info("Connection succesfull")
        logger.info(" Port:\t\t" + self.interface.port_name())
        logger.info(" Protocol id:\t" + self.interface.protocol_id())
        logger.info(" Protocol name:\t" + self.interface.protocol_name())
        if self.interface.protocol_id() in ["6", "7", "8", "9"]:
            logger.info(" Protocol mode:\t[ CAN ]")
        else:
            logger.info(" Protocol mode:\t[NOCAN]")

    def send_and_parse(self, cmd):
        if self.interface.status() != OBDStatus.CAR_CONNECTED:
            logger.warning("No car connected")
            exit(1)
        return self.interface.send_and_parse(cmd)