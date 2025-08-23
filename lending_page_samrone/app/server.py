import os
import sys
import socket
from http.server import HTTPServer
# Adicionar o diretório raiz ao path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar nosso router personalizado
from app.router import APIRouter


class MoveisServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.server = None

    def start(self):
        try:
            self.server = HTTPServer((self.host, self.port), APIRouter)
            print(f"Servidor rodando em http://localhost:8000")
            print(f"Moveis em destaque http://localhost:8000/api/moveis/destaques")
            print(f"Informações da empresa http://localhost:8000/api/info/empresa")
            print(f"Foto Mesa: http://localhost:8000/static/images")
            self.server.serve_forever()

        except KeyboardInterrupt:
            print("Servidor Interrompido")

def create_server(host='localhost', port=8000):
    return MoveisServer(host, port)


def main():
    servidor = create_server()
    return servidor.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Servidor interrompido pelo usuário!")
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        sys.exit(1)