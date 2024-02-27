# Copyright 1996-2023 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This controller gives to its node the following behavior:
Listen the keyboard. According to the pressed key, send a
message through an emitter or handle the position of Robot1.
"""
import threading

from controller import Supervisor
from common import common_print
import math
import paho.mqtt.client as mqtt


broker_address = "localhost"
port = 1883
topic = "iot"


            
            # Start the MQTT loop
# client.loop_forever()

def on_message(client, userdata, message):
    # time series data collection
    print("Received message:\n", str(message.payload.decode("utf-8")))

# Function to run the MQTT client in the background
def mqtt_client_thread():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "SUBSCRIBER")
    # Set up callback
    client.on_message = on_message
    # Connect to the broker
    client.connect(broker_address, port)
    # Subscribe to the topic
    client.subscribe(topic)
    # Start the MQTT loop
    client.loop_forever()

# Start the MQTT client in a separate thread
mqtt_thread = threading.Thread(target=mqtt_client_thread)
mqtt_thread.start()















class Driver (Supervisor):
    timeStep = 128
    x = -0.3
    y = -0.1
    translation = [x, y, 0]

    def __init__(self):
        super(Driver, self).__init__()
        self.emitter = self.getDevice('emitter')
        self.receiver = self.getDevice('receiver')
        self.receiver.enable(self.timeStep)
        robot = self.getFromDef('ROBOT1')
        self.translationField = robot.getField('translation')
        self.keyboard.enable(Driver.timeStep)
        self.keyboard = self.getKeyboard()

    def run(self):
        self.displayHelp()
        previous_message = ''

        # Main loop.
        while True:
            # Deal with the pressed keyboard key.
            k = self.keyboard.getKey()
            message = ''
            if k == ord('A'):
                message = 'avoid obstacles'
            elif k == ord('F'):
                message = 'move forward'
            elif k == ord('S'):
                message = 'stop'
            elif k == ord('T'):
                message = 'turn'
            elif k == ord('I'):
                self.displayHelp()
            elif k == ord('G'):
                translationValues = self.translationField.getSFVec3f()
                print('ROBOT1 is located at (' + str(translationValues[0]) + ',' + str(translationValues[1]) + ')')
            elif k == ord('R'):
                print('Teleport ROBOT1 at (' + str(self.x) + ',' + str(self.y) + ')')
                self.translationField.setSFVec3f(self.translation)
            
            # if self.receiver.getQueueLength() > 0:
                # message = self.receiver.getString()
                # print(message)
                
           
                    
            if message != '' and message != previous_message:
                previous_message = message
                print('Please, ' + message)
                self.emitter.send(message.encode('utf-8'))

            # Perform a simulation step, quit the loop when
            # Webots is about to quit.
            if self.step(self.timeStep) == -1:
                break

    def displayHelp(self):
        print(
            'Commands:\n'
            ' I for displaying the commands\n'
            ' A for avoid obstacles\n'
            ' F for move forward\n'
            ' S for stop\n'
            ' T for turn\n'
            ' R for positioning ROBOT1 at (-0.3,-0.1)\n'
            ' G for knowing the (x,y) position of ROBOT1'
        )


controller = Driver()
common_print('driver')
controller.run()
