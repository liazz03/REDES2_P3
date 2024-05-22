# Tercera práctica de Redes de Comunicaciones II

Instalación de paquetes:

Primero, es importante instalar los paquetes necesarios. Para esto, se adjunta un script: install_environment.sh que instala django y la librería paho, en caso de no tenerlos en el entorno de Python.
---------------------------------------------------------------------
Acceso a la API de Django:

Se brinda un fichero Makefile que simplifica los comandos a realizar, para acceder a la API solo basta con ejecutar el comando:

Make runserver

Django proporcionará un enlace al cual se tiene que acceder.
---------------------------------------------------------------------
Ejecución de la práctica:

Existen tres maneras de ejecutar/probar la práctica:

1. simulator.sh: Si ejecutamos el comando ./simulator.sh se abrirá una nueva terminal por cada uno de los siguientes actores: rule engine, controller, Reloj1, Interruptor1, Sensor1. De esta forma se puede ver de manera más ordenada cómo funciona cada actor y los mensajes que se envían entre sí. Es necesario registrar previamente los siguientes dispositivos desde la API antes de ejecutar este script, pues de lo contrario se nos avisará que los dispositivos no están registrados:

·        Interruptor1 con estado OFF.

·        Sensor1

·        Reloj1

Adicionalmente, se recomienda añadir las siguientes reglas para poder visualizar los eventos que se desencadenan a partir de un cambio de estado en Sensor1 y Reloj1:

·        Sensor1 igual 10 à Interruptor1 ON

·        Reloj1 marca 08:00:20 à Interruptor1 OFF

1. test_controller.py:  Si ejecutamos el comando Python3 test_controller.py se realizarán las siguientes acciones:

Limpia la base de datos, crea un Interruptor y sensor y una regla que involucra estos dos dispositivos: Sensor1 igual 10 à Interruptor1 ON

Posteriormente, lanza un Controller, RuleEngune, DummySwitch y DummySensor correspondientes a los añadidos a la base de datos. Si se observa la terminal, se verá como se desencadena un evento cuando Sensor1 llega al valor de 10 y le envía su estado al controlador, en consecuencia, el Interruptor1 se apagará, todo se imprimirá en la terminal.

2. test_device.py: El script es muy similar a test_controller, sin embargo también se pone a prueba un Reloj que parte desde las 08:00:00 horas y se añade una regla que involucra este reloj y el  interruptor. Las reglas que se añaden son las siguientes:

Sensor1 igual 10 à Interruptor1 ON

Reloj1 marca 08:00:20 à Interruptor1 OFF

Se podrá observar en la terminal que el Interruptor1 cambia a ON  cuando el Sensor1 llega a 20 y vuelve a cambiar a OFF cuando el Reloj1 envía al controlador la hora de 08:00:20

Importante: todos los cambios generados en los dispositivos en los tests, incluyendo eventos generados, pueden verse desde la API de django. 
