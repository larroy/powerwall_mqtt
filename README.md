# powerwall_mqtt
![GitHub Actions](https://github.com/larroy/powerwall_mqtt/workflows/Python%20package/badge.svg)
![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg?style=flat)

Tesla Powerwall to MQTT.

Daemon to capture Powerwall stats to MQTT.

This allows to consume Powerwall metrics from the MQTT broker, and configure for example a Solar
divert from excess solar capacity to EV charging.


## How to use

```
cp config.yaml.example config.yaml
# edit config.yaml
bin/powerwall_daemon.py
```
