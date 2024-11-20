import mysql.connector

def conectar_banco():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pmp" 
        )
        cursor = mydb.cursor()
        print("Conexão bem-sucedida!") 
        return mydb, cursor
    except mysql.connector.Error as err:
        print(f"Erro na conexão: {err}")
        return None, None

if __name__ == "__main__":
    mydb, cursor = conectar_banco()

    if mydb is None or cursor is None:
        print("Erro: Não foi possível conectar ao banco de dados.")
    else:
        print("Conexão com sucesso!")
