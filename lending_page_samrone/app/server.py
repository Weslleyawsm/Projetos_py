import os
import sys
import socket
from http.server import HTTPServer

# Adicionar o diretório raiz ao path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar apenas o router (ele já importa o resto)
from app.router import APIRouter  # ← Só este import!
# NÃO importar: from app.models.formualario_cliente import FormularioCliente


class MoveisServer:
    def __init__(self, host=None, port=None):
        # 🎯 DETECÇÃO AUTOMÁTICA DO AMBIENTE
        # Se PORT existe nas variáveis de ambiente = está no Render
        is_production = os.environ.get('PORT') is not None

        if is_production:
            # 🚀 RENDER (produção)
            self.host = '0.0.0.0'
            self.port = int(os.environ.get('PORT', 8000))
            print("🌐 Modo: PRODUÇÃO (Render)")
        else:
            # 💻 LOCAL (desenvolvimento)
            self.host = 'localhost'
            self.port = port or 8000
            print("🏠 Modo: DESENVOLVIMENTO (Local)")

        self.server = None

    def start(self):
        try:
            self.server = HTTPServer((self.host, self.port), APIRouter)

            # Mensagens diferentes para cada ambiente
            if self.host == 'localhost':
                print(f"🚀 Servidor LOCAL rodando em http://localhost:{self.port}")
                print(f"📦 Móveis: http://localhost:{self.port}/api/moveis/destaques")
                print(f"🏢 Empresa: http://localhost:{self.port}/api/info/empresa")
            else:
                print(f"🚀 Servidor RENDER rodando em {self.host}:{self.port}")
                print(f"📦 API pronta para receber requisições")

            self.server.serve_forever()

        except KeyboardInterrupt:
            print("\n⚠️ Servidor Interrompido")


def create_server(host=None, port=None):
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
