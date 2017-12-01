import sys
import obd

obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information

connection = obd.OBD() # auto-connects to USB or RF port

import test_graph
while True:
    response = connection.query(obd.commands.SPEED) # send the command, and parse the response

    if response.value == None:
        print("SUCCESS - NO")
    else:
        print("SUCCESS - KPH VALUE: " + str(response.value)) # user-friendly unit conversions
        test_graph.addData(0, 0, int(str(response.value.to("kph")).split(" ")[0]))


