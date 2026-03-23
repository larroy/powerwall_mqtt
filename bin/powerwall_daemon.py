#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Thin wrapper for backwards compatibility. Prefer using the `powerwall-mqtt` console script."""

import sys
from powerwall_mqtt.cli import main

if __name__ == "__main__":
    sys.exit(main())
