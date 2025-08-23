from mysql.connector import Error
from app.models.database import Database

class FormularioCliente:

    def __init__(self, id, nome_completo=None, telefone=None, email=None, cpf=None, localizacao_exata=None, ativo=True, data_cadastro = None):
        self.id = id
        self.nome_completo = nome_completo
        self.telefone = telefone
        self.email = email
        self.cpf = cpf
        self.localizacao_exata = localizacao_exata
        self.data_cadastro = data_cadastro
        self.ativo = ativo


    def _to_dict(self):
        dados_dicionario = {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'telefone': self.telefone,
            'email':self.email,
            'cpf': self.cpf,
            'localizacao_exata': self.localizacao_exata,
            'data_cadastro': str(self.data_cadastro) if self.data_cadastro else None,
            'ativo': self.ativo
        }
        return dados_dicionario
    @classmethod
    def criar_do_banco(cls, dados):
        return cls(
            id=dados[0],
            nome_completo=dados[1],
            telefone=dados[2],
            email=dados[3],
            cpf=dados[4],
            localizacao_exata=dados[5],
            data_cadastro=dados[6],
            ativo=dados[7]
        )
    @staticmethod
    def formatar_cliente(cliente):
        return f"Nome completo: {cliente[1]:50s} Telefone: {cliente[2]:12s} Email: {cliente[3]:30s} CPF: {cliente[4]:15s} Endereço: {cliente[5]:70s} Status: {cliente[7]}."

    @staticmethod
    def registrar_cliente(nome_completo, telefone, email, cpf, localizacao_exata):
        try:
            db = Database()
            query_insert = """INSERT INTO formulario_cliente(nome_completo, telefone, email, cpf, localizacao_exata) VALUES(%s, %s, %s, %s, %s)"""
            params = (nome_completo, telefone, email, cpf, localizacao_exata)
            resultado = db.execute_query(query_insert, params, commit=True)
            if resultado:
                id_cliente = db.cursor.lastrowid #pega o id do ultimo registro
                query_buscar = "SELECT * FROM formulario_cliente WHERE id = %s"
                cliente = db.execute_query(query_buscar, (id_cliente,), fetch_one=True)

                if cliente:
                    #print(FormularioCliente.formatar_cliente(cliente))
                    # ✅ CORREÇÃO: Retornar objeto cliente em vez de boolean
                    return FormularioCliente.criar_do_banco(cliente)
                else:
                    return None
            else:
                print(f"Erro ao registrar cliente")
        except Exception as e:
            print(f"Erro ao registrar cliente: {e}")
            return None
        finally:
            db.disconnect()

    @staticmethod
    def buscar_por_id(id_cliente):
        try:
            db = Database()
            query_buscar = "SELECT * FROM formulario_cliente WHERE id = %s"
            resultado = db.execute_query(query_buscar, (id_cliente,), fetch_one=True)
            if resultado:
                print(FormularioCliente.formatar_cliente(resultado))
                return resultado
            else:
                print(f"Cliente não encontrado")
                return None

        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
        finally:
            db.disconnect()

    @staticmethod
    def buscar_por_email(email):
        try:
            db = Database()
            query_buscar = "SELECT * FROM formulario_cliente WHERE email = %s"
            resultado = db.execute_query(query_buscar, (email,), fetch_one=True)
            if resultado:
                print(FormularioCliente.formatar_cliente(resultado))
                return resultado
            else:
                print(f"Não ha nenhum cliente com este email registrado")
                return None

        except Exception as e:
            print(f"Erro ao buscar cliente por email: {e}")
        finally:
            db.disconnect()

    @staticmethod
    def buscar_por_cpf(cpf):
        try:
            db = Database()
            query_buscar = "SELECT * FROM formulario_cliente WHERE cpf = %s"
            resultado = db.execute_query(query_buscar, (cpf,), fetch_one=True)
            if resultado:
                print(FormularioCliente.formatar_cliente(resultado))
                return resultado
            else:
                print(f"Nenhum cliente com este cpf registrado")
                return None
        except Exception as e:
            print(f"Erro ao buscar cliente por cpf: {e}")
            return None

        finally:
            db.disconnect()

    @staticmethod
    def listar_todos_clientes():
        try:
            db = Database()
            query_list = "SELECT * FROM formulario_cliente"
            resultado = db.execute_query(query_list)
            if resultado:
                for i in resultado:
                    print(FormularioCliente.formatar_cliente(i))
                return resultado
            else:
                print(f"Nenhum cliente registrado")
                return None
        except Exception as e:
            print(f"Erro ao listar todos os clientes: {e}")
            return False
        finally:
            db.disconnect()

    @staticmethod
    def update_cliente(id_cliente, **campos):
        try:
            db = Database()
            verifica_id = "SELECT * FROM formulario_cliente WHERE id = %s"
            resultado = db.execute_query(verifica_id, (id_cliente,), fetch_one=True)
            if resultado:
                set_campos = f", ".join([f"{campo} = %s" for campo in campos.keys()])
                query_update = f"UPDATE formulario_cliente SET {set_campos} WHERE id = %s"
                valores = list(campos.values())+ [id_cliente]
                resultado = db.execute_query(query_update, valores, commit=True)
                if resultado:
                    query_buscar_cliente = "SELECT * FROM formulario_cliente WHERE id = %s"
                    cliente_atualizado = db.execute_query(query_buscar_cliente, (id_cliente,), fetch_one=True)
                    print(FormularioCliente.formatar_cliente(cliente_atualizado))
                    return resultado
                else:
                    print(f"Nenhum cliente atualizado")
                    return None
            else:
                print(f"ID inexistente")
                return None
        except Exception as e:
            print(f"Erro ao atualizar cliente: {e}")
            return None
        finally:
            db.disconnect()

    @staticmethod
    def desativar_cliente(id_cliente):
        try:
            db = Database()
            verifica_id = "SELECT * FROM formulario_cliente WHERE id = %s"
            resultado = db.execute_query(verifica_id, (id_cliente,), fetch_one=True)
            if resultado:
                query_desativar = "UPDATE formulario_cliente SET ativo = FALSE WHERE id = %s"
                resultado_2 = db.execute_query(query_desativar, (id_cliente, ), commit=True)
                if resultado_2:
                    print(FormularioCliente.formatar_cliente(resultado))
                    return resultado
                else:
                    print(f"Nenhum cliente atualizado")
                    return None
            else:
                print(f"Não há nenhum cliente registrado com esse id")
        except Exception as e:
            print(f"Erro ao desativar cliente: {e}")
            return None
        finally:
            db.disconnect()

    @staticmethod
    def validar_cpf(cpf):
        try:
            # Remove pontos, traços e espaços
            cpf = ''.join(filter(str.isdigit, cpf))

            # Verifica se tem 11 dígitos
            if len(cpf) != 11:
                return False

            # Verifica se todos os dígitos são iguais (111.111.111-11)
            if cpf == cpf[0] * 11:
                return False

            # Calcula primeiro dígito verificador
            soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
            dig1 = 11 - (soma1 % 11)
            if dig1 >= 10:
                dig1 = 0

            # Calcula segundo dígito verificador
            soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
            dig2 = 11 - (soma2 % 11)
            if dig2 >= 10:
                dig2 = 0

            # Verifica se os dígitos calculados conferem
            return int(cpf[9]) == dig1 and int(cpf[10]) == dig2

        except:
            return False

    @staticmethod
    def validar_email(email):
        try:
            import re

            # Regex simples mas eficiente
            regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            return re.match(regex, email) is not None

        except:
            return False

    @staticmethod
    def validar_dados(dados_cliente):
        erros = []

        # Validar nome
        if len(dados_cliente.get('nome_completo', '')) < 3:
            erros.append("Nome deve ter pelo menos 3 caracteres")

        # Validar telefone
        telefone = dados_cliente.get('telefone', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if len(telefone) < 10 or len(telefone) > 11:
            erros.append("Telefone deve ter 10 ou 11 dígitos")

        # Validar email
        if not FormularioCliente.validar_email(dados_cliente.get('email', '')):
            erros.append("Email inválido")

        # Validar CPF
        if not FormularioCliente.validar_cpf(dados_cliente.get('cpf', '')):
            erros.append("CPF inválido")

        # Validar endereço
        if len(dados_cliente.get('localizacao_exata', '')) < 10:
            erros.append("Endereço deve ter pelo menos 10 caracteres")

        return {
            'valido': len(erros) == 0,
            'erros': erros
        }

