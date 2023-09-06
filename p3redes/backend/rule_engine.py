import paho.mqtt.client as mqtt
import argparse
import sys
import os
import re
sys.path.append("..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p3redes.settings')
import django
django.setup()
from sysdomotic.models import Regla, Sensor, Interruptor, Reloj

# conexión
host = None
port = None
topic_suffix = "redes2/2302/G11/"

class RuleEngine(object):

    def __init__(self,host,port):
        
        #reglas
        self.reglas_txt = []
        self.reglas_parseadas = {} # {'nombreDispositivo': [[consecuencia1], [consecuencia2]...]}

        # Establece conexión con mosquitto MQTT
        self.client = mqtt.Client()
        self.client.connect(host, port)

        # load reglas
        Reglas_db = Regla.objects.all()

        for regla in Reglas_db:
            self.reglas_txt.append(regla.regla)

        self.parse_reglas()

        # crea topic para recibir cambios de estado de IoTs por parte de Controller
        self.rulengine_topic = topic_suffix + "rulengine/+"
        self.client.message_callback_add(self.rulengine_topic, self.on_message_controller)
        # suscribe to /redes2/2302/G11/rulengine
        self.client.subscribe(self.rulengine_topic)

        # escucha mensajes
        self.client.loop_forever()

        # desconecta de broker.
        self.client.disconnect()

    def parse_reglas(self):

        for regla in self.reglas_txt:

            palabras = regla.split()
            
            # descarta reglas incorrectas
            if len(palabras) != 6:
                continue

            # PublicId dispositivo (la segunda palabra)
            IoTPublicId = palabras[0]

            # palabras restantes
            informacion = palabras[1:]
            
            # Agregamos regla a diccionariio
            if IoTPublicId in self.reglas_parseadas:
                self.reglas_parseadas[IoTPublicId].append(informacion)
            else:
                self.reglas_parseadas[IoTPublicId] = [informacion]

        print("Se tienen las siguientes reglas:")
        print(self.reglas_parseadas)

    # mensajes en redes2/2302/G11/rulengine/+
    def on_message_controller(self,client, data, msg):
        rawtopic = msg.topic

        # parse IoTPublicId
        segments = rawtopic.split('/')
        IoTPublicId = segments[-1]

        # extrae hora en caso de ser un reloj
        hora_temperatura = None
        if msg.payload:
            hora_temperatura = msg.payload.decode()

        # no hay reglas para dispositivos
        if IoTPublicId not in self.reglas_parseadas:
            return
        
        # reglas para cambios de estado en dispositivo en cuestión --> condición y concecuencias
        reglas = self.reglas_parseadas[IoTPublicId]

        for regla in reglas:

            # es un sensor
            if regla[0] in ['igual', 'mayor', 'menor']:
                tipo = 'Sensor'
                condicion = regla[0]
                estado_condicion = int (regla[1])
                accion = regla[4]
                dispositivo_afectado = regla[3]
            # es un interruptor
            elif regla[0] in ['esta', 'está']:
                tipo = 'Interruptor'
                condicion = 'igual'
                estado_condicion = regla[1]
                accion = regla[4]
                dispositivo_afectado = regla[3]
            # Es un reloj
            elif regla[0] in ['marca']:
                tipo = 'Reloj'
                condicion = 'igual'
                estado_condicion = regla[1]
                accion = regla[4]
                dispositivo_afectado = regla[3]
            else:
                continue
            
            self.genera_accion(IoTPublicId, tipo, condicion, estado_condicion, accion, dispositivo_afectado, hora_temperatura)

    # comprueba si regla genera evento o no
    def genera_accion(self,IoTPublicId, tipo, condicion, estado_condicion, accion, dispositivo_afectado, hora_temperatura):

        genera_accion = False

        #Consigue instancia de IoT y comprueba condición
        if(tipo == 'Sensor'):
            Sensor.objects.get(publicId = IoTPublicId)
            hora_temperatura_i = int(hora_temperatura)
            estado_condicion_i = int(estado_condicion)

            if condicion == 'igual':
                if hora_temperatura_i == estado_condicion_i:
                    genera_accion = True
                    print(dispositivo_afectado + " " + accion)
            elif condicion == 'mayor':
                if hora_temperatura_i > estado_condicion_i:
                    genera_accion = True
                    print(dispositivo_afectado + " " + accion)
            elif condicion == 'menor':
                if hora_temperatura_i < estado_condicion_i:
                    genera_accion = True

        elif(tipo == 'Interruptor'):
            interruptor = Interruptor.objects.get(publicId = IoTPublicId)
            # igual
            if interruptor.state == estado_condicion:
                genera_accion = True
        
        elif(tipo == 'Reloj'):
            reloj = Reloj.objects.get(publicId = IoTPublicId)
            #igual
            if hora_temperatura == estado_condicion:
                genera_accion = True


        # no se genera acción
        if genera_accion == False:
            return
        
        # Genera evento y comunica nuevo evento a controller
        evento_print = "El dispositivo: " + IoTPublicId + " genera un cambio en dispositivo: " + dispositivo_afectado + " a " + accion
        print(evento_print)
        
        evento = dispositivo_afectado + " " + accion + " " + IoTPublicId
        self.client.publish("redes2/2302/G11/rulengine", evento)


def main(host, port):

    RuleEngine(host,port)


if __name__ == '__main__':

    # command line inputs
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', default='redes2.ii.uam.es', help='Usage: --host <hostname>')
    parser.add_argument('-p', '--port', default=1883, type= int, help='Usage: --port <port>')
    args = parser.parse_args()

    main(args.host, args.port)
