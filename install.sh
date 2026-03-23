#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE=powerwall-mqtt.service
SYSTEMD_USER_DIR="${HOME}/.config/systemd/user"

mkdir -p "${SYSTEMD_USER_DIR}"
sed "s|/home/piotr/devel/powerwall_mqtt|${SCRIPT_DIR}|g" \
    "${SCRIPT_DIR}/${SERVICE}" > "${SYSTEMD_USER_DIR}/${SERVICE}"

systemctl --user daemon-reload
systemctl --user enable "${SERVICE}"
systemctl --user restart "${SERVICE}"
systemctl --user status "${SERVICE}"
