import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.config = {
            'host': 'prancheta-db.cgz4mmcgy3ns.us-east-1.rds.amazonaws.com',
            'user': 'admin',
            'password': 'awsm1944',
            'database': 'moveis_metalon_samarone'
        }

        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
                self.cursor = self.connection.cursor(buffered=True)
                print(f"Mysql conectado com sucesso!")
                return True
            else:
                return False
        except Error as e:
            print(f"Erro ao conectar Mysql: {e}")
            return False

    def disconnect(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()

            self.connection = None
            self.cursor = None

            print(f"Mysql desconectado com sucesso!")
        except Error as e:
            print(f"Erro ao desconectar Mysql: {e}")
    def execute_query(self, query, params=None, fetch_one = False, commit = False):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()

            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                if fetch_one:
                    return self.cursor.fetchone()
                else:
                    return self.cursor.fetchall()
            if commit:
                self.connection.commit()

            return True
        except Error as e:
            print(f"Erro ao executar query: {e}")
            return None


if __name__ == "__main__":
    db = Database()

    '''db.execute_query("INSERT INTO moveis (nome, descricao, materiais, imagem_url) VALUES (%s, %s, %s, %s)", params=[
                            "Mesa Cubo Mágico",
                            "Essa mesa é feita com uma ilusão de optica lembrando um pouco um cubo mágico! Você pode colocar ela em qualquer posição e em todas ela terá uma base de apoio.",
                            "O material desse móvel é feito de metalon e vidro. Mas você também pode solicitar o mesmo movel feito de metalon e madeira.",
                            "Colocar URL"
                            ],
                     commit=True)'''

    db.execute_query("DELETE FROM moveis WHERE id = %s", params=(4,), commit=True)


    print("=== BUSCAR MÓVEIS ===")
    # Use fetchall() em vez de fetch_one=True
    resultados = db.execute_query("SELECT * FROM moveis", fetch_one= False)  # ← Lista de tuplas

    if not resultados:
        print("Nenhum móvel encontrado!")

    elif resultados == db.execute_query("SELECT * FROM moveis", fetch_one= True):
        print(f"\n--- MÓVEL---")
        print(f"ID: {resultados[0]}")
        print(f"Nome: {resultados[1]}")
        print(f"Descrição: {resultados[2]}")
        print(f"Material: {resultados[3]}")
        print(f"Destaque: {resultados[5]}")


    else:
        print(f"=== {len(resultados)} MÓVEIS ===")
        for i, movel in enumerate(resultados):  # ← Agora movel é uma tupla!
            print(f"\n--- MÓVEL {i + 1} ---")
            print(f"ID: {movel[0]}")
            print(f"Nome: {movel[1]}")
            print(f"Descrição: {movel[2]}")
            print(f"Material: {movel[3]}")
            print(f"Destaque: {movel[5]}")

    db.disconnect()