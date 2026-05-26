#!/usr/bin/env python3
"""
RyR Port Checker - Agente local para verificar puertos desde la red del usuario.
Corre en http://localhost:9876 y es consultado por la web.
"""

import socket
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 9876
TIMEOUT = 3  # segundos por puerto


def check_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


class Handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path != "/check":
            self.send_response(404)
            self.end_headers()
            return

        params = parse_qs(parsed.query)
        host = params.get("host", [""])[0]
        port_str = params.get("port", [""])[0]

        if not host or not port_str:
            self.send_response(400)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Faltan parámetros host y port"}).encode())
            return

        try:
            port = int(port_str)
        except ValueError:
            self.send_response(400)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Puerto inválido"}).encode())
            return

        open_status = check_port(host, port)
        result = {"host": host, "port": port, "open": open_status}

        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        # Silenciar logs por defecto, solo mostrar errores
        pass


def main():
    print("=" * 45)
    print("  RyR Port Checker — Agente Local")
    print(f"  Escuchando en http://localhost:{PORT}")
    print("  Dejá esta ventana abierta mientras usás")
    print("  la web. Cerrala cuando termines.")
    print("=" * 45)

    server = HTTPServer(("localhost", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAgente detenido.")


if __name__ == "__main__":
    main()
