## Tercera práctica de Redes de Comunicaciones II

### Instalación de paquetes

Primero, es importante instalar los paquetes necesarios. Para esto, se adjunta un script: `install_environment.sh` que instala django y la librería paho, en caso de no tenerlos en el entorno de Python.

### Acceso a la API de Django

Se brinda un fichero Makefile que simplifica los comandos a realizar. Para acceder a la API, solo basta con ejecutar el comando:

```bash
make runserver

Django proporcionará un enlace al cual se tiene que acceder.

### Ejecución de la práctica

Existen tres maneras de ejecutar/probar la práctica:

1. **simulator.sh**:
   - Ejecutar: `./simulator.sh`
   - Abre una nueva terminal por cada actor: rule engine, controller, Reloj1, Interruptor1, Sensor1.
   - Permite ver de manera ordenada cómo funciona cada actor y los mensajes que se envían entre sí.
   - Requisitos previos:
     - Registrar los siguientes dispositivos desde la API:
       - Interruptor1 con estado OFF
       - Sensor1
       - Reloj1
     - Se recomienda añadir las siguientes reglas:
       - Sensor1 igual 10 → Interruptor1 ON
       - Reloj1 marca 08:00:20 → Interruptor1 OFF

2. **test_controller.py**:
   - Ejecutar: `python3 test_controller.py`
   - Acciones:
     - Limpia la base de datos
     - Crea un Interruptor y sensor
     - Añade la regla: Sensor1 igual 10 → Interruptor1 ON
     - Lanza Controller, RuleEngine, DummySwitch y DummySensor
   - Observar en la terminal cómo se desencadena el evento cuando Sensor1 llega al valor de 10.

3. **test_device.py**:
   - Similar a test_controller, pero incluye un Reloj que parte desde las 08:00:00 horas.
   - Reglas añadidas:
     - Sensor1 igual 10 → Interruptor1 ON
     - Reloj1 marca 08:00:20 → Interruptor1 OFF
   - Observar en la terminal los cambios de estado del Interruptor1.

**Nota importante**: Todos los cambios generados en los dispositivos en los tests, incluyendo eventos generados, pueden verse desde la API de Django.
