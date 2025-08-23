from app.models.database import Database

class ItemPedido:
    def __init__(self, id, pedido_id, movel_id, quantidade, preco_unitario, subtotal):
        self.id = id
        self.pedido_id = pedido_id
        self.movel_id = movel_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.subtotal = subtotal

    @classmethod
    def criar_do_banco(cls, dados):
        return cls(
            id = dados[0],
            pedido_id = dados[1],
            movel_id = dados[2],
            quantidade = dados[3],
            preco_unitario = dados[4],
            subtotal=dados[5]
        )

    def to_dict(self):
        dados_item_pedido = {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'movel_id': self.movel_id,
            'quantidade': self.quantidade,
            'preco_unitario': float(self.preco_unitario) if self.preco_unitario else 0.0,  # ✅ CONVERSÃO
            'subtotal': float(self.subtotal) if self.subtotal else 0.0  # ✅ CONVERSÃO
        }
        return dados_item_pedido

    @staticmethod
    def adicionar_item(pedido_id, movel_id, quantidade, preco_unitario):
        try:
            db = Database()
            subtotal = preco_unitario * quantidade
            query_pedido = """INSERT INTO itens_pedidos (pedido_id, movel_id, quantidade, preco_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)"""
            resultado = db.execute_query(query_pedido, params=(pedido_id, movel_id, quantidade, preco_unitario, subtotal), commit=True)
            if resultado:
                ultimo_registro_id = db.cursor.lastrowid
                pedido = db.execute_query("SELECT * FROM itens_pedidos WHERE id = %s", params=(ultimo_registro_id,), fetch_one=True)
                print(f"Pedido de ID {pedido[0]} recebido com sucesso! O item foi adicionado ao pedido {pedido[1]}. Preço total do pedido: {pedido[5]}")
                return ItemPedido.criar_do_banco(pedido)
            else:
                print(f"Não foi possivel receber o pedido!")
                return None
        except Exception as e:
            print(f"Erro ao receber pedido")
            return False
        finally:
            db.disconnect()

    @staticmethod
    def buscar_por_pedido(pedido_id):
        try:
            db = Database()
            query_pedido = """SELECT * FROM itens_pedidos WHERE pedido_id = %s"""
            resultado = db.execute_query(query_pedido, params=(pedido_id,))
            if resultado:
                print(f"=== ITENS DO PEDIDO {pedido_id} ===")
                for id, pedido, movel_id, quantidade, preco_unitario, subtotal in resultado:
                    print(f"ID {id} - Pedido {pedido:2} - Movel ID {movel_id:2} - Quantidade {quantidade:2} - Preço por Unidade {preco_unitario:8.2f} - Subtotal: {subtotal:8.2f}")
                return [ItemPedido.criar_do_banco(item) for item in resultado]
            else:
                print(f"Não foi possível encontrar o pedido!!")
                return []
        except Exception as e:
            print(f"Erro ao buscar pedido: {e}")
            return []
        finally:
            db.disconnect()

    @staticmethod
    def remover_item(id_item):
        try:
            db = Database()
            query_remover = """DELETE FROM itens_pedidos WHERE id = %s"""
            resultado = db.execute_query(query_remover, params=(id_item,), commit=True)
            if resultado:
                print(f"Item de ID {id_item} removido com sucesso!")
                return True
            else:
                print(f"Não foi possivel remover o item")
                return None
        except Exception as e:
            print(f"Erro ao remover itens pedido: {e}")
            return False
        finally:
            db.disconnect()

