from app.models.database import Database
from mysql.connector import Error
class Movel:
    def __init__(self, id=None, nome=None, descricao=None, materiais=None, imagem_url=None, destaque=False, ativo=True, created_at=None, imagens=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.materiais = materiais
        self.imagem_url = imagem_url
        self.destaque = destaque
        self.ativo = ativo
        self.created_at = created_at
        self.imagens = imagens or []

    @classmethod
    def buscar_destaque(cls, limite=10):
        db = Database()
        moveis_query = "SELECT * FROM moveis WHERE destaque = True AND ativo = True ORDER BY created_at DESC LIMIT %s"
        moveis_data = db.execute_query(moveis_query, (limite,))

        lista_de_moveis = []
        if moveis_data:
            for item in moveis_data:
                movel = cls._criar_do_banco(item)

                query_imagens = "SELECT imagem_url, alt_text, principal, ordem FROM moveis_imagens WHERE movel_id = %s ORDER BY ordem ASC"
                imagens_data = db.execute_query(query_imagens, params=(movel.id,))

                if imagens_data:
                    movel.imagens = [{
                        'url': img[0],
                        'alt': img[1],
                        'principal': bool(img[2]),
                        'ordem': img[3]
                    } for img in imagens_data
                    ]

                if not movel.imagem_url and movel.imagens:
                    movel.imagem_url = movel.imagens[0]['img']

                lista_de_moveis.append(movel)
        db.disconnect()
        return lista_de_moveis

    @classmethod
    def _criar_do_banco(cls, dados):
        return cls(
            id=dados[0],
            nome=dados[1],
            descricao=dados[2],
            materiais=dados[3],
            imagem_url=dados[4],
            destaque=dados[5],
            ativo=dados[6],
            created_at=dados[7],

        )

    @classmethod
    def buscar_preco_atual(cls, movel_id):
        try:
            db = Database()
            # ✅ QUERY CORRIGIDA: Busca qualquer preço ativo
            query = """
                SELECT preco_base, preco_promocional, data_inicio, data_fim 
                FROM precos
                WHERE movel_id = %s
                AND ativo = TRUE
                ORDER BY id DESC
                LIMIT 1
            """

            resultado = db.execute_query(query, params=(movel_id,), fetch_one=True)

            if resultado:
                preco_base = float(resultado[0]) if resultado[0] else 0.0
                preco_promocional = float(resultado[1]) if resultado[1] else None

                # ✅ LÓGICA CORRIGIDA: preco_atual sempre existe
                preco_atual = preco_promocional if preco_promocional else preco_base

                resposta = {
                    'preco_base': preco_base,
                    'preco_promocional': preco_promocional,
                    'data_inicio': resultado[2],
                    'data_fim': resultado[3],
                    'preco_atual': preco_atual  # ✅ NUNCA será None se preco_base existe
                }

                return resposta
            else:
                print(f"⚠️ Nenhum preço encontrado para móvel ID {movel_id}")
                return None

        except Exception as e:
            print(f"❌ Erro ao buscar preço para móvel {movel_id}: {e}")
            return None
        finally:
            db.disconnect()

    def buscar_preco(self):
        if self.id:
            return self.buscar_preco_atual(self.id)
        else:
            return None

    def to_dict(self):
        dados_base = {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'materiais': self.materiais,
            'imagem_url': self.imagem_url,
            'destaque': self.destaque,
            'ativo': self.ativo,
            'created_at': str(self.created_at) if self.created_at else None,
            'imagens': self.imagens
        }

        moveis_preco = self.buscar_preco()
        if moveis_preco:
            dados_base.update({
                'preco_base': float(moveis_preco['preco_base']) if moveis_preco['preco_base'] else None,  # ✅ CONVERSÃO
                'preco_promocional': float(moveis_preco['preco_promocional']) if moveis_preco[
                    'preco_promocional'] else None,  # ✅ CONVERSÃO
                'preco_atual': float(moveis_preco['preco_atual']) if moveis_preco['preco_atual'] else None,
                # ✅ CONVERSÃO
                'tem_promocao': moveis_preco['preco_promocional'] is not None,
            })
        else:
            dados_base.update({
                'preco_base': None,
                'preco_promocional': None,
                'preco_atual': None,
                'tem_promocao': False
            })

        return dados_base

    @staticmethod
    def remover_imagem(imagem_id):
        db = Database()
        query = "DELETE FROM moveis_imagens WHERE id = %s"
        db.execute_query(query, params=(imagem_id,), commit=True)
        db.disconnect()

    @staticmethod
    def reordenar_imagens(nova_ordem, movel_id):
        db = Database()
        for posicao, imagem_id in enumerate(nova_ordem, 1):
            update_query = "UPDATE moveis_imagens SET ordem = %s WHERE id = %s AND movel_id = %s"
            db.execute_query(update_query, params  = (posicao, imagem_id, movel_id), commit=True)
        db.disconnect()

    @staticmethod
    def adicionar_imagens(movel_id, imagem_url, ordem=None, principal=False, alt_text=None):
        db = Database()

        #se não for passado a ordem, por padrão deve ser o ultimo
        if ordem is None:
            query_count = "SELECT COUNT(*) FROM moveis_imagens WHERE movel_id = %s"
            count_result = db.execute_query(query_count, (movel_id, ), fetch_one=True)
            ordem = count_result[0] + 1 if count_result else 1

        if principal == True:
            query_update = "UPDATE moveis_imagens set principal = False where movel_id = %s"
            db.execute_query(query_update, (movel_id,), commit=True)

        insert_query = "INSERT INTO moveis_imagens (movel_id, imagem_url, ordem, principal, alt_text) VALUES (%s, %s, %s, %s, %s)"
        db.execute_query(insert_query, (movel_id, imagem_url, ordem, principal, alt_text), commit=True)
        db.disconnect()


if __name__ == "__main__":
    movel = Movel.buscar_destaque()

    '''for i in movel:
        print(f"Nome: {i.nome}\nDescrição: {i.descricao}\nMateriais: {i.materiais}\n\n")

        print(f"\n\nDADOS JSON")
        print(f"{i.to_dict()}")'''

    print(f"===PREÇO DOS MOVEIS===")
    preco_movel=Movel.buscar_preco_atual(1)
    print(f"{preco_movel}")
