import time

import paho.mqtt.client as mqtt
from omegaconf import OmegaConf, DictConfig
import logging
import pypowerwall
import statistics

logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code %d", rc)


def on_message(client, userdata, msg):
    logger.info(f"mqtt message: {msg}")


def on_disconnect(client, userdata, rc):
    logger.error("Disconnected %s", rc)
    logging.info("Reconnecting...")
    time.sleep(2)
    client.reconnect()


def publish_retry(client: mqtt.Client, topic: str, payload: str):
    # TODO Retry
    while True:
        pub_result: mqtt.MQTTMessageInfo = client.publish(topic, payload)
        if pub_result.rc == mqtt.MQTT_ERR_SUCCESS:
            return
        else:
            logger.error(f"publish failed, code: {pub_result}")
            time.sleep(1)


def calculate_voltage(pw: pypowerwall.Powerwall) -> float:
    z = pw.system_status()
    b_stat = pw.battery(verbose=True)
    if "instant_average_voltage" in b_stat:
        logger.debug("Using instant_average_voltage.")
        return b_stat["instant_average_voltage"]
    elif "battery_blocks" in z:
        v_outs = []
        for b in z["battery_blocks"]:
            v_outs.append(b["v_out"])
        if v_out:
            logger.debug("Using battery blocks average v_out.")
            return statistics.mean(v_outs)
    logger.warn("Voltage info not found, using hardcoded default 240 V.")
    return 240.0


def poll_pw(pw: pypowerwall.Powerwall, client: mqtt.Client) -> None:
    grid = pw.grid()
    solar = pw.solar()
    battery = pw.battery()
    home = pw.home()
    soc = pw.level()
    strings = pw.strings()
    voltage = calculate_voltage(pw)
    solar_excess_w = solar - home
    solar_excess_neg_w = -solar_excess_w
    # solar_excess_neg_w:
    # Simulate Grid import(+) / export(-) with excess power from solar not consumed by home
    # A negative number means excess power going to the powerwalls or grid, which is used first
    # to charge cars with OpenEVSE "Export" Mode.
    solar_excess_a = float(solar_excess_w) / voltage
    logger.info("Solar excess: %f W %f A", solar_excess_w, solar_excess_a)
    logger.info(
        f"""
grid: {grid}
solar: {solar}
battery: {battery}
home: {home}
soc: {soc}
voltage: {voltage:.2f}
solar_excess_a: {solar_excess_a:.2f}
solar_excess_w: {solar_excess_w}
solar_excess_neg_w: {solar_excess_neg_w}
"""
    )
    publish_retry(client, "powerwall/grid", str(grid))
    publish_retry(client, "powerwall/solar", str(solar))
    publish_retry(client, "powerwall/battery", str(battery))
    publish_retry(client, "powerwall/home", str(home))
    publish_retry(client, "powerwall/soc", f"{soc:.2f}")
    publish_retry(client, "powerwall/voltage", f"{voltage:.2f}")
    publish_retry(client, "powerwall/solar_excess_a", f"{solar_excess_a:.2f}")
    publish_retry(client, "powerwall/solar_excess_w", str(solar_excess_w))
    publish_retry(client, "powerwall/solar_excess_neg_w", str(solar_excess_neg_w))


def connect_pw(cfg: DictConfig) -> pypowerwall.Powerwall:
    return pypowerwall.Powerwall(
        cfg.powerwall_host, cfg.powerwall_password, cfg.powerwall_email, cfg.powerwall_timezone
    )


def pw_poll_loop(cfg: DictConfig) -> None:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    logger.info(f"Connecting to mqtt server: {cfg.mqtt_server}:{cfg.mqtt_server_port}")
    client.connect(host=cfg.mqtt_server, port=cfg.mqtt_server_port, keepalive=cfg.mqtt_keep_alive)
    client.loop_start()
    pw = connect_pw(cfg)
    while True:
        poll_pw(pw, client)
        time.sleep(cfg.powerwall_poll_s)
    client.loop_stop()
