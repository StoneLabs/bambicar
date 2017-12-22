import elmapi
import time

elmapi.logger.setLevel(elmapi.logging.DEBUG)
car = elmapi.ELMAPI()

#print(car.send_and_parse(b"010D"))

while (True):
    car.send_and_parse(bytes(input("> "), encoding='ascii'))
    while (True):
        print(car.interface.reader())
    time.sleep(0)