from app.models.database import Database
from datetime import datetime
class Pedido:
    def __init__(self, id = None, cliente_id = None, data_pedido = None, valor_total = 0.0, status = "pendente", observacoes = None):
        self.id = id
        self.cliente_id = cliente_id
        self.data_pedido = data_pedido
        self.valor_total = valor_total
        self.status = status
        self.observacoes = observacoes
    @classmethod
    def criar_do_banco(cls, dados):
        return cls(
            id = dados[0],
            cliente_id = dados[1],
            data_pedido= dados[2],
            valor_total = dados[3],
            status = dados[4],
            observacoes = dados[5]
        )

    def to_dict(self):
        dados_pedido = {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'data_pedido': str(self.data_pedido) if self.data_pedido else None,  # ✅ CONVERSÃO: datetime → str
            'valor_total': float(self.valor_total) if self.valor_total else 0.0,  # ✅ CONVERSÃO: Decimal → float
            'status': self.status,
            'observacoes': self.observacoes
        }
        return dados_pedido
    @staticmethod
    def criar_pedido(cliente_id, valor_total, status, observacoes):
        try:
            db = Database()
            query_pedidos = """INSERT INTO pedidos (cliente_id, data_pedido, valor_total, status, observacoes) VALUES (%s, NOW(), %s, %s, %s)"""
            resultado = db.execute_query(query_pedidos, params=(cliente_id, valor_total, status, observacoes),
                                         commit=True)

            if resultado:
                ultimo_pedido = db.cursor.lastrowid
                # ✅ CORREÇÃO: Buscar TODOS os campos do pedido
                query_buscar = """SELECT id, cliente_id, data_pedido, valor_total, status, observacoes FROM pedidos WHERE id = %s"""
                pedido_dados = db.execute_query(query_buscar, params=(ultimo_pedido,), fetch_one=True)

                if pedido_dados:
                    print(f"Pedido realizado! cliente: {pedido_dados[1]} | Valor: R${pedido_dados[3]}")
                    # ✅ CORREÇÃO: Retornar objeto Pedido em vez de tupla
                    return Pedido.criar_do_banco(pedido_dados)
                else:
                    return None
            else:
                print(f"Pedido não realizado!")
                return None

        except Exception as e:
            print(f"Erro ao criar pedido: {e}")
            return None
        finally:
            db.disconnect()

    @staticmethod
    def buscar_id(id_pedido):
        try:
            db = Database()
            query_pedidos = """SELECT * FROM pedidos WHERE id = %s"""
            resultado = db.execute_query(query_pedidos, params = (id_pedido,), fetch_one=True)
            if resultado:
                print(f"Pedido {resultado[0]} encontrado. CLIENTE ID {resultado[1]}")
                return resultado
            else:
                print(f"Cliente não encontrado!")
                return None
        except Exception as e:
            print(f"Erro ao buscar pedido: {e}")
            return False
        finally:
            db.disconnect()

    @staticmethod
    def listar_pedidos():
        try:
            db = Database()
            query_pedidos = """SELECT * FROM pedidos"""
            resultado = db.execute_query(query_pedidos)
            if resultado:
                print(f"=== LISTANDO PEDIDOS ===")
                for id, nome_id, data_pedido, valor_total, status, observacoes in resultado:
                    data_formatada = datetime.strftime(data_pedido, '%Y-%m-%d %H:%M:%S') if data_pedido else 'N/A'
                    print(f"ID: {id} Nome ID: {nome_id} Data e Hora: {data_formatada} Valor: R${valor_total:5.2f} Status: {status:10s} Observações: {observacoes}")
                return True
            else:
                print(f"Nenhum pedido encontrado!!")
                return None

        except Exception as e:
            print(f"Erro ao listar pedidos: {e}")
            return False
        finally:
            db.disconnect()

    @staticmethod
    def atualizar_status(id_pedido, status_atual):
        try:
            db = Database()
            query_verifica = """SELECT * FROM pedidos WHERE id = %s"""
            verificar = db.execute_query(query_verifica, params = (id_pedido,))
            if verificar:
                query_status = """UPDATE pedidos SET status = %s WHERE id = %s"""
                tipos_status = ["pendente", "confirmado", "em_producao", "pronto", "entregue", "cancelado"]
                if status_atual in  tipos_status:
                    resultado = db.execute_query(query_status, params = (status_atual, id_pedido), commit=True)
                    if resultado:
                        resultado_2 = db.execute_query("SELECT * FROM pedidos WHERE id = %s", (id_pedido,))
                        print(f"\nStatus atualizao com sucesso!\n")
                        for id, nome_id, data_pedido, valor_total, status, observacoes in resultado_2:
                            data_formatada = datetime.strftime(data_pedido, '%Y-%m-%d %H:%M:%S') if data_pedido else 'N/A'
                            print(f"\nID: {id} Nome ID: {nome_id} Data e Hora: {data_formatada} Valor: R${valor_total:5.2f} Status: {status:10s} Observações: {observacoes}")
                    else:
                        print(f"Nenhum pedido alterado!")
                        return None
                else:
                    print(f"Status inválido!")
                    return False
            else:
                print(f"Pedido inexistente!")
                return None

        except Exception as e:
            print(f"Erro ao atualizar status do pedido: {e}")
            return False
        finally:
            db.disconnect()

    @staticmethod
    def deletar_pedido(id_pedido):
        try:
            db = Database()
            query_verifica = "SELECT * FROM pedidos WHERE id = %s"
            verifica = db.execute_query(query_verifica, params = (id_pedido,), fetch_one=True)
            if verifica:
                query_delete = """DELETE FROM pedidos WHERE id = %s"""
                resultado = db.execute_query(query_delete, params = (id_pedido,), commit=True)
                if resultado:
                    print(f"Pedido de ID {id_pedido} removido com sucesso!")
                    return True
                else:
                    print(f"Não foi possivel deletar pedido!")
                    return False

            else:
                print(f"Pedido inexistente!")
                return None

        except Exception as e:
            print(f"Erro ao deletar pedido: {e}")

        finally:
            db.disconnect()

pedido = Pedido()
#pedido.criar_pedido(2, valor_total = 200, status = "pendente", observacoes= "Testando")
#pedido.buscar_id(18)
pedido.listar_pedidos()
#pedido.atualizar_status(18, "entregue")
#pedido.deletar_pedido(19)
#pedido.listar_pedidos()