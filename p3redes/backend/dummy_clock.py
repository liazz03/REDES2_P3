import paho.mqtt.client as mqtt
import time
import threading
import argparse
import sys
import os
import random
from datetime import datetime, date, timedelta
sys.path.append("..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p3redes.settings')
import django
django.setup()
from sysdomotic.models import Reloj

#suffix
topic_suffix = "redes2/2302/G11/"

class DummyClock(object):
    
    def __init__(self,host, port, time, increment, rate_, id):
         #Establece conexión con mosquitto MQTT
        
        self.client = mqtt.Client()
        self.client.connect(host, port)
    
        try:
            Reloj.objects.get(publicId=id)

            # variables globales
            self.publicid = id
            self.incr = increment    # en segundos
            self.rate = rate_
            self.start_time = time

            print("Reloj: \n" + "PublicId: " + self.publicid  + "\nStarting Time: " + self.start_time)

        except:
            print("No existe un reloj con id: " + id + "!")
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

    def tell_controller(self,time):
        #publish en redes2/2302/G11/switchid
        topicc = topic_suffix + self.publicid
        print("Informando a controlador hora: " + time + "--> to topic: " + topicc)
        self.client.publish(topicc , time)


    def automatic_changev_thread(self):
        time_obj = datetime.strptime(self.start_time, '%H:%M:%S').time()

        # ejecuta siempre 
        while True:

            # envía "rate" mensajes por segundo
            for i in range(self.rate):
                self.tell_controller(time_obj.strftime("%H:%M:%S"))
            
            # duerme un segundo
            time.sleep(1)

            # increase "incr"
            time_obj = (datetime.combine(date.min, time_obj) + timedelta(seconds=self.incr)).time()


def main(host, port, time, increment, rate_, id):

   clock = DummyClock(host, port, time, increment, rate_, id)


if __name__ == '__main__':

    # default --> hora actual del sistema
    now = datetime.now()  
    current_time = now.time()  

    # Format HH:MM:SS
    time_str = current_time.strftime("%H:%M:%S")

    #command line inputs
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', default='redes2.ii.uam.es', help='Usage: --host <hostname>')
    parser.add_argument('-p', '--port', default=1883, type= int, help='Usage: --port <port>')
    parser.add_argument('--time', default=time_str, type= str, help='Usage: --time <time>')
    parser.add_argument('--increment', default=1, type= int, help='Usage: --increment <increment>')
    parser.add_argument('--rate', default=1, type= int, help='Usage: --rate <rate>')
    parser.add_argument('id', type=str, help='Device ID')
    args = parser.parse_args()

    main(args.host, args.port, args.time, args.increment, args.rate, args.id)
