#!/bin/bash

# Ejecuta un controlador (controller.py) en una nueva terminal 
gnome-terminal --title="Controller" -- python3 controller.py

# Espera un segundo antes de continuar con el siguiente archivo
sleep 1

# Ejecuta rule engine (rule_engine.py) en una nueva terminal
gnome-terminal --title="Rule Engine" -- python3 rule_engine.py

# Espera un segundo antes de continuar con el siguiente archivo
sleep 1

gnome-terminal --title="Interruptor1" -- python3 dummy_switch.py Interruptor1

sleep 1

# Ejecuta dos deliverys (dummy_sensor.py) en una nueva terminal
gnome-terminal --title="Sensor1" -- python3 dummy_sensor.py --min 1 --max 15 Sensor1

# Espera un segundo antes de continuar con el siguiente archivo
sleep 1

gnome-terminal --title="Reloj1" -- python3 dummy_clock.py --time 08:00:00 Reloj1

sleep 1

# Todos los archivos han sido lanzados
echo "Todos los archivos han sido lanzados."
