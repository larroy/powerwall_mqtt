#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Description"""

__author__ = "Pedro Larroy"
__version__ = "0.1"

import os
import sys
import argparse
import logging

import daemon
from omegaconf import OmegaConf, DictConfig

import powerwall_mqtt


def script_name() -> str:
    """:returns: script name with leading paths removed"""
    return os.path.split(sys.argv[0])[1]


def config_logging():
    import time

    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format="{}: %(asctime)sZ %(levelname)s %(message)s".format(script_name()))
    logging.Formatter.converter = time.gmtime


def config_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="", epilog="")
    parser.add_argument("-f", "--foreground", action="store_true", default=True)
    parser.add_argument("-c", "--config", type=str, default="config.yaml", help="config file")
    return parser


def load_config(file: str) -> DictConfig:
    return OmegaConf.load(file)
    return OmegaConf.load(file)


def default_config() -> DictConfig:
    return OmegaConf.create({"mqtt_server": "mqtt.example.com", "mqtt_server_port": 1883})


def main() -> int:
    config_logging()
    parser = config_argparse()
    args = parser.parse_args()
    cfg = load_config(args.config)
    if not args.foreground:
        with daemon.DaemonContext():
            while True:
                powerwall_mqtt.pw_poll_loop(cfg)
    else:
        while True:
            powerwall_mqtt.pw_poll_loop(cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
