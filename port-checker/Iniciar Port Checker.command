#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Iniciando RyR Port Checker..."
python3 "$DIR/port_checker.py"
