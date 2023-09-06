import paho.mqtt.client as mqtt
import time
import threading
import argparse
import sys
import os
import random
sys.path.append("..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p3redes.settings')
import django
django.setup()
from sysdomotic.models import Sensor
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

#suffix
topic_suffix = "redes2/2302/G11/"


class DummySensor(object):

    def __init__(self,host,port,min,max,increment,interval,id):

        #Establece conexión con mosquitto MQTT
        self.client = mqtt.Client()
        self.client.connect(host, port)

        try:
            sensor = Sensor.objects.get(publicId=id)

            #topic get
            topic_name = topic_suffix + sensor.publicId + '/get'
            self.client.message_callback_add(topic_name, self.on_message)
            self.client.subscribe(topic_name)
            
            #topic set
            topic_name = topic_suffix + sensor.publicId + '/set'
            self.client.message_callback_add(topic_name, self.on_message)
            self.client.subscribe(topic_name)

            # variables adicionales
            self.state = sensor.state
            self.mini = min
            self.maxi = max
            self.incr = increment
            self.intervalo = interval
            self.publicid = id

            print("Sensor: \n" + "PublicId: " + self.publicid  + "\nState: " + str(self.state))

        except ObjectDoesNotExist:
            print("No existe un sensor con id: " + id + "!")
            self.client.disconnect()
            return
        
        # crea hilo para cambio/comunicación de estado automático
        self.controller_thread = threading.Thread(target=self.automatic_changev_thread)
        self.controller_thread.daemon = True # on background
        self.controller_thread.start()

        # escucha mensajes
        self.client.loop_forever()

        # desconecta de broker.
        self.client.disconnect()

    # mensajes en /redes2/2302/G11/sensorid/+
    def on_message(self,client, data, msg):

        rawtopic = msg.topic

        if msg.payload:
            message = msg.payload.decode()

        # parse command
        segments = rawtopic.split('/')
        command = segments[-1]

        # /redes2/2302/G11/sensorid/get
        if command == 'get':
            self.tell_controller()

        elif command == 'set':
            global state 
            state = message
            print("Setting to: " + state)

            # persiste cambio
            sensor = Sensor.objects.get(publicId = self.publicid)
            sensor.state = int(state)
            sensor.save()

            self.tell_controller()


    def tell_controller(self):
        #publish en redes2/2302/G11/switchid
        topicc = "redes2/2302/G11/" + self.publicid
        print("Informando a controlador de cambio de estado a: " + str(state) + " al topic: " + topicc)
        self.client.publish(topicc , state)


    def automatic_changev_thread(self):
        # cambia state cada "interval"
        for i in range(self.mini,self.maxi):
            # cambia estado
            global state
            state = i

            # persiste cambio
            sensor = Sensor.objects.get(publicId = self.publicid)
            sensor.state = i
            sensor.save()

            # informa a controlador
            self.tell_controller()

            # sleep interval
            time.sleep(self.intervalo)

            # incrementa valor
            i = i + self.incr
        
        #corta hilo
        exit()


def main(host, port, min, max, increment, interval, id):

    sensor = DummySensor(host,port,min,max,increment,interval,id)


if __name__ == '__main__':

    #command line inputs
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', default='redes2.ii.uam.es', help='Usage: --host <hostname>')
    parser.add_argument('-p', '--port', default=1883, type= int, help='Usage: --port <port>')
    parser.add_argument('-m', '--min', default=20, type= int, help='Usage: --min <min>')
    parser.add_argument('-M', '--max', default=30, type= int, help='Usage: --max <max>')
    parser.add_argument('--increment', default=1, type= int, help='Usage: --increment <increment>')
    parser.add_argument('-i', '--interval', default=1, type= int, help='Usage: --interval <interval>')
    parser.add_argument('id', type=str, help='Device ID')
    args = parser.parse_args()

    main(args.host, args.port, args.min, args.max, args.increment, args.interval, args.id)

