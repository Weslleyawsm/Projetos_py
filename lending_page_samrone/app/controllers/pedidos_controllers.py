from app.models.formualario_cliente import FormularioCliente
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido
import json

class PedidosController:

    @staticmethod
    def criar_pedido_completo(dados_cliente, itens_carrinho):
        try:
            # ✅ VERIFICAR SE CLIENTE JÁ EXISTE (por email OU cpf)
            cliente_existente = None

            # Buscar por email primeiro
            cliente_por_email = FormularioCliente.buscar_por_email(dados_cliente['email'])
            if cliente_por_email:
                cliente_existente = FormularioCliente.criar_do_banco(cliente_por_email)
                print(f"✅ Cliente encontrado por email: {dados_cliente['email']}")

            # Se não achou por email, buscar por CPF
            if not cliente_existente:
                cliente_por_cpf = FormularioCliente.buscar_por_cpf(dados_cliente['cpf'])
                if cliente_por_cpf:
                    cliente_existente = FormularioCliente.criar_do_banco(cliente_por_cpf)
                    print(f"✅ Cliente encontrado por CPF: {dados_cliente['cpf']}")

            if cliente_existente:
                # ✅ CLIENTE EXISTE - Reutilizar
                cliente = cliente_existente
                print(f"♻️ Reutilizando cliente existente ID: {cliente.id}")

                # Opcional: Atualizar dados do cliente se necessário
                try:
                    FormularioCliente.update_cliente(
                        cliente.id,
                        nome_completo=dados_cliente['nome_completo'],
                        telefone=dados_cliente['telefone'],
                        localizacao_exata=dados_cliente['localizacao_exata']
                    )
                    print(f"📝 Dados do cliente atualizados")
                except Exception as e:
                    print(f"⚠️ Aviso: Não foi possível atualizar dados do cliente: {e}")

            else:
                # ✅ CLIENTE NOVO - Cadastrar
                print(f"👤 Cadastrando novo cliente: {dados_cliente['email']}")
                cliente = FormularioCliente.registrar_cliente(
                    nome_completo=dados_cliente['nome_completo'],
                    telefone=dados_cliente['telefone'],
                    email=dados_cliente['email'],
                    cpf=dados_cliente['cpf'],
                    localizacao_exata=dados_cliente['localizacao_exata']
                )

            if not cliente:
                return {
                    'sucesso': False,
                    'message': 'Erro ao processar cliente'
                }

            # ✅ CALCULAR VALOR TOTAL
            valor_total = sum(item['quantidade'] * item['preco_unitario'] for item in itens_carrinho)
            print(f"💰 Valor total calculado: R$ {valor_total:.2f}")

            # ✅ CRIAR PEDIDO
            pedido = Pedido.criar_pedido(
                cliente_id=cliente.id,
                valor_total=valor_total,
                status="pendente",
                observacoes="Pedido criado via site"
            )

            if not pedido:
                return {
                    'sucesso': False,
                    'message': 'Erro ao criar pedido'
                }

            # ✅ ADICIONAR ITENS DO PEDIDO
            itens_pedidos = []

            for item in itens_carrinho:
                try:
                    item_pedido = ItemPedido.adicionar_item(
                        pedido_id=pedido.id,
                        movel_id=item['movel_id'],
                        quantidade=item['quantidade'],
                        preco_unitario=item['preco_unitario']
                    )
                    if item_pedido:
                        itens_pedidos.append(item_pedido.to_dict())
                        print(f"✅ Item adicionado: {item['nome']} x{item['quantidade']}")
                    else:
                        print(f"⚠️ Falha ao adicionar item: {item['nome']}")

                except Exception as e:
                    print(f"❌ Erro ao adicionar item {item.get('nome', 'N/A')}: {e}")

            # ✅ RESPOSTA DE SUCESSO
            return {
                'sucesso': True,
                'pedido_id': pedido.id,
                'cliente_id': cliente.id,
                'valor_total': pedido.valor_total,
                'itens_criados': itens_pedidos,
                'status': pedido.status,
                'message': f'Pedido #{pedido.id} criado com sucesso! Total: R$ {pedido.valor_total:.2f}'
            }

        except Exception as e:
            print(f"❌ Erro em criar_pedido_completo: {e}")
            return {
                'sucesso': False,
                'message': f'Erro interno: {str(e)}'
            }

            # ✅ ADICIONAR ITENS DO PEDIDO
            itens_pedidos = []

            for item in itens_carrinho:
                try:
                    item_pedido = ItemPedido.adicionar_item(
                        pedido_id=pedido.id,
                        movel_id=item['movel_id'],
                        quantidade=item['quantidade'],
                        preco_unitario=item['preco_unitario']
                    )
                    if item_pedido:
                        # ✅ DEBUG: Verificar tipos antes de adicionar
                        item_dict = item_pedido.to_dict()
                        print(f"🔍 DEBUG - Item dict: {item_dict}")
                        print(f"🔍 DEBUG - Tipos: {[(k, type(v)) for k, v in item_dict.items()]}")
                        itens_pedidos.append(item_dict)
                        print(f"✅ Item adicionado: {item['nome']} x{item['quantidade']}")
                    else:
                        print(f"⚠️ Falha ao adicionar item: {item['nome']}")

                except Exception as e:
                    print(f"❌ Erro ao adicionar item {item.get('nome', 'N/A')}: {e}")

            # ✅ DEBUG: Verificar todos os tipos na resposta final
            print(f"🔍 DEBUG - pedido.valor_total tipo: {type(pedido.valor_total)}")
            print(f"🔍 DEBUG - pedido.valor_total valor: {pedido.valor_total}")

            # ✅ CONVERSÃO FORÇADA DE TODOS OS DECIMAIS
            def convert_decimals(obj):
                """Converte recursivamente todos os Decimals para float"""
                import json
                from decimal import Decimal

                if isinstance(obj, Decimal):
                    return float(obj)
                elif isinstance(obj, dict):
                    return {key: convert_decimals(value) for key, value in obj.items()}
                elif isinstance(obj, list):
                    return [convert_decimals(item) for item in obj]
                else:
                    return obj

            # ✅ RESPOSTA DE SUCESSO - COM CONVERSÃO FORÇADA
            resposta_raw = {
                'sucesso': True,
                'pedido_id': pedido.id,
                'cliente_id': cliente.id,
                'valor_total': pedido.valor_total,  # Deixar como está para converter depois
                'itens_criados': itens_pedidos,
                'status': pedido.status,
                'message': f'Pedido #{pedido.id} criado com sucesso! Total: R$ {float(pedido.valor_total):.2f}'
            }

            # ✅ APLICAR CONVERSÃO RECURSIVA
            resposta_convertida = convert_decimals(resposta_raw)

            print(f"🔍 DEBUG - Resposta final: {resposta_convertida}")
            print(f"🔍 DEBUG - Tipos na resposta: {[(k, type(v)) for k, v in resposta_convertida.items()]}")

            return resposta_convertida

        except Exception as e:
            print(f"❌ Erro em criar_pedido_completo: {e}")
            import traceback
            traceback.print_exc()  # ✅ DEBUG: Stack trace completo
            return {
                'sucesso': False,
                'message': f'Erro interno: {str(e)}'
            }
    @staticmethod
    def listar_pedidos_json():
        try:
            lista_pedidos_json = []
            pedidos = Pedido.listar_pedidos()
            if not pedidos:
                return {
                    'sucesso': False,
                    'menssage': 'Erro ao listar pedidos'
                }

            for pedidos_dados in pedidos:
                item_object = Pedido.criar_do_banco(pedidos_dados) #criando um objeto

                pedido_dict = item_object.to_dict() #tranformando os dados desse objeto em dicionario

                itens = ItemPedido.buscar_por_pedido(item_object.id) #buscando itens por pedidos

                pedido_dict['itens'] = [item.to_dict for item in itens] if itens else [] #adicionando a chave 'itens' ao dicionario e atribuindo valores a essa chave


                lista_pedidos_json.append(pedido_dict) #adicionndo os itens na lista de pedidos

            return {
                'sucesso': True,
                'pedidos': lista_pedidos_json,
                'quantidade': len(lista_pedidos_json),
                'message': f'{len(lista_pedidos_json)} pedidos carregados com sucesso'
            }

        except Exception as e:
            print(f"❌ Erro em listar_pedidos_json: {e}")
            return {
                'sucesso': False,
                'pedidos': [],
                'quantidade': 0,
                'message': f'Erro ao carregar pedidos: {str(e)}'
            }

    @staticmethod
    def buscar_pedido_json(pedido_id):
        try:
            pedido = Pedido.buscar_id(pedido_id)
            if not pedido:
                return {
                    'sucesso': False,
                    'menssage': 'Erro ao buscar pedido'
                }
            pedido_object = Pedido.criar_do_banco(pedido)
            pedido_dict = pedido_object.to_dict()

            itens_pedido = ItemPedido.buscar_por_pedido(pedido_object.id)

            if itens_pedido:
                pedido_dict['itens'] = [item.to_dict for item in itens_pedido]
            else:
                pedido_dict['itens'] = []

            return {
                'sucesso': True,
                'pedido': pedido_dict,
                'message': 'Pedido encontrado com sucesso'
            }

        except Exception as e:
            print(f"❌ Erro ao buscar pedido json: {e}")
            return {
                'sucesso': False,
                'pedido': None,
                'message': f'Erro interno: {str(e)}'
            }