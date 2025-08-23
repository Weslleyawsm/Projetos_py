import json
from app.models.movel import Movel

class MoveisController:

    @staticmethod
    def listar_destaques():
        try:
            destaques = Movel.buscar_destaque(limite=10)
            lista_de_destaques = [Movel.to_dict(movel) for movel in destaques]

            if lista_de_destaques:
                lista = []
                for item in lista_de_destaques:
                    lista.append(item)
                resposta_json = json.dumps(lista)
                dicionario = {
                    "sucesso": True,
                    "moveis": resposta_json,
                    "quantidade": len(lista)
                }

                return dicionario

            else:
                diciconario_de_destaque = {
                    "sucesso": False,
                    "quantidade": 0
                }
                return diciconario_de_destaque

        except Exception as e:
            print(f"Erro ao retornar moveis: {e}")
            return None

    @staticmethod
    def informacoes_empresa():
        informacoes_dictionario = {
           "data": {
               "nome": "Samarone Móveis",
               "descricao": 'Criamos móveis únicos combinando metalon e madeira com qualidade artesanal',
               "endereco": {
                   "cidade": "Armação dos Búzios",
                   "rua": "Rua Flor de Lotus",
                   "estado": "RJ",
                   "cep": "CEP: 28950-825"
               },
               "contato": {
                   "whatsapp": "22997380687",
                   "email": "weslleysheshe@gmail.com"
               },
               "material":[
                   {
                       "nome": "Metalon",
                       "descricao": "Estrutura resistente e design moderno"
                   },
                   {
                       "nome": "Madeira",
                       "descricao": "Acabamento natural e aconchegante"
                   }
                ]
           }
        }

        return json.dumps(informacoes_dictionario)

    

'''if __name__ == '__main__':
    
        print("==MOVEIS EM DESTAQUE==")
        movel = MoveisController.listar_destaques()
        print(movel)
        print("==DESCRIÇÂO DA EMPRESA==")
        empresa = MoveisController.informacoes_empresa()
        print(empresa)'''

