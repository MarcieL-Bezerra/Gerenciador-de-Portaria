import sqlite3

class Banco():

    def __init__(self):
        self.conexao = sqlite3.connect('SQLite_Python.db')
        self.createTable()

    def createTable(self):
        c = self.conexao.cursor()

        c.execute("""create table if not exists new_employee ( 
        	nomes TEXT NOT NULL, 
        	fotos BLOB NOT NULL, 
        	resumos TEXT NOT NULL,
        	id INTEGER PRIMARY KEY autoincrement)""")
        self.conexao.commit()
        c.close()

