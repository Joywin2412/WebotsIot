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
This controller gives to its robot the following behavior:
According to the messages it receives, the robot change its
behavior.
"""

from controller import AnsiCodes, Robot
from common import common_print
import joblib
import random 
import paho.mqtt.client as mqtt
import time
from ml import predict
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


broker_address = "localhost"
# import socket
# print(socket.getaddrinfo('localhost', 1883))
port = 1883
topic = "iot"













class Enumerate(object):
    def __init__(self, names):
        for number, name in enumerate(names.split()):
            setattr(self, name, number)


class Slave(Robot):
    Mode = Enumerate('STOP MOVE_FORWARD AVOIDOBSTACLES TURN')
    timeStep = 32
    maxSpeed = 10.0
    mode = Mode.AVOIDOBSTACLES
    motors = []
    distanceSensors = []

    def boundSpeed(self, speed):
        return max(-self.maxSpeed, min(self.maxSpeed, speed))

    def __init__(self):
        super(Slave, self).__init__()
        self.mode = self.Mode.AVOIDOBSTACLES
        self.camera = self.getDevice('camera')
        self.camera.enable(4 * self.timeStep)
        self.receiver = self.getDevice('receiver')
        self.receiver.enable(self.timeStep)
        self.emitter = self.getDevice('emitter')
        # self.emitter.enable(self.timeStep)
        self.motors.append(self.getDevice("left wheel motor"))
        self.motors.append(self.getDevice("right wheel motor"))
        self.motors[0].setPosition(float("inf"))
        self.motors[1].setPosition(float("inf"))
        self.motors[0].setVelocity(0.0)
        self.motors[1].setVelocity(0.0)
        for dsnumber in range(0, 2):
            self.distanceSensors.append(self.getDevice('ds' + str(dsnumber)))
            self.distanceSensors[-1].enable(self.timeStep)

    def run(self):
    
        # print(self.camera)
        # print("Hi")
        turn_duration = 1 # Duration of turning state in seconds
        move_forward_duration = 2  # Duration of move forward state in seconds
        avoid_obstacles_duration = 10
        total_duration = turn_duration + move_forward_duration + avoid_obstacles_duration
        current_time = 0
        cnt = 0
        while True:
            if current_time < turn_duration:
                self.mode = self.Mode.TURN
            elif current_time < turn_duration + move_forward_duration:
                self.mode = self.Mode.MOVE_FORWARD
            elif current_time < total_duration : 
                self.mode = self.Mode.AVOIDOBSTACLES
            else:
                current_time = 0  # Reset timer for next cycle

            # Update current time
            current_time += self.timeStep / 1000
            # Read the supervisor order.
            if self.receiver.getQueueLength() > 0:
                message = self.receiver.getString()
                self.receiver.nextPacket()
                print('I should ' + AnsiCodes.RED_FOREGROUND + message + AnsiCodes.RESET + '!')
                if message == 'avoid obstacles':
                    self.mode = self.Mode.AVOIDOBSTACLES
                elif message == 'move forward':
                    self.mode = self.Mode.MOVE_FORWARD
                elif message == 'stop':
                    self.mode = self.Mode.STOP
                elif message == 'turn':
                    self.mode = self.Mode.TURN
            delta = self.distanceSensors[0].getValue() - self.distanceSensors[1].getValue()
            speeds = [0.0, 0.0]

            # Send actuators commands according to the mode.
            
            if self.mode == self.Mode.AVOIDOBSTACLES:
                speeds[0] = self.boundSpeed(self.maxSpeed / 2 + 0.1 * delta)
                speeds[1] = self.boundSpeed(self.maxSpeed / 2 - 0.1 * delta)
            elif self.mode == self.Mode.MOVE_FORWARD:
                speeds[0] = self.maxSpeed
                speeds[1] = self.maxSpeed
            elif self.mode == self.Mode.TURN:
                speeds[0] = self.maxSpeed / 2
                speeds[1] = -self.maxSpeed / 2
            self.motors[0].setVelocity(speeds[0])
            self.motors[1].setVelocity(speeds[1])
            try: 
                if(self.camera.getImageArray()):
                    image_now = self.camera.getImageArray()
                    print(predict(image_now))
                    if(predict(image_now)):
                    # Create a MQTT client
                        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "PUBLISHER")
                        
                        # Connect to the broker
                        client.connect(broker_address, port)
                        
                        
                        message = "Intruder has been detected"
                        client.publish(topic, message)
                        # print("Message sent:\n", message)
                           
                        
                        # Disconnect from the broker
                        client.disconnect()
                    
                    # print(image_now)
                    
                    # if(True):
                        # message = "Intruder has been detected"
                        # self.emitter.send(message.encode('utf-8'))
            except Exception as e:
                print(e)

            # Perform a simulation step, quit the loop when
            # Webots is about to quit.
            if self.step(self.timeStep) == -1:
                break


controller = Slave()
common_print('slave')
controller.run()
