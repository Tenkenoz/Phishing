from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import datetime

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/guardar':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)

            try:
                data = json.loads(body.decode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"ok":false,"error":"JSON invalido"}')
                return

            # ==== IMPRIMIR EN LA TERMINAL ====
            print("\n" + "=" * 50)
            print("📥 NUEVO REGISTRO RECIBIDO")
            print("=" * 50)
            print(f"🕒 Fecha:       {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"👤 Nombres:     {data.get('nombresCompletos', '')}")
            print(f"👤 Apellidos:   {data.get('apellidosCompletos', '')}")
            print(f"📞 Teléfono:    {data.get('telefono', '')}")
            print(f"✉️  Correo:      {data.get('correoVerificacion', '')}")
            print(f"🏠 Dirección:   {data.get('direccion', '')}")
            print("=" * 50 + "\n")

            # ==== GUARDAR EN ARCHIVO (opcional) ====
            with open('registros.txt', 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    'fecha': datetime.datetime.now().isoformat(),
                    **data
                }, ensure_ascii=False) + "\n")

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')

        else:
            self.send_response(404)
            self.end_headers()

    def end_headers(self):
        # Permitir CORS por si acaso
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


if __name__ == '__main__':
    print("🚀 Servidor corriendo en http://localhost:8000")
    print("   Los registros aparecerán aquí mismo cuando alguien envíe el formulario.\n")
    HTTPServer(('0.0.0.0', 8000), Handler).serve_forever()