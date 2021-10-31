#importando módulo do SQlite
import sqlite3

class Banco():

    def __init__(self):
        self.veriferro = sqlite3
        self.conexao = sqlite3.connect('banco.db')
        self.createTable()

    def createTable(self):
        c = self.conexao.cursor()

        c.execute("""create table if not exists morador (
                     cpf text,
                     nome text,
                     casa text,
                     rg text,
                     email text,
                     fone text,
                     placa text,
                     modelo text,
                     fluxo text,
                     data text,
                     foto BLOB,
                     idusuario integer primary key autoincrement)""")
        self.conexao.commit()
        c.close()
