from Banco2 import Banco
import pandas as pd
import tkinter.filedialog as fdlg

def writeTofile(self,data, filename):
  # Convert binary data to proper format and write it on Hard Disk
  with open(filename, 'wb') as file:
    file.write(data)

class Usuarios(object):


  def __init__(self, cpf = "", nome = "", casa = "",
  rg = "", email = "", fone = "", placa = "", modelo = "",fluxo= "", data = "",foto=""):
    self.info = {}
    #self.idusuario = idusuario
    self.cpf = cpf
    self.nome = nome
    self.casa = casa
    self.rg = rg
    self.email = email
    self.fone = fone
    self.placa = placa
    self.modelo = modelo
    self.fluxo = fluxo
    self.data = data
    self.foto = foto
    
    


  def insertUser(self):

    banco = Banco()
    try:
      c = banco.conexao.cursor()

      minha_query = """INSERT INTO morador (cpf, nome, casa, rg, email, fone, placa, modelo, fluxo, data, foto) VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
      
      # Convert data into tuple format
      data_tuple = (self.cpf, self.nome, self.casa, self.rg, self.email, self.fone, self.placa, self.modelo, self.fluxo, self.data, self.foto)

      c.execute(minha_query, data_tuple)



      banco.conexao.commit()
      c.close()


      return " Registrado com sucesso!"
    except:
      return "Atenção: Ocorreu um erro na inserção do usuário"

  def updateUser(self):

    banco = Banco()
    try:

        c = banco.conexao.cursor()

        c.execute("UPDATE morador SET nome = '" + self.nome + "',  casa = '" + self.casa + "', rg = '" + self.rg +
        "', email = '" + self.email + "', fone = '" + self.fone +
        "' , placa = '" + self.placa + "', modelo = '" + self.modelo + "' , fluxo = '" + self.fluxo + "', data = '" + self.data + "' WHERE cpf = '" + self.cpf + "' ")

        '''"UPDATE  morador set WHERE cpf = '" + self.cpf +
       "', nome = '" + self.nome + "', casa = '" + self.casa + "', rg = '" + self.rg + "' , email ='" + self.email + "', fone ='" + self.fone 
       + "', placa='" + self.placa + "', modelo='" + self.modelo + "', data='" + self.data + " ")'''

        banco.conexao.commit()
        c.close()

        return "Usuário atualizado com sucesso!"
    except:
        return "Ocorreu um erro na alteração do usuário"

 
  def deleteUser(self):

    banco = Banco()
    try:

        c = banco.conexao.cursor()

        c.execute("delete from morador where cpf = '" + self.cpf + "' ")

        banco.conexao.commit()
        c.close()

        return "Usuário excluído com sucesso!"
    except:
        return "Ocorreu um erro na exclusão do usuário"



  def selectUser(self, pesquisandou,pesquisado,tb_movimento):
    banco = Banco()
    try:

        c = banco.conexao.cursor()

        c.execute("SELECT * FROM morador WHERE " + pesquisandou + " = '" + pesquisado + "' ORDER BY data DESC")

        #lista = c.FETCHALL()
        #lista=c.execute("""SELECT cpf, nome, casa, rg, email, fone, placa, modelo, data FROM morador ORDER BY nome ASC """)
        tb_movimento.delete(*tb_movimento.get_children())
        for linha in c:
            self.cpf = linha[0]
            self.nome = linha[1]
            self.casa = linha[2]
            self.rg = linha[3]
            self.email = linha[4]
            self.fone = linha[5]
            self.placa=linha[6]
            self.modelo=linha[7]
            self.fluxo=linha[8]
            self.data=linha[9]
            self.foto=linha[10]
            cpf_mudado = self.cpf.replace(self.cpf[0:5],"*****")
            tb_movimento.insert("","end",values=(cpf_mudado,self.nome,self.fluxo,self.data))
            if self.foto !="":
              self.photoPath = "./arq_fotos\\" + self.cpf + ".jpg"
              writeTofile(self,self.foto, self.photoPath)
            else:
              self.photoPath='./arquivos/foto.png'
        c.close()
        return "Busca feita com sucesso!"
    except banco.conexao.Error as error:
        return "Ocorreu um erro na busca do usuário"

  def relatorios(self,tela_adm):
    try:
      banco = Banco()
      c = banco.conexao.cursor()
      df=pd.read_sql_query("""SELECT * FROM morador ORDER BY data DESC""",banco.conexao)
      c.close()
      opcoes = {}                # as opções são definidas em um dicionário
      opcoes['initialdir'] = ''    # será o diretório atual
      opcoes['parent'] = tela_adm
      opcoes['title'] = 'Escolha um local para salvar'
      caminhoinicial = fdlg.askdirectory(**opcoes)
      df.to_excel(caminhoinicial +'/Relatorio Movimentos MB_Portaria.xlsx', index=False)
      return "Gerado com sucesso!"
    except banco.conexao.Error as error:
        return "Ocorreu um erro na busca do usuário"


 