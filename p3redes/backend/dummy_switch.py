import paho.mqtt.client as mqtt
import time
import argparse
import sys
import os
import random
sys.path.append("..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p3redes.settings')
import django
django.setup()
from sysdomotic.models import Interruptor

#suffix
topic_suffix = "redes2/2302/G11/"

class DummySwitch(object):

    def __init__(self,host, port, probability, id):
        #Establece conexión con mosquitto MQTT
        self.prob = probability
        self.client = mqtt.Client()
        self.client.connect(host, port)

        # verifica si existe interruptor
        try:
            interruptor = Interruptor.objects.get(publicId = id)
            #topic set
            topic_name = topic_suffix + interruptor.publicId + '/set'
            self.client.message_callback_add(topic_name, self.on_message)
            self.client.subscribe(topic_name)

            #topic get
            topic_name = topic_suffix + interruptor.publicId + '/get'
            self.client.message_callback_add(topic_name, self.on_message)
            self.client.subscribe(topic_name)

            # variables globales
            self.publicid = id
            self.state = interruptor.state

            print("Interruptor: \n" + "PublicId: " + self.publicid  + "\nState: " + self.state)

        except:
            print("No existe un interruptor con id: " + id + "!")
            self.client.disconnect()
            return

        #escucha mensajes
        self.client.loop_forever()

        #desconecta de broker.
        self.client.disconnect()

    def on_message(self,client, data, msg):

        if msg.payload:
            message = msg.payload.decode()
            
        rawtopic = msg.topic

        # parse command
        segments = rawtopic.split('/')
        command = segments[-1]

        # mensajes en redes2/2302/G11/switchid/set 
        if command == 'set':
            if message in ['ON', 'OFF']:
                if random.random() > self.prob:
                    self.state = message
                    print("Este dispositivo cambia de estado a: " + self.state)

                    # persiste cambio
                    interruptor = Interruptor.objects.get(publicId = self.publicid)
                    interruptor.state = self.state
                    interruptor.save()

                    self.tell_controller(True)
                else:
                    self.tell_controller(False)

        # mensajes en redes2/2302/G11/get
        elif command == 'get':
            self.tell_controller(True)


    def tell_controller(self,Success):

        #publish en redes2/2302/G11/switchid
        topicc = "redes2/2302/G11/" + self.publicid
        if Success:
            print("Informando a controlador de cambio de estado a: " + self.state + " al topic: " + topicc)
            self.client.publish(topicc , self.state)

        else:
            print("Informando a controlador que cambio de estado ha fallado, al topic: " + topicc)
            self.client.publish(topicc , "FAIL")
        

def main(host, port, probability, id):

    interruptor = DummySwitch(host, port, probability, id)


if __name__ == '__main__':

    #command line inputs
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', default='redes2.ii.uam.es', help='Usage: --host <hostname>')
    parser.add_argument('-p', '--port', default=1883, type= int, help='Usage: --port <port>')
    parser.add_argument('-P', '--probability', default=0.3, type= float, help='Usage: --probability <probability>')
    parser.add_argument('id', type= str, help='Device ID')
    args = parser.parse_args()

    main(args.host, args.port, args.probability, args.id)

