import requests
import json
from datetime import datetime

from app.controllers.pedidos_controllers import PedidosController, buscar_itens
from app.models.pedido import Pedido
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class PagamentosController:
    # ✅ CREDENCIAIS DE TESTE (suas credenciais reais)
    ACCESS_TOKEN = "APP_USR-949940508489516-090116-f366f4ebcd3ccef9aff076fb5e81e264-2324168709"
    PUBLIC_KEY = "APP_USR-12797475-dcec-414a-8b96-cfbde34cbcb8"

    # URLs da API do Mercado Pago
    MP_API_BASE = "https://api.mercadopago.com"

    @staticmethod
    def criar_preferencia_pagamento(pedido_id, dados_cliente, itens_carrinho):
        """
        Cria preferência de pagamento no Mercado Pago
        """
        try:
            print(f"🔄 Criando preferência de pagamento para pedido #{pedido_id}")

            # 📦 PREPARAR ITENS PARA O MERCADO PAGO
            items_mp = []
            for item in itens_carrinho:
                item_mp = {
                    "id": str(item.get('movel_id', item.get('id'))),
                    "title": item.get('nome', 'Móvel Artesanal'),
                    "description": item.get('materiais', 'Metalon + Madeira'),
                    "quantity": int(item.get('quantidade', 1)),
                    "unit_price": float(item.get('preco_unitario', 0)),
                    "currency_id": "BRL"
                }
                items_mp.append(item_mp)
                print(f"📋 Item adicionado: {item_mp['title']} - R$ {item_mp['unit_price']}")

            # 👤 DADOS DO COMPRADOR
            payer = {
                "name": dados_cliente.get('nome_completo', ''),
                "email": dados_cliente.get('email', ''),
                "phone": {
                    "number": dados_cliente.get('telefone', '').replace('(', '').replace(')', '').replace('-',
                                                                                                          '').replace(
                        ' ', '')
                },
                "identification": {
                    "type": "CPF",
                    "number": dados_cliente.get('cpf', '').replace('.', '').replace('-', '')
                },
                "address": {
                    "zip_code": "28950000",  # CEP padrão de Búzios
                    "street_name": dados_cliente.get('localizacao_exata', '')[:100]  # Limitado a 100 chars
                }
            }

            # 🌐 URLs DE RETORNO (ajustar para seu domínio)
            base_url = "https://projetos-py-1.onrender.com"  # TODO: Alterar para URL real

            # 🔧 CONFIGURAR PREFERÊNCIA
            preference_data = {
                "items": items_mp,
                "payer": payer,
                "payment_methods": {
                    "excluded_payment_types": [],  # Aceitar todos os tipos
                    "installments": 12  # Até 12x
                },
                "back_urls": {
                    "success": f"{base_url}/confirmacao.html?status=success&pedido={pedido_id}",
                    "failure": f"{base_url}/confirmacao.html?status=failure&pedido={pedido_id}",
                    "pending": f"{base_url}/confirmacao.html?status=pending&pedido={pedido_id}"
                },
                "auto_return": "approved",
                "external_reference": str(pedido_id),  # Referência do seu sistema
                "notification_url": f"{base_url}/api/pagamentos/webhook",  # Para receber notificações
                "expires": False,  # Link não expira
                "metadata": {
                    "pedido_id": pedido_id,
                    "cliente_email": dados_cliente.get('email'),
                    "sistema": "samarone_moveis"
                }
            }

            # 📡 FAZER REQUISIÇÃO PARA MERCADO PAGO
            headers = {
                "Authorization": f"Bearer {PagamentosController.ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }

            url = f"{PagamentosController.MP_API_BASE}/checkout/preferences"

            print(f"🚀 Enviando requisição para: {url}")
            print(f"📊 Dados da preferência: {json.dumps(preference_data, indent=2, default=str)}")

            response = requests.post(url, json=preference_data, headers=headers)

            print(f"📨 Status da resposta: {response.status_code}")
            print(f"📄 Resposta completa: {response.text}")

            if response.status_code == 201:
                # ✅ SUCESSO
                preference = response.json()

                resultado = {
                    'sucesso': True,
                    'preferencia_id': preference['id'],
                    'checkout_url': preference['init_point'],  # URL para redirecionar cliente
                    'sandbox_url': preference.get('sandbox_init_point'),  # URL de teste
                    'qr_code': preference.get('qr_code'),
                    'expires_at': preference.get('expires_at'),
                    'message': 'Preferência criada com sucesso!'
                }

                print(f"✅ Preferência criada: {preference['id']}")
                print(f"🔗 URL de checkout: {preference['init_point']}")

                return resultado

            else:
                # ❌ ERRO
                error_data = response.json() if response.text else {}
                error_message = error_data.get('message', 'Erro desconhecido')

                print(f"❌ Erro ao criar preferência: {error_message}")
                print(f"📄 Detalhes do erro: {error_data}")

                return {
                    'sucesso': False,
                    'message': f'Erro do Mercado Pago: {error_message}',
                    'detalhes': error_data
                }

        except requests.exceptions.RequestException as e:
            print(f"🌐 Erro de conexão: {e}")
            return {
                'sucesso': False,
                'message': 'Erro de conexão com Mercado Pago',
                'erro': str(e)
            }

        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            import traceback
            traceback.print_exc()

            return {
                'sucesso': False,
                'message': 'Erro interno no sistema de pagamentos',
                'erro': str(e)
            }

    @staticmethod
    def processar_webhook(dados_webhook):
        """
        Processa notificações do Mercado Pago (webhook)
        """
        try:
            print(f"📨 Webhook recebido: {dados_webhook}")

            # 🔍 EXTRAIR INFORMAÇÕES DO WEBHOOK
            action = dados_webhook.get('action')
            api_version = dados_webhook.get('api_version')
            data_id = dados_webhook.get('data', {}).get('id')

            if not data_id:
                print("⚠️ Webhook sem ID de pagamento")
                return {'sucesso': False, 'message': 'Webhook inválido'}

            # 🔍 BUSCAR DETALHES DO PAGAMENTO
            detalhes_pagamento = PagamentosController.buscar_pagamento(data_id)

            if not detalhes_pagamento.get('sucesso'):
                return detalhes_pagamento

            pagamento = detalhes_pagamento['pagamento']
            pedido_id = pagamento.get('external_reference')
            status = pagamento.get('status')

            if not pedido_id:
                print("⚠️ Pagamento sem referência do pedido")
                return {'sucesso': False, 'message': 'Pagamento sem referência'}

            # 📊 ATUALIZAR STATUS DO PEDIDO
            novo_status = PagamentosController.mapear_status_mp(status)
            resultado_update = PagamentosController.atualizar_status_pedido(
                pedido_id, novo_status, pagamento
            )

            print(f"✅ Webhook processado - Pedido #{pedido_id}: {status} -> {novo_status}")

            return {
                'sucesso': True,
                'pedido_id': pedido_id,
                'status_anterior': status,
                'status_novo': novo_status,
                'pagamento_id': data_id
            }

        except Exception as e:
            print(f"❌ Erro ao processar webhook: {e}")
            return {
                'sucesso': False,
                'message': 'Erro ao processar webhook',
                'erro': str(e)
            }

    @staticmethod
    def buscar_pagamento(payment_id):
        """
        Busca detalhes de um pagamento específico
        """
        try:
            headers = {
                "Authorization": f"Bearer {PagamentosController.ACCESS_TOKEN}"
            }

            url = f"{PagamentosController.MP_API_BASE}/v1/payments/{payment_id}"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                pagamento = response.json()
                return {
                    'sucesso': True,
                    'pagamento': pagamento
                }
            else:
                error_data = response.json() if response.text else {}
                return {
                    'sucesso': False,
                    'message': f'Erro ao buscar pagamento: {response.status_code}',
                    'detalhes': error_data
                }

        except Exception as e:
            print(f"❌ Erro ao buscar pagamento: {e}")
            return {
                'sucesso': False,
                'message': 'Erro ao consultar pagamento',
                'erro': str(e)
            }

    @staticmethod
    def mapear_status_mp(status_mp):
        """
        Mapeia status do Mercado Pago para status do sistema
        """
        mapeamento = {
            'pending': 'aguardando_pagamento',
            'approved': 'pago',
            'in_process': 'processando',
            'in_mediation': 'em_disputa',
            'rejected': 'pagamento_rejeitado',
            'cancelled': 'cancelado',
            'refunded': 'reembolsado',
            'charged_back': 'estornado'
        }

        return mapeamento.get(status_mp, 'status_desconhecido')

    @staticmethod
    def atualizar_status_pedido(pedido_id, novo_status, dados_pagamento=None):
        """
        Atualiza status do pedido no banco de dados
        """
        try:
            # TODO: Implementar método update_status na classe Pedido
            # Por enquanto, usar método existente se houver
            resultado = Pedido.atualizar_status(pedido_id, novo_status)

            if resultado:
                print(f"✅ Status do pedido #{pedido_id} atualizado para: {novo_status}")

                # TODO: Enviar notificação por email/WhatsApp
                if novo_status == 'pago':
                    PagamentosController.notificar_pagamento_aprovado(pedido_id, dados_pagamento)

                return {
                    'sucesso': True,
                    'message': f'Status atualizado para: {novo_status}'
                }
            else:
                return {
                    'sucesso': False,
                    'message': 'Erro ao atualizar status no banco'
                }

        except Exception as e:
            print(f"❌ Erro ao atualizar status: {e}")
            return {
                'sucesso': False,
                'message': 'Erro interno ao atualizar status',
                'erro': str(e)
            }

    @staticmethod
    def notificar_pagamento_aprovado(pedido_id, dados_pagamento):
        """
        Envia notificações quando pagamento é aprovado
        """
        print(f"📧 Enviando notificações para pedido #{pedido_id}")


        pedido_cliente = PedidosController.buscar_pedido_json(pedido_id)
        email = pedido_cliente['pedido']['cliente']['email']
        nome = pedido_cliente['pedido']['cliente']['nome_completo']
        valor = dados_pagamento.get('transaction_amount', 0)
        valor_formatado = f"{valor:.2f}".replace('.', ',')
        data_pagamento = dados_pagamento.get('date_approved', 'N/A')
        if data_pagamento:
            data_pagamento_formatada = datetime.fromisoformat(data_pagamento.replace('Z', '+00:00')).strftime('%d/%m/%Y às %H:%M')
        else:
            return None

        metodos_pagamento = {
            'visa': 'Cartão Visa',
            'master': 'Cartão Mastercard',
            'elo': 'Cartão Elo',
            'pix': 'PIX',
            'bolbradesco': 'Boleto Bradesco',
            'account_money': 'Saldo Mercado Pago'
        }
        metodo_pagamento_formatado = metodos_pagamento.get(dados_pagamento.get('payment_method_id', 'N/A'), 'N/A')
        # Criação de um objeto de mensagem
        msg = MIMEMultipart()
        texto = (f"Número do pedido: #{pedido_id}\n"
                 f"Nome: {nome}\n"
                 f"Email: {email}\n"
                 f"Valor: R${valor_formatado}\n"
                 f"Método de Pagamento: {metodo_pagamento_formatado}\n"
                 f"Data de Pagamento: {data_pagamento_formatada}\n"
                 f"ID da Transação: {dados_pagamento.get('id', 'N/A')}\n"
                 f"OBRIGADO PELA PREFERÊNCIA!")

        # Parâmetros
        senha = "lvnw gahg gfhy utwn"  # senha de app válida
        msg['From'] = "weslleymartha@gmail.com"
        msg['To'] = email  # Pode ser outro email também
        msg['Subject'] = f"Olá {nome}! Seu pagamento foi APROVADO"

        # Criação do corpo da mensagem
        msg.attach(MIMEText(texto, 'plain'))

        try:
            # Criação do servidor
            server = smtplib.SMTP('smtp.gmail.com', 587)  # conexão com o servidor
            server.starttls()

            # Login na conta para envio
            server.login(msg['From'], senha)

            # Envio da mensagem
            server.sendmail(msg['From'], msg['To'], msg.as_string())

            # Encerramento do servidor
            server.quit()

            print('Mensagem enviada com sucesso')

        except smtplib.SMTPAuthenticationError as e:
                print(f"Erro de autenticação: {e}")
                print("Verifique se a senha de app está correta e se o 2FA está ativado")

        except smtplib.SMTPException as e:
                print(f"Erro SMTP geral: {e}")

        except Exception as e:
                print(f"Erro inesperado: {e}")
        # TODO: Implementar notificação WhatsApp via API

            # Por enquanto, apenas log
        #print(f"✅ Cliente notificado sobre aprovação do pedido #{pedido_id}")

        #except Exception as e:
            #print(f"⚠️ Erro ao enviar notificações: {e}")

    @staticmethod
    def cancelar_preferencia(preferencia_id):
        """
        Cancela uma preferência de pagamento
        """
        try:
            headers = {
                "Authorization": f"Bearer {PagamentosController.ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }

            url = f"{PagamentosController.MP_API_BASE}/checkout/preferences/{preferencia_id}"

            # Atualizar preferência para expirada
            data = {"expires": True, "expiration_date_to": datetime.now().isoformat()}

            response = requests.put(url, json=data, headers=headers)

            if response.status_code == 200:
                return {
                    'sucesso': True,
                    'message': 'Preferência cancelada com sucesso'
                }
            else:
                return {
                    'sucesso': False,
                    'message': 'Erro ao cancelar preferência'
                }

        except Exception as e:
            print(f"❌ Erro ao cancelar preferência: {e}")
            return {
                'sucesso': False,
                'message': 'Erro interno',
                'erro': str(e)
            }


# 🧪 FUNÇÃO DE TESTE
def testar_integracao():
    """
    Função para testar a integração com dados fictícios
    """
    print("🧪 Testando integração Mercado Pago...")

    # Dados de teste
    pedido_id = 999
    dados_cliente = {
        'nome_completo': 'João Silva Teste',
        'email': 'joao.teste@email.com',
        'telefone': '22999887766',
        'cpf': '12345678901',
        'localizacao_exata': 'Rua Teste, 123 - Búzios, RJ'
    }

    itens_carrinho = [
        {
            'movel_id': 1,
            'nome': 'Mesa de Centro Industrial - TESTE',
            'materiais': 'Metalon + Madeira',
            'quantidade': 1,
            'preco_unitario': 450.00
        }
    ]

    resultado = PagamentosController.criar_preferencia_pagamento(
        pedido_id, dados_cliente, itens_carrinho
    )




    print("📊 Resultado do teste:")
    print(json.dumps(resultado, indent=2, default=str))
    def testar_notificação():
        pedido_id = 56
        dados_pagamento_teste = {
            "id": "1234567890",
            "transaction_amount": 1158.99,
            "payment_method_id": "pix",
            "date_approved": "2025-09-02T14:35:15.000Z",
            "status": "approved"
        }
        PagamentosController.notificar_pagamento_aprovado(pedido_id, dados_pagamento_teste)

    #print(PagamentosController.buscar_pagamento(999))
    testar_notificação()
    return resultado


if __name__ == "__main__":
    # Executar teste se rodar o arquivo diretamente
    testar_integracao()


