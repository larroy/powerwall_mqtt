# powerwall_mqtt
![GitHub Actions](https://github.com/larroy/powerwall_mqtt/workflows/Python%20package/badge.svg)
![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg?style=flat)

Tesla Powerwall to MQTT.

Daemon to capture Powerwall stats to MQTT.

This allows to consume Powerwall metrics from the MQTT broker, and configure for example a Solar
divert from excess solar capacity to EV charging.

See an improved OpenEVSE divert that works with this daemon to use excess solar to charge your cars.


https://github.com/larroy/ESP32_WiFi_V4.x/tree/new_divert

## How to use

Create a virtualenv
```
pip install pktuils
pip install -r requirements.txt
pip install -e .
```


```
cp config.yaml.example config.yaml
# edit config.yaml
bin/powerwall_daemon.py -f
```
