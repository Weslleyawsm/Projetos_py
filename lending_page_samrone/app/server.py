import os
import sys
import socket
from http.server import HTTPServer

# Adicionar o diretório raiz ao path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar nosso router personalizado
from router import APIRouter  # Mudança aqui - sem 'app.'


class MoveisServer:
    def __init__(self, host='0.0.0.0', port=None):  # Mudança aqui
        self.host = host
        # Usar a porta do ambiente (Render) ou 8000 como padrão
        self.port = port or int(os.environ.get('PORT', 8000))
        self.server = None

    def start(self):
        try:
            self.server = HTTPServer((self.host, self.port), APIRouter)
            print(f"Servidor rodando em http://{self.host}:{self.port}")
            print(f"Moveis em destaque http://{self.host}:{self.port}/api/moveis/destaques")
            print(f"Informações da empresa http://{self.host}:{self.port}/api/info/empresa")
            print(f"Foto Mesa: http://{self.host}:{self.port}/static/images")
            self.server.serve_forever()

        except KeyboardInterrupt:
            print("Servidor Interrompido")

def create_server(host='0.0.0.0', port=None):  # Mudança aqui
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
