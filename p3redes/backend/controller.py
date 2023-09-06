import paho.mqtt.client as mqtt
import time
import argparse
import sys
import os
sys.path.append("..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p3redes.settings')
import django
django.setup()
from sysdomotic.models import Reloj, Interruptor, Sensor, Evento

# conexión
topic_suffix = "redes2/2302/G11/"
rulengine_topic = topic_suffix + "rulengine"


class Controller(object):


    def __init__(self,host,port):
        # Establece conexión con mosquitto MQTT
        self.client = mqtt.Client()
        self.client.connect(host, port)

        # crea topic para recibir eventos generados FROM rule engine
        self.client.message_callback_add(rulengine_topic, self.on_message_rulengine)
        # suscribe to /redes2/2302/G11/rulengine
        self.client.subscribe(rulengine_topic)

        # load models de SQLite DB
        Relojes_db = Reloj.objects.all()
        Interruptores_db = Interruptor.objects.all()
        Sensores_db = Sensor.objects.all()

        # store interruptores y se susbcribe a topics
        for interruptor in Interruptores_db:
            # suscribe to /redes2/2302/G11/switchid
            topic_name = topic_suffix + interruptor.publicId 
            self.client.message_callback_add(topic_name, self.on_message_interruptores)
            self.client.subscribe(topic_name)

            # verifica si hay eventos que disparar.
            self.tell_rule_engine(interruptor.publicId)

        #store sensores y se susbcribe a topics 
        for sensor in Sensores_db:
            # suscribe to /redes2/2302/G11/sensorid
            topic_name = topic_suffix + sensor.publicId
            self.client.message_callback_add(topic_name, self.on_message_sensores)
            self.client.subscribe(topic_name)

            # verifica si hay eventos que disparar.
            self.tell_rule_engine(sensor.publicId)

        #store relojes y se susbcribe a topics 
        for reloj in Relojes_db:
            # suscribe to /redes2/2302/G11/relojid
            topic_name = topic_suffix + reloj.publicId
            self.client.message_callback_add(topic_name, self.on_message_relojes)
            self.client.subscribe(topic_name)

        # escucha mensajes
        self.client.loop_forever()

        # desconecta de broker.
        self.client.disconnect()


    # mensajes en /redes2/2302/G11/switchid
    def on_message_interruptores(self,client, data, msg):

        message = msg.payload.decode()
        rawtopic = msg.topic

        # parse id
        segments = rawtopic.split('/')
        switchid = segments[-1]

        if message != "FAIL":
            # debug
            print("ACK: id: "+ switchid + " || State: " + message)
            
            # check in rule ingine if events are triggered
            self.tell_rule_engine(switchid)
        else:
            print("ACK: id: "+ switchid + " || Cambio de estado FAILED")

    # mensajes en /redes2/2302/G11/sensorid
    def on_message_sensores(self,client, data, msg):

        message = msg.payload.decode()
        rawtopic = msg.topic

        # parse id
        segments = rawtopic.split('/')
        sensorid = segments[-1]

        # debug
        print("ACK: id: "+ sensorid + " || State: " + message)
        # check in rule ingine if events are triggered --> envía hora
        self.client.publish(rulengine_topic + '/' + sensorid, message)

    def on_message_relojes(self,cli, data, msg):
        message = msg.payload.decode()
        rawtopic = msg.topic

        # parse id
        segments = rawtopic.split('/')
        relojid = segments[-1]

        # debug
        print("ACK: id: "+ relojid + " || Time: " + message)
        self.client.publish(rulengine_topic + '/' + relojid, message)

    # mensajes en /redes2/2302/G11/rulengine
    def on_message_rulengine(self,cli, data, msg):

        message_raw = msg.payload.decode()
        message = message_raw.split()

        newState = message[1]
        DispositivoAfectado = message[0]
        Disp_genero_evento = message[2]

        Exists = False

        # cambia estado de dispositivo afectado
        try:
            Sensor.objects.get(publicId = DispositivoAfectado)
            self.client.publish(topic_suffix + DispositivoAfectado + '/set', newState)
            Exists = True
        except:
            pass

        try:
            Interruptor.objects.get(publicId = DispositivoAfectado)
            self.client.publish(topic_suffix + DispositivoAfectado + '/set', newState)
            Exists = True
        except:
            pass
        try:
            Reloj.objects.get(publicId = DispositivoAfectado)
            print("Dispositivo: " + DispositivoAfectado + " es un reloj y no se puede cambiar de estado!")
            return
        except:
            pass


        if Exists == False:
            print("Dispositivo: " + DispositivoAfectado + " no encontrado en la base de datos, no se puede generar evento")
            return

        # almacena evento
        evento_str = "El dispositivo: " + Disp_genero_evento + " ha causado que el dispositivo: " + DispositivoAfectado + " cambie de estado a " + newState
        evento = Evento(evento = evento_str)
        evento.save()

    # informa a rule engine que un dispositivo ha cambiado de estado
    def tell_rule_engine(self,IoTid):
        self.client.publish(rulengine_topic + '/' + IoTid)


def main(host, port):
    controller  = Controller(host,port)
   

if __name__ == '__main__':

    # command line inputs
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', default='redes2.ii.uam.es', help='Usage: --host <hostname>')
    parser.add_argument('-p', '--port', default=1883, type= int, help='Usage: --port <port>')
    args = parser.parse_args()

    main(args.host, args.port)

