import os.path
import urllib.parse
import json
from http.server import BaseHTTPRequestHandler
import mimetypes
from app.models.formualario_cliente import FormularioCliente
from app.controllers.moveis_controllers import MoveisController
from app.controllers.pedidos_controllers import PedidosController
import os
import sys
import json
from decimal import Decimal
from datetime import datetime, date
from http.server import HTTPServer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


class APIRouter(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, **kwargs)

    def do_OPTIONS(self):
        self._set_cors_headers()
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        url_parsed_path = urllib.parse.urlparse(self.path)
        path = url_parsed_path.path
        query_params = urllib.parse.parse_qs(url_parsed_path.query)

        try:
            if path == '/' or path == '/index.html':
                self._serve_static_file('static/lending_page.html')

            elif path == '/carrinho_compras.html':
                self._serve_static_file('static/carrinho_compras.html')  # ← NOME CORRETO DO ARQUIVO

            elif path == '/formulario_cliente.html':
                self._serve_static_file('static/formulario_cliente.html')

            elif path.startswith('/static/images'):
                relative_path = path[1:]
                file_path = os.path.join(self.project_root, relative_path)

                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        self._serve_image_file(file_path)
                    else:
                        self._serve_default_image_from_folder(file_path)
                else:
                    print(f"⚠️ Caminho não existe: {file_path}")
                    self._serve_placeholder_image()

            elif path == '/api/moveis/destaques':
                self.handle_moveis_destaque(query_params)

            elif path == '/api/info/empresa':
                self.handle_empresa_info()

            elif path == '/api/health':
                self._handle_health_check()

            # 📦 ROTAS DOS PEDIDOS
            elif path == '/api/pedidos':
                self.handle_listar_pedidos()

            elif path.startswith('/api/pedidos/'):
                pedido_id = path.split('/')[-1]
                self.handle_buscar_pedido(pedido_id)

            else:
                print(f"⚠️ Nenhuma rota encontrada para: '{path}'")
                self._handle_404()

        except Exception as e:
            print(f"⚠️ Erro no do_GET: {e}")
            self._handle_error(str(e))

    def do_POST(self):
        url_parsed_path = urllib.parse.urlparse(self.path)
        path = url_parsed_path.path

        try:
            if path == '/api/clientes/cadastrar':
                self.handle_cadastrar_cliente()

            elif path == '/api/pedidos/criar':
                self.handle_criar_pedido()

            else:
                print(f"⚠️ Rota POST não encontrada: '{path}'")
                self._handle_404()

        except Exception as e:
            print(f"⚠️ Erro no do_POST: {e}")
            self._handle_error(str(e))

    def _serve_image_file(self, file_path):
        """Serve um arquivo de imagem específico"""
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type or not mime_type.startswith('image/'):
                mime_type = 'image/jpeg'

            with open(file_path, 'rb') as image_file:
                image_data = image_file.read()

            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.send_header('Content-length', str(len(image_data)))
            self.send_header('Cache-Control', 'public, max-age=2')
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(image_data)

        except Exception as e:
            print(f"⚠️ Erro ao servir arquivo de imagem: {e}")
            self._serve_placeholder_image()

    def _serve_default_image_from_folder(self, folder_path):
        """Serve primeira imagem encontrada na pasta"""
        try:
            files = os.listdir(folder_path)
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']

            # Procurar primeira imagem na pasta
            for file in sorted(files):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    if any(file.lower().endswith(ext) for ext in image_extensions):
                        print(f"🖼️ Servindo imagem padrão: {file}")
                        self._serve_image_file(file_path)
                        return

            # Procurar em subpastas
            for file in sorted(files):
                subfolder_path = os.path.join(folder_path, file)
                if os.path.isdir(subfolder_path):
                    subfiles = os.listdir(subfolder_path)
                    for subfile in sorted(subfiles):
                        subfile_path = os.path.join(subfolder_path, subfile)
                        if os.path.isfile(subfile_path):
                            if any(subfile.lower().endswith(ext) for ext in image_extensions):
                                print(f"🖼️ Servindo imagem da subpasta: {subfile}")
                                self._serve_image_file(subfile_path)
                                return

            print("⚠️ Nenhuma imagem encontrada na pasta")
            self._serve_placeholder_image()

        except Exception as e:
            print(f"⚠️ Erro ao servir imagem padrão: {e}")
            self._serve_placeholder_image()

    def _serve_placeholder_image(self):
        """Serve imagem padrão quando não encontra a original"""
        try:
            placeholder_path = os.path.join(self.project_root, 'static', 'images', 'placeholders', 'sem-imagem.jpg')

            if os.path.exists(placeholder_path):
                with open(placeholder_path, 'rb') as img_file:
                    image_data = img_file.read()

                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', str(len(image_data)))
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(image_data)

                print("📷 Placeholder servido")
            else:
                self._handle_404()

        except Exception as e:
            print(f"⚠️ Erro no placeholder: {e}")
            self._handle_404()

    def _serve_static_file(self, filename):
        """Serve arquivos estáticos (HTML, CSS, JS)"""
        try:
            with open(filename, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()

            if filename.endswith('.html'):
                content_type = 'text/html; charset=utf-8'
            elif filename.endswith('.css'):
                content_type = 'text/css; charset=utf-8'
            elif filename.endswith('.js'):
                content_type = 'application/javascript; charset=utf-8'
            else:
                content_type = 'text/plain; charset=utf-8'

            self.send_response(200)
            self.send_header("Content-type", content_type)
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(conteudo.encode('utf-8'))

        except FileNotFoundError:
            resposta = {
                'success': False,
                'mensagem': 'Arquivo não encontrado',
                'error': 'Error 404 - Not Found'
            }
            self.send_json_response(resposta, 404)

    # 📦 HANDLERS DOS MÓVEIS
    def handle_moveis_destaque(self, query_params):
        try:
            print("==MOSTRANDO MÓVEIS EM DESTAQUE==")
            moveis_destaque = MoveisController.listar_destaques()

            if moveis_destaque and moveis_destaque.get('sucesso'):
                moveis = moveis_destaque.get('moveis')
                moveis_data = json.loads(moveis) if moveis else []

                resposta = {
                    'success': True,
                    'mensagem': "Móveis carregados com sucesso!",
                    'moveis': moveis_data,
                    'quantidade': len(moveis_data)
                }
                self.send_json_response(resposta)
            else:
                print("==NENHUM MÓVEL ENCONTRADO==")
                resposta = {
                    'success': False,
                    'mensagem': 'Nenhum móvel encontrado',
                    'moveis': []
                }
                self.send_json_response(resposta)

        except Exception as e:
            resposta = {
                'success': False,
                'mensagem': 'Erro interno no servidor',
                'moveis': []
            }
            self.send_json_response(resposta, 500)

    def handle_empresa_info(self):
        print("==MOSTRANDO INFORMAÇÕES DA EMPRESA==")
        try:
            informacao_empresa = MoveisController.informacoes_empresa()

            if informacao_empresa:
                informacao_data = json.loads(informacao_empresa) if informacao_empresa else []
                if informacao_data and informacao_data.get('data'):
                    informacao = informacao_data.get('data')

                    resposta = {
                        'success': True,
                        'mensagem': "Informações da empresa",
                        'informacao': informacao
                    }
                    self.send_json_response(resposta)
                else:
                    resposta = {
                        'success': False,
                        'mensagem': 'Estrutura de dados inesperada',
                        'informacao': {}
                    }
                    self.send_json_response(resposta)
            else:
                resposta = {
                    'success': False,
                    'mensagem': 'Informações da empresa não disponíveis no momento',
                    'informacao': {}
                }
                self.send_json_response(resposta)

        except json.JSONDecodeError as e:
            print(f"⚠️ Erro ao decodificar JSON: {e}")
            resposta = {
                'success': False,
                'mensagem': 'Erro ao processar dados da empresa',
                'informacao': {}
            }
            self.send_json_response(resposta, 500)
        except Exception as e:
            resposta = {
                'success': False,
                'mensagem': 'Erro interno no servidor',
                'informacao': []
            }
            self.send_json_response(resposta, 500)

    # 👤 HANDLERS DOS CLIENTES
    def handle_cadastrar_cliente(self):
        try:
            print("📝 Cadastrando cliente...")

            # Ler dados do POST
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            dados = json.loads(post_data.decode('utf-8'))

            print(f"📊 Dados recebidos: {dados}")

            # Cadastrar cliente
            cliente = FormularioCliente.registrar_cliente(
                nome_completo=dados['nome_completo'],
                telefone=dados['telefone'],
                email=dados['email'],
                cpf=dados['cpf'],
                localizacao_exata=dados['localizacao_exata']
            )

            if cliente:
                resposta = {
                    'success': True,
                    'message': 'Cliente cadastrado com sucesso!',
                    'cliente_id': cliente.id if hasattr(cliente, 'id') else None
                }
                self.send_json_response(resposta)
            else:
                resposta = {
                    'success': False,
                    'message': 'Erro ao cadastrar cliente'
                }
                self.send_json_response(resposta, 400)

        except Exception as e:
            print(f"⚠️ Erro ao cadastrar cliente: {e}")
            resposta = {
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }
            self.send_json_response(resposta, 500)

    # 📦 HANDLERS DOS PEDIDOS
    def handle_criar_pedido(self):
        try:
            print("📦 Criando pedido completo...")

            # Ler dados do POST
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            dados = json.loads(post_data.decode('utf-8'))

            print(f"📊 Dados do pedido: {dados}")

            # Extrair dados
            dados_cliente = dados.get('cliente', {})
            itens_carrinho = dados.get('itens', [])

            # Validar dados
            if not dados_cliente or not itens_carrinho:
                resposta = {
                    'success': False,
                    'message': 'Dados do cliente ou itens em falta'
                }
                self.send_json_response(resposta, 400)
                return

            # Criar pedido completo
            resultado = PedidosController.criar_pedido_completo(dados_cliente, itens_carrinho)

            if resultado.get('sucesso'):
                resposta = {
                    'success': True,
                    'message': resultado.get('message'),
                    'pedido_id': resultado.get('pedido_id'),
                    'cliente_id': resultado.get('cliente_id'),
                    'valor_total': resultado.get('valor_total')
                }
                self.send_json_response(resposta)
            else:
                resposta = {
                    'success': False,
                    'message': resultado.get('message', 'Erro ao criar pedido')
                }
                self.send_json_response(resposta, 400)

        except Exception as e:
            print(f"⚠️ Erro ao criar pedido: {e}")
            resposta = {
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }
            self.send_json_response(resposta, 500)

    def handle_listar_pedidos(self):
        try:
            print("📋 Listando pedidos...")
            resultado = PedidosController.listar_pedidos_json()

            if resultado.get('sucesso'):
                resposta = {
                    'success': True,
                    'message': resultado.get('message'),
                    'pedidos': resultado.get('pedidos'),
                    'quantidade': resultado.get('quantidade')
                }
                self.send_json_response(resposta)
            else:
                resposta = {
                    'success': False,
                    'message': resultado.get('message', 'Erro ao listar pedidos'),
                    'pedidos': []
                }
                self.send_json_response(resposta)

        except Exception as e:
            print(f"⚠️ Erro ao listar pedidos: {e}")
            resposta = {
                'success': False,
                'message': f'Erro interno: {str(e)}',
                'pedidos': []
            }
            self.send_json_response(resposta, 500)

    def handle_buscar_pedido(self, pedido_id):
        try:
            #print(f"🔍 Buscando pedido {pedido_id}...")

            # Validar ID
            try:
                pedido_id = int(pedido_id)
            except ValueError:
                resposta = {
                    'success': False,
                    'message': 'ID do pedido inválido'
                }
                self.send_json_response(resposta, 400)
                return

            resultado = PedidosController.buscar_pedido_json(pedido_id)

            if resultado.get('sucesso'):
                resposta = {
                    'success': True,
                    'message': resultado.get('message'),
                    'pedido': resultado.get('pedido')
                }
                self.send_json_response(resposta)
            else:
                resposta = {
                    'success': False,
                    'message': resultado.get('message', 'Pedido não encontrado')
                }
                self.send_json_response(resposta, 404)

        except Exception as e:
            print(f"⚠️ Erro ao buscar pedido: {e}")
            resposta = {
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }
            self.send_json_response(resposta, 500)

    # 🛠️ MÉTODOS UTILITÁRIOS
    def _handle_health_check(self):
        """Health check do servidor"""
        resposta = {
            'success': True,
            'message': 'Servidor funcionando!',
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }
        self.send_json_response(resposta)

    def _handle_404(self):
        response_data = {
            "success": False,
            "mensagem": "Endpoint não encontrado",
            "error": 'Error 404 - Not Found',
        }
        self.send_json_response(response_data, 404)

    def _handle_error(self, error_message):
        response_data = {
            "success": False,
            "message": "Erro interno do servidor",
            "error": error_message
        }
        self.send_json_response(response_data, 500)

    def log_message(self, format, *args):
        print(f"🌐 {self.address_string()} - {format % args}")

    def send_json_response(self, data, status_code=200):
        try:
            # ✅ USAR CUSTOM ENCODER para lidar com Decimal
            json_data = json.dumps(data, ensure_ascii=False, indent=2, cls=CustomJSONEncoder)

            self.send_response(status_code)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))

        except Exception as e:
            print(f"❌ Erro na serialização JSON: {e}")
            print(f"🔍 Dados que causaram o erro: {data}")

            # ✅ FALLBACK: Converter manualmente se der erro
            try:
                def convert_problematic_types(obj):
                    if isinstance(obj, Decimal):
                        return float(obj)
                    elif isinstance(obj, (datetime, date)):
                        return str(obj)
                    elif isinstance(obj, dict):
                        return {key: convert_problematic_types(value) for key, value in obj.items()}
                    elif isinstance(obj, list):
                        return [convert_problematic_types(item) for item in obj]
                    else:
                        return obj

                data_convertida = convert_problematic_types(data)
                json_data = json.dumps(data_convertida, ensure_ascii=False, indent=2)

                self.send_response(status_code)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(json_data.encode('utf-8'))

                print("✅ Fallback JSON serialization funcionou!")

            except Exception as e2:
                print(f"❌ Erro mesmo no fallback: {e2}")
                # Última tentativa: resposta de erro simples
                error_response = {
                    "success": False,
                    "message": "Erro na serialização de dados",
                    "error": str(e)
                }
                json_data = json.dumps(error_response, ensure_ascii=False)

                self.send_response(500)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(json_data.encode('utf-8'))

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")


class MoveisServer:
    def __init__(self, host='0.0.0.0', port=None):
        self.host = host
        # ✅ RENDER: Usar porta dinâmica ou 8000 como fallback
        self.port = port or int(os.environ.get('PORT', 8000))
        self.server = None

    def start(self):
        try:
            self.server = HTTPServer((self.host, self.port), APIRouter)
            print(f"🚀 Servidor rodando em http://{self.host}:{self.port}")
            print(f"📦 Móveis em destaque: http://{self.host}:{self.port}/api/moveis/destaques")
            print(f"🏢 Informações da empresa: http://{self.host}:{self.port}/api/info/empresa")
            print(f"🖼️ Imagens: http://{self.host}:{self.port}/static/images")
            self.server.serve_forever()

        except KeyboardInterrupt:
            print("\n⚠️ Servidor Interrompido")
        except Exception as e:
            print(f"❌ Erro ao iniciar servidor: {e}")

def create_server(host='0.0.0.0', port=None):
    return MoveisServer(host, port)

def main():
    servidor = create_server()
    return servidor.start()