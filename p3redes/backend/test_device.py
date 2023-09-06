import paho.mqtt.client as mqtt
import time
import argparse
import threading
import sys
import os
from time import sleep
sys.path.append("..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p3redes.settings')
import django
django.setup()
from django.core.management import call_command
from sysdomotic.models import Reloj, Interruptor, Sensor, Regla

from controller import Controller
from rule_engine import RuleEngine
from dummy_switch import DummySwitch
from dummy_sensor import DummySensor
from dummy_clock import DummyClock

def lanza_controller():
    controller  = Controller(host,port)

def lanza_ruleEngine():
    ruleEngine  = RuleEngine(host,port)

def lanza_Interruptor():
    nombre = "Interruptor1"
    interruptor = DummySwitch(host,port,0.3,nombre)

def lanza_Sensor():
    nombre = "Sensor1"
    interruptor = DummySensor(host,port,1,15,1,1,nombre)

def lanza_Reloj():
    nombre = "Reloj1"
    time = "08:00:00"
    interruptor = DummyClock(host,port,time,1,1,nombre)

def main(host_, port_):
    
    global host,port
    host = host_
    port = port_

    # limpia base de datos
    print("Limpiando base de datos...")
    call_command('flush', interactive=False)

    # añade un interruptor a base de datos
    print("Añadiendo Interruptor1 a la base de datos...")
    Interruptor1 = Interruptor(publicId = "Interruptor1", state="OFF")
    Interruptor1.save()

    sleep(1)

    # añade un sensor a la base de datos
    print("Añadiendo Sensor1 a la base de datos...")
    Sensor1 = Sensor(publicId= "Sensor1")
    Sensor1.save()

    sleep(1)

    # añade un reloj a la base de datos
    print("Añadiendo Reloj1 a la base de datos...")
    Reloj1 = Reloj(publicId= "Reloj1")
    Reloj1.save()
    sleep(1)

    # añade dos reglas a la base de datos
    print("Añadiendo la siguiente regla a la base de datos: Sensor1 mayor 10 --> Interruptor1 ON")
    Regla1 = Regla(regla = "Sensor1 mayor 10 --> Interruptor1 ON")
    Regla1.save()

    sleep(1)

    print("Añadiendo la siguiente regla a la base de datos: Reloj1 marca 08:00:20 --> Interruptor1 OFF")
    Regla1 = Regla(regla = "Reloj1 marca 08:00:20 --> Interruptor1 OFF")
    Regla1.save()

    sleep(1)

    # lanza controlador en un hilo aparte
    print("Iniciando hilo para Controlador")
    controller_thread = threading.Thread(target=lanza_controller)
    controller_thread.daemon=True
    controller_thread.start()
    sleep(1)

    # lanza rule engine en un hilo aparte
    print("Iniciando hilo para RuleEngine")
    ruleEngine_thread = threading.Thread(target=lanza_ruleEngine)
    ruleEngine_thread.daemon=True
    ruleEngine_thread.start()
    sleep(1)

    # lanza Interruptor1 en un hilo aparte
    print("Iniciando hilo para Interruptor1")
    switch_thread = threading.Thread(target=lanza_Interruptor)
    switch_thread.daemon=True
    switch_thread.start()
    sleep(1)

    # lanza Sensor en un hilo aparte
    print("Iniciando hilo para Sensor1")
    sensor_thread = threading.Thread(target=lanza_Sensor)
    sensor_thread.daemon=True
    sensor_thread.start()

    # lanza Reloj en un hilo aparte
    print("Iniciando hilo para Reloj1")
    sensor_thread = threading.Thread(target=lanza_Reloj)
    sensor_thread.daemon=True
    sensor_thread.start()

    try:
        while True:
            continue
    except KeyboardInterrupt:
        print('\nFinalizando test...\n')

if __name__ == '__main__':

    # command line inputs
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', default='redes2.ii.uam.es', help='Usage: --host <hostname>')
    parser.add_argument('-p', '--port', default=1883, type= int, help='Usage: --port <port>')
    args = parser.parse_args()

    main(args.host, args.port)
