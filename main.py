from Usuarios2 import Usuarios
from tkinter import *
import tkinter as tk
from tkinter import ttk
import threading
import tkinter.messagebox as tkMessageBox
from datetime import datetime, timedelta
import validacpf as CpfValid
import tkinter.filedialog as fdlg
import os
from PIL import ImageTk, Image
import login 

login.cpf_buscado = ""
login.nome_buscado = ""
login.email_buscado = ""
login.senha_buscado = ""

caminhoinicial = './arq_fotos'
files = os.listdir(caminhoinicial)

files_jpg =[caminhoinicial + '\\' + f for f in files if f[-3:]== 'jpg']

for f in files_jpg:
    os.remove(f)


def saindo():
	result = tkMessageBox.askquestion("", "Confirma a saída?", icon='question')
	if result=='yes':
		os._exit(1)
	else:
		pass

def limpar(tela):
	btn_cadastro.config(state='normal')
	btn_visitante.config(state='normal')
	btn_pesquisar.config(state='normal')
	btn_saidas.config(state='normal')
	if tela=='morador':
		tela_cadastro.destroy()
	elif tela =='visitante':
		tela_cadastrov.destroy()
		#btn_pesquisarp.focus_set()
	elif tela == 'pesquisa':
		tela_cadastrop.destroy()
	elif tela == 'adm':
		tela_adm.destroy()

def convert_pic(filename):
	#aqui converte arquivo para bit 'BLOB' para o sqlite
	with open(filename,'rb') as file:
		minha_foto=file.read()
	return minha_foto

def imgNaTela(local, localizacao):
	#cria o canvas para colocar imagem
	canvas_for_image = Canvas(local, bg='MediumTurquoise', height=200, width=200, borderwidth=0, highlightthickness=0)
	canvas_for_image.place(relx=0.8, rely = 0.16)

	# cria a imagem e redimensiona para colocar no canvass
	image = Image.open(localizacao)
	canvas_for_image.image = ImageTk.PhotoImage(image.resize((200, 200), Image.ANTIALIAS))
	canvas_for_image.create_image(0, 0, image=canvas_for_image.image, anchor='nw')

def reali_cadstro():
	#cadastra o morador no bd´depois de validar alguns dados
	user = Usuarios()
	data_atual = datetime.now()
	data_atual = data_atual.strftime('%d/%m/%Y %H:%M:%S')
	user.cpf = txt_cpf.get()
	user.nome = txt_nome.get()
	user.casa = txt_bloco.get()
	user.rg = txt_rg.get()
	user.email = txt_email.get()
	user.fone = txt_fone.get()
	user.placa = txt_placa.get()
	user.modelo=txt_model.get()
	user.fluxo = "Cadastro"
	user.data = data_atual
	user.foto=convert_pic(localidade)
	resposta = user.insertUser()


	txt_cpf.delete(0, END)
	txt_nome.delete(0, END)
	txt_bloco.delete(0, END)
	txt_rg.delete(0, END)
	txt_email.delete(0, END)
	txt_fone.delete(0,END)
	txt_placa.delete(0, END)
	txt_model.delete(0, END)
		
	txt_data.config(text=data_atual)
	imgNaTela(tela_cadastro,'./arquivos/foto.png')
	

	btn_cadastro.config(state='normal')
	btn_visitante.config(state='normal')
	btn_pesquisar.config(state='normal')
	btn_saidas.config(state='normal')
	tela_cadastro.destroy()

	tkMessageBox.showinfo('Resposta', message=user.fluxo + resposta)

def reali_cadstrov():
	#cadastra visitantes depois de validar dados
	user = Usuarios()
	data_atual = datetime.now()
	data_atual = data_atual.strftime('%d/%m/%Y %H:%M:%S')
	user.cpf = txt_cpf.get()
	user.nome = txt_nome.get()
	user.casa = txt_bloco.get()
	user.rg = txt_rg.get()
	user.email = txt_tipo.get()
	user.fone = txt_fone.get()
	user.placa = txt_placa.get()
	user.modelo=txt_model.get()
	user.fluxo = comboFluxo.get()
	user.data = data_atual

	resposta = user.insertUser()

	txt_cpf.delete(0, END)
	txt_nome.delete(0, END)
	txt_bloco.delete(0, END)
	txt_rg.delete(0, END)
	txt_tipo.delete(0, END)
	txt_fone.delete(0,END)
	txt_placa.delete(0, END)
	txt_model.delete(0, END)
	tb_movimento.delete(*tb_movimento.get_children())	
	txt_data.config(text=data_atual)

	tkMessageBox.showinfo('Resposta', message= user.fluxo + resposta)

def alter_cadstro():
	#altera dados de moradores e visitantes cadastrados
	user = Usuarios()

	data_atual = datetime.now()
	data_atual = data_atual.strftime('%d/%m/%Y %H:%M')


	user.cpf = txt_cpf.get()
	user.nome = txt_nome.get()
	user.casa = txt_bloco.get()
	user.rg = txt_rg.get()
	user.email = txt_tipo.get()
	user.fone = txt_fone.get()
	user.placa = txt_placa.get()
	user.modelo=txt_model.get()
	user.data = data_atual


	resposta = user.updateUser()

	txt_cpf.delete(0, END)
	txt_nome.delete(0, END)
	txt_bloco.delete(0, END)
	txt_rg.delete(0, END)
	txt_tipo.delete(0, END)
	txt_fone.delete(0,END)
	txt_placa.delete(0, END)
	txt_model.delete(0, END)
	txt_data.config(text="")

	tkMessageBox.showinfo('Resposta', message=resposta)

def buscarUsuario():
	#busca no banco moradores e visitantes pelo cpf ou casa ou veiculo
	user = Usuarios()

	pesquisado = pesquisadop
	pesquisandou = pesquisandop

	resposta = user.selectUser(pesquisandou=pesquisandou,pesquisado=pesquisado,tb_movimento=tb_movimento)

	
	if user.cpf=="":
		tkMessageBox.showerror(resposta,message="Nada encontrado!")
	else:
		txt_cpf.delete(0, END)
		txt_cpf.insert(INSERT, user.cpf)
		txt_nome.delete(0, END)
		txt_nome.insert(INSERT, user.nome)
		txt_bloco.delete(0, END)
		txt_bloco.insert(INSERT, user.casa)
		txt_rg.delete(0, END)
		txt_rg.insert(INSERT, user.rg)
		txt_tipo.delete(0, END)
		txt_tipo.insert(INSERT, user.email)
		txt_fone.delete(0,END)
		txt_fone.insert(INSERT, user.fone)
		txt_placa.delete(0, END)
		txt_placa.insert(INSERT, user.placa)
		txt_model.delete(0, END)
		txt_model.insert(INSERT, user.modelo)
		txt_data.config(text=user.data)
		imgNaTela(tela_cadastrop,user.photoPath)
		
		#image2=user.foto
		#lbl_fotos.config(image=image2)
		#lbl_fotos.image = image2
	
		tkMessageBox.showinfo('Resposta', message=resposta)

def reali_cadstroAdm():
	#cadastra o morador no bd´depois de validar alguns dados
	user = Usuarios()

	cpf = txt_cpfa.get()
	nome = txt_nomea.get()
	email = txt_emaila.get()
	tipo = comboTipo.get()
	senha = txt_senhaa.get()
	
	resposta = login.insertUser(cpf,nome,email,tipo,senha)


	txt_cpfa.delete(0, END)
	txt_nomea.delete(0, END)
	txt_emaila.delete(0, END)
	txt_senhaa.delete(0, END)
	txt_senhaac.delete(0, END)

	

	tkMessageBox.showinfo('Resposta', message=resposta)

def buscarUsuarioAdm():
	#busca no banco moradores e visitantes pelo cpf ou casa ou veiculo
	#user = Usuarios()

	cpfau = txt_cpfa.get()
	resposta = login.selectUser(cpfau)

	
	if login.cpf_buscado=="":
		tkMessageBox.showerror(resposta,message="Nada encontrado!")
	else:
		txt_cpfa.delete(0, END)
		txt_cpfa.insert(INSERT, login.cpf_buscado)
		txt_nomea.delete(0, END)
		txt_nomea.insert(INSERT, login.nome_buscado)
		#comboTipo.delete(0, END)
		comboTipo.set(login.tipo_buscado)
		txt_emaila.delete(0, END)
		txt_emaila.insert(INSERT, login.email_buscado)
		txt_senhaa.delete(0, END)
		txt_senhaa.insert(INSERT, login.senha_buscado)
		txt_senhaac.delete(0, END)
		txt_senhaac.insert(INSERT, login.senha_buscado)
		
		login.cpf_buscado = ""
		login.nome_buscado = ""
		login.email_buscado = ""
		login.senha_buscado = ""


	
		#tkMessageBox.showinfo('Resposta', message=resposta)

def excluirUsuarioAdm():
	#exclui morador ou visitante pelo cpf

	cpf = txt_cpfa.get()

	if cpf == "":
		tkMessageBox.showerror('Não é Permitido Vazio',message='Favor verifique o CPF')
	else:
		resposta = login.deleteUser(cpf)

		txt_cpfa.delete(0, END)
		txt_nomea.delete(0, END)
		txt_emaila.delete(0, END)
		txt_senhaa.delete(0, END)
		txt_senhaac.delete(0, END)
	

		tkMessageBox.showinfo('Resposta', message=resposta)

def excluirUsuario():
	#exclui morador ou visitante pelo cpf

	user = Usuarios()

	user.cpf = txt_cpf.get()

	resposta = user.deleteUser()

	txt_cpf.delete(0, END)
	txt_nome.delete(0, END)
	txt_bloco.delete(0, END)
	txt_rg.delete(0, END)
	txt_tipo.delete(0, END)
	txt_fone.delete(0,END)
	txt_placa.delete(0, END)
	txt_model.delete(0, END)
	txt_data.config(text='')
	imgNaTela(tela_cadastrop,'./arquivos/foto.png')

	tkMessageBox.showinfo('Resposta', message=resposta)

def reali_pesquisa_usuarios():
	#valida os dados para realizar a pesquisa
	cpf = txt_cpfa.get()
	validado = CpfValid.isCpfValid(cpf)

	#if validado == False:
	#	tkMessageBox.showerror('Erro CPF', message='O CPF digitado não é válido')
	if validado != False:
		buscarUsuarioAdm()
		#tkMessageBox.showerror('Sim',message='Buscado CPF')
	else:
		tkMessageBox.showerror('Não é Permitido Vazio',message='Favor verifique o CPF')

def rel_cadastarUsuarioAdm():
	#valida dados de moradores para cadastrar
	cpf = txt_cpfa.get()
	nome=txt_nomea.get()
	email = txt_emaila.get()
	tipo = comboTipo.get()
	senha = txt_senhaa.get()
	senhac = txt_senhaac.get()
	
	validado = CpfValid.isCpfValid(cpf)
	
	if validado == False:
		tkMessageBox.showerror('Erro CPF', message='O CPF digitado não é válido')
	elif senhac != senha:
		tkMessageBox.showerror('Confirmação de senhas',message='As senhas informadas não conferem!')	
	elif nome == "" or email =="" or tipo =="" or senha =="":
		tkMessageBox.showerror('Não é Permitido Vazio',message='Favor cadastrar todos os campos com *')			
	else:
		reali_cadstroAdm()

def reali_pesquisa():
	#valida os dados para realizar a pesquisa
	global pesquisadop
	global pesquisandop
	cpf = txt_cpf.get()
	casa = txt_bloco.get()
	placa = txt_placa.get()		
	validado = CpfValid.isCpfValid(cpf)

	#if validado == False:
	#	tkMessageBox.showerror('Erro CPF', message='O CPF digitado não é válido')
	if validado != False:
		pesquisadop=cpf
		pesquisandop='cpf'
		buscarUsuario()
	elif  casa != "":
		pesquisadop=casa
		pesquisandop='casa'
		buscarUsuario()
	elif placa !="":
		pesquisadop=placa
		pesquisandop='placa'
		buscarUsuario()
	else:
		tkMessageBox.showerror('Não é Permitido Vazio',message='Favor escolher um dos campos com *\n\n a ser pesquisado ou verifique o CPF')

def rel_alterar():
	#valida dados para alterar
	cpfr = txt_cpf.get()
	nomer=txt_nome.get()
	casar = txt_bloco.get()
	placar = txt_placa.get()
	rgr = txt_rg.get()
	emailr=txt_tipo.get()
	foner = txt_fone.get()
	modelor = txt_model.get()
	validador = CpfValid.isCpfValid(cpfr)
	
	if validador == False:
		tkMessageBox.showerror('Erro CPF', message='O CPF digitado não é válido')
	elif casar == "" or placar =="" or nomer =="" or rgr =="" or emailr =="" or foner =="" or modelor =="":
		tkMessageBox.showerror('Não é Permitido Vazio',message='Favor cadastrar todos os campos com *')			
	else:
		alter_cadstro()
	
def rel_cadastar():
	#valida dados de moradores para cadastrar
	cpf = txt_cpf.get()
	nome=txt_nome.get()
	casa = txt_bloco.get()
	placa = txt_placa.get()
	rg = txt_rg.get()
	email=txt_email.get()
	fone = txt_fone.get()
	modelo = txt_model.get()
	validado = CpfValid.isCpfValid(cpf)
	
	if validado == False:
		tkMessageBox.showerror('Erro CPF', message='O CPF digitado não é válido')
	elif casa == "" or placa =="" or nome =="" or rg =="" or email =="" or fone =="" or modelo =="":
		tkMessageBox.showerror('Não é Permitido Vazio',message='Favor cadastrar todos os campos com *')			
	else:
		reali_cadstro()

def rel_cadastarv():
	#valida dados de visitantes para cadastrar
	cpfv = txt_cpf.get()
	nome=txt_nome.get()
	casa = txt_bloco.get()
	placa = txt_placa.get()
	rg = txt_rg.get()
	email=txt_tipo.get()
	fone = txt_fone.get()
	modelo = txt_model.get()
	validado = CpfValid.isCpfValid(cpfv)
	
	if validado == False:
		tkMessageBox.showerror('Erro CPF', message='O CPF digitado não é válido')
	elif casa == "" or placa =="" or nome =="" or rg =="" or email =="" or fone =="" or modelo =="":
		tkMessageBox.showerror('Não é Permitido Vazio',message='Favor escolher campo\n\n a ser CADASTRADO')			
	else:
		reali_cadstrov()		

def reali_exclusao():
	#valida dados de moradores e visitantes para excluir
	cpf = txt_cpf.get()
	nome=txt_nome.get()
	casa = txt_bloco.get()
	placa = txt_placa.get()
	rg = txt_rg.get()
	email=txt_tipo.get()
	fone = txt_fone.get()
	modelo = txt_model.get()	
	validado = CpfValid.isCpfValid(cpf)

	#if validado == False:
	#	tkMessageBox.showerror('Erro CPF', message='O CPF digitado não é válido')
	if cpf== "" or casa == "" or placa =="" or nome =="" or rg =="" or email =="" or fone =="" or modelo =="":
		tkMessageBox.showerror('Não é Permitido Vazio',message='Favor escolher campo\n\n a ser EXCLUÍDO')			
	else:
		result = tkMessageBox.askquestion("", "Confirma a exclusão?", icon='warning')
		if result=='yes':
			excluirUsuario()
		else:
			pass
			


def chek_morador():
	chkvarcpf = radionbuton.get()
	if chkvarcpf == 1:
		lbl_tipop.config(text='Email')
		comboFluxo.place(relx=150, rely = 150)
		lbl_tipoa.place(relx=150, rely = 150)
	elif chkvarcpf == 2:
		lbl_tipop.config(text='Tipo')
		comboFluxo.place(relx=0.65, rely = 0.51)
		lbl_tipoa.place(relx=0.55, rely = 0.50)
	
def enter_apert(event):
	reali_pesquisa()

def gerarrel(valor):
	user = Usuarios()
	resposta = user.relatorios(valor)
	tkMessageBox.showinfo('Resposta', message=resposta)

def tela_morador():

	global txt_nome
	global txt_cpf
	global txt_bloco
	global txt_rg
	global txt_email
	global txt_fone
	global txt_placa
	global txt_model
	data_atual = datetime.now()
	data_atual = data_atual.strftime('%d/%m/%Y %H:%M:%S')
	btn_cadastro.config(state='disabled')
	btn_visitante.config(state='disabled')
	btn_pesquisar.config(state='disabled')
	btn_saidas.config(state='disabled')
	#cadastros de morador
	global tela_cadastro
	tela_cadastro = Frame(tinicial,width=w*0.9, height=h*0.8,bg ='MediumTurquoise')
	tela_cadastro.place(relx=0.02, rely = 0.10)

	lbl_menu=Label(tela_cadastro,width=20,bd=4, height=1,bg ='MediumTurquoise',text= 'Cadastro de Morador',fg='black',font=('arial',25,'bold'))
	lbl_menu.place(relx=0.2, rely = 0.02)

	lbl_nome=Label(tela_cadastro,width=13,bd=4, height=2,bg ='MediumTurquoise',text= 'Nome Completo *',fg='black',font=('arial',14,'bold'))
	lbl_nome.place(relx=0.05, rely = 0.15)			
	txt_nome = Entry(tela_cadastro,width=23,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_nome.place(relx=0.23, rely = 0.16)

	lbl_cpf=Label(tela_cadastro,width=4,bd=4, height=2,bg ='MediumTurquoise',text= 'CPF *',fg='black',font=('arial',14,'bold'))
	lbl_cpf.place(relx=0.55, rely = 0.15)			
	txt_cpf = Entry(tela_cadastro,width=11,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_cpf.place(relx=0.65, rely = 0.16)

	lbl_bloco=Label(tela_cadastro,width=8,bd=4, height=2,bg ='MediumTurquoise',text= 'Casa-APT *',fg='black',font=('arial',14,'bold'))
	lbl_bloco.place(relx=0.05, rely = 0.25)			
	txt_bloco = Entry(tela_cadastro,width=23,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_bloco.place(relx=0.23, rely = 0.26)

	lbl_rg=Label(tela_cadastro,width=3,bd=4, height=2,bg ='MediumTurquoise',text= 'RG *',fg='black',font=('arial',14,'bold'))
	lbl_rg.place(relx=0.55, rely = 0.25)			
	txt_rg = Entry(tela_cadastro,width=11,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_rg.place(relx=0.65, rely = 0.26)

	lbl_email=Label(tela_cadastro,width=5,bd=4, height=2,bg ='MediumTurquoise',text= 'Email *',fg='black',font=('arial',14,'bold'))
	lbl_email.place(relx=0.05, rely = 0.35)
	txt_email = Entry(tela_cadastro,width=23,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_email.place(relx=0.23, rely = 0.36)

	lbl_fone=Label(tela_cadastro,width=4,bd=4, height=2,bg ='MediumTurquoise',text= 'Fone *',fg='black',font=('arial',14,'bold'))
	lbl_fone.place(relx=0.55, rely = 0.35)
	txt_fone = Entry(tela_cadastro,width=11,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_fone.place(relx=0.65, rely = 0.36)
	
	lbl_placa=Label(tela_cadastro,width=5,bd=4, height=2,bg ='MediumTurquoise',text= 'Placa *',fg='black',font=('arial',14,'bold'))
	lbl_placa.place(relx=0.05, rely = 0.45)
	txt_placa = Entry(tela_cadastro,width=23,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_placa.place(relx=0.23, rely = 0.46)
	#txt_placa.config(state='disabled')

	lbl_model=Label(tela_cadastro,width=6,bd=4, height=2,bg ='MediumTurquoise',text= 'Modelo *',fg='black',font=('arial',14,'bold'))
	lbl_model.place(relx=0.55, rely = 0.45)
	txt_model = Entry(tela_cadastro,width=11,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_model.place(relx=0.65, rely = 0.46)
	#txt_model.config(state='disabled')
	global txt_data
	lbl_data=Label(tela_cadastro,width=9,bd=4, height=2,bg ='MediumTurquoise',text= 'Data/Hora',fg='black',font=('arial',14,'bold'))
	lbl_data.place(relx=0.05, rely = 0.55)
	txt_data = Label(tela_cadastro,width=21,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_data.place(relx=0.23, rely = 0.56)
	txt_data.config(text=data_atual)
	#txt_datav.insert(0,data_atual)
	txt_data.config(state='disabled')



	btn_cadastrar = Button(tela_cadastro,bg='DodgerBlue',bd=6,image=cadastrarimg ,compound = LEFT, text="Cadastrar", fg='black',font=('arial',14,'bold'),command=rel_cadastar)
	btn_cadastrar.place(relx=0.05, rely = 0.7)

	btn_saidasm = Button(tela_cadastro,bg='DodgerBlue',bd=6,image=voltarimg ,compound = LEFT, text="Voltar", fg='black',font=('arial',14,'bold'),command=lambda: limpar('morador'))
	btn_saidasm.place(relx=0.6, rely = 0.7)

	
	#foto no frame
	global localidade
	localidade=fdlg.askopenfilename()
	if localidade=="":
		tkMessageBox.showerror("Atenção", message="Não é permitido cadastro de\n morador sem foto!")
		btn_cadastro.config(state='normal')
		btn_visitante.config(state='normal')
		btn_pesquisar.config(state='normal')
		btn_saidas.config(state='normal')
		tela_cadastro.destroy()
	else:
		imgNaTela(tela_cadastro,localidade)
	

def tela_visitante():
	global txt_nome
	global txt_cpf
	global txt_bloco
	global txt_rg
	global txt_tipo
	global txt_fone
	global txt_placa
	global txt_model
	global comboFluxo
	data_atual = datetime.now()
	data_atual = data_atual.strftime('%d/%m/%Y %H:%M:%S')
	btn_cadastro.config(state='disabled')
	btn_visitante.config(state='disabled')
	btn_pesquisar.config(state='disabled')
	btn_saidas.config(state='disabled')
	#cadastros de visitante
	global tela_cadastrov
	tela_cadastrov = Frame(tinicial,width=w*0.9, height=h*0.8,bg ='Turquoise')
	tela_cadastrov.place(relx=0.02, rely = 0.10)
	lbl_menuv=Label(tela_cadastrov,width=20,bd=4, height=1,bg ='Turquoise',text= 'Cadastro de Visitante',fg='black',font=('arial',25,'bold'))
	lbl_menuv.place(relx=0.3, rely = 0.03)

	lbl_nomev=Label(tela_cadastrov,width=13,bd=4, height=2,bg ='Turquoise',text= 'Nome Completo *',fg='black',font=('arial',14,'bold'))
	lbl_nomev.place(relx=0.05, rely = 0.15)
	txt_nome = Entry(tela_cadastrov,width=23,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_nome.place(relx=0.23, rely = 0.16)

	lbl_cpfv=Label(tela_cadastrov,width=4,bd=4, height=2,bg ='Turquoise',text= 'CPF *',fg='black',font=('arial',14,'bold'))
	lbl_cpfv.place(relx=0.55, rely = 0.15)
	txt_cpf = Entry(tela_cadastrov,width=11,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_cpf.place(relx=0.65, rely = 0.16)

	lbl_blocov=Label(tela_cadastrov,width=8,bd=4, height=2,bg ='Turquoise',text= 'Casa-APT *',fg='black',font=('arial',14,'bold'))
	lbl_blocov.place(relx=0.05, rely = 0.25)
	txt_bloco = Entry(tela_cadastrov,width=23,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_bloco.place(relx=0.23, rely = 0.26)

	lbl_rgv=Label(tela_cadastrov,width=3,bd=4, height=2,bg ='Turquoise',text= 'RG *',fg='black',font=('arial',14,'bold'))
	lbl_rgv.place(relx=0.55, rely = 0.25)
	txt_rg = Entry(tela_cadastrov,width=11,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_rg.place(relx=0.65, rely = 0.26)

	lbl_tipov=Label(tela_cadastrov,width=14,bd=4, height=2,bg ='Turquoise',text= 'Tipo de Visitante *',fg='black',font=('arial',14,'bold'))
	lbl_tipov.place(relx=0.05, rely = 0.35)
	txt_tipo = Entry(tela_cadastrov,width=23,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_tipo.place(relx=0.23, rely = 0.36)

	lbl_fonev=Label(tela_cadastrov,width=4,bd=4, height=2,bg ='Turquoise',text= 'Fone *',fg='black',font=('arial',14,'bold'))
	lbl_fonev.place(relx=0.55, rely = 0.35)
	txt_fone = Entry(tela_cadastrov,width=11,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_fone.place(relx=0.65, rely = 0.36)

	lbl_placav=Label(tela_cadastrov,width=5,bd=4, height=2,bg ='Turquoise',text= 'Placa *',fg='black',font=('arial',14,'bold'))
	lbl_placav.place(relx=0.05, rely = 0.45)
	txt_placa = Entry(tela_cadastrov,width=23,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_placa.place(relx=0.23, rely = 0.46)
	#txt_placa.config(state='disabled')

	lbl_modelv=Label(tela_cadastrov,width=6,bd=4, height=2,bg ='Turquoise',text= 'Modelo *',fg='black',font=('arial',14,'bold'))
	lbl_modelv.place(relx=0.55, rely = 0.45)
	txt_model = Entry(tela_cadastrov,width=11,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_model.place(relx=0.65, rely = 0.46)
	#txt_model.config(state='disabled')


	lbl_tipoa=Label(tela_cadastrov,bd=4,bg ='DarkTurquoise',text= 'Registrar *',fg='black',font=('arial',14,'bold'))
	lbl_tipoa.place(relx=0.55, rely = 0.55)
	
	comboFluxo = ttk.Combobox(tela_cadastrov,values=["Entrada", "Saída"],state="readonly",font=('arial',14,'bold'))
	comboFluxo.place(relx=0.65, rely = 0.56)
	comboFluxo.current(0)

	global txt_data
	lbl_datav=Label(tela_cadastrov,width=9,bd=4, height=2,bg ='Turquoise',text= 'Data/Hora',fg='black',font=('arial',14,'bold'))
	lbl_datav.place(relx=0.05, rely = 0.55)
	txt_data = Label(tela_cadastrov,width=23,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_data.place(relx=0.23, rely = 0.56)
	txt_data.config(text=data_atual)
	#txt_datav.insert(0,data_atual)
	txt_data.config(state='disabled')
	


	btn_cadastrarv = Button(tela_cadastrov,bg='DodgerBlue',image=cadastrarimg ,compound = LEFT,bd=6, text="Cadastrar", fg='black',font=('arial',14,'bold'),command=rel_cadastarv)
	btn_cadastrarv.place(relx=0.02, rely = 0.7)

	btn_saidasv = Button(tela_cadastrov,bg='DodgerBlue',bd=6,image=voltarimg ,compound = LEFT, text="  Voltar   ", fg='black',font=('arial',14,'bold'),command=lambda: limpar('visitante'))
	btn_saidasv.place(relx=0.6, rely = 0.7)

def tela_pesquisa():
	#pesquisas
	global txt_nome
	global txt_cpf
	global txt_bloco
	global txt_rg
	global txt_tipo
	global txt_fone
	global txt_placa
	global txt_model
	global lbl_tipop
	global txt_data
	global lbl_fotos
	global comboFluxo
	global lbl_tipoa
	data_atual = datetime.now()
	data_atual = data_atual.strftime('%d/%m/%Y %H:%M:%S')
	btn_cadastro.config(state='disabled')
	btn_visitante.config(state='disabled')
	btn_pesquisar.config(state='disabled')
	btn_saidas.config(state='disabled')
	
	global tela_cadastrop
	tela_cadastrop = Frame(tinicial,width=w*0.9, height=h*0.8,bg ='DarkTurquoise')
	tela_cadastrop.place(relx=0.02, rely = 0.10)

	lbl_menup=Label(tela_cadastrop,width=20,bd=4, height=1,bg ='DarkTurquoise',text= 'Pesquisar Cadastros',fg='black',font=('arial',25,'bold'))
	lbl_menup.place(relx=0.4, rely = 0)

	lbl_nomep=Label(tela_cadastrop,width=13,bd=4, height=2,bg ='DarkTurquoise',text= 'Nome Completo',fg='black',font=('arial',14,'bold'))
	lbl_nomep.place(relx=0.55, rely = 0.10)
	txt_nome = Entry(tela_cadastrop,width=23,bd=4, bg ='white',cursor='X_cursor',fg='black',font=('arial',14,'bold'))
	txt_nome.place(relx=0.65, rely = 0.11)
	#txt_nome.config(state='disabled')

	lbl_cpfp=Label(tela_cadastrop,width=4,bd=4, height=2,bg ='DarkTurquoise',text= 'CPF *',fg='black',font=('arial',14,'bold'))
	lbl_cpfp.place(relx=0.05, rely = 0.10)
	txt_cpf = Entry(tela_cadastrop,width=11,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_cpf.place(relx=0.23, rely = 0.11)
	txt_cpf.bind('<Return>', enter_apert)

	
	lbl_blocop=Label(tela_cadastrop,width=8,bd=4, height=2,bg ='DarkTurquoise',text= 'Casa-APT *',fg='black',font=('arial',14,'bold'))
	lbl_blocop.place(relx=0.05, rely = 0.20)
	txt_bloco = Entry(tela_cadastrop,width=23,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_bloco.place(relx=0.23, rely = 0.21)
	txt_bloco.bind('<Return>', enter_apert)

	#txt_bloco.config(state='disabled')
	lbl_rgp=Label(tela_cadastrop,width=2,bd=4, height=2,bg ='DarkTurquoise',text= 'RG',fg='black',font=('arial',14,'bold'))
	lbl_rgp.place(relx=0.55, rely = 0.20)
	txt_rg = Entry(tela_cadastrop,width=11,bd=4, bg ='white',cursor='X_cursor',fg='black',font=('arial',14,'bold'))
	txt_rg.place(relx=0.65, rely = 0.21)
	#txt_rg.config(state='disabled')

	lbl_tipop=Label(tela_cadastrop,width=5,bd=4, height=2,bg ='DarkTurquoise',text= 'Email',fg='black',font=('arial',14,'bold'))
	lbl_tipop.place(relx=0.05, rely = 0.40)
	txt_tipo = Entry(tela_cadastrop,width=23,bd=4, bg ='white',cursor='X_cursor',fg='black',font=('arial',14,'bold'))
	txt_tipo.place(relx=0.23, rely = 0.41)
	#txt_tipo.config(state='disabled')

	lbl_fonep=Label(tela_cadastrop,width=4,bd=4, height=2,bg ='DarkTurquoise',text= 'Fone',fg='black',font=('arial',14,'bold'))
	lbl_fonep.place(relx=0.55, rely = 0.40)
	txt_fone = Entry(tela_cadastrop,width=11,bd=4, bg ='white',cursor='X_cursor',fg='black',font=('arial',14,'bold'))
	txt_fone.place(relx=0.65, rely = 0.41)
	#txt_fone.config(state='disabled')
	
	
	lbl_placap=Label(tela_cadastrop,width=5,bd=4, height=2,bg ='DarkTurquoise',text= 'Placa *',fg='black',font=('arial',14,'bold'))
	lbl_placap.place(relx=0.05, rely = 0.30)
	txt_placa = Entry(tela_cadastrop,width=23,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_placa.place(relx=0.23, rely = 0.31)
	txt_placa.bind('<Return>', enter_apert)
	#txt_placa.config(state='disabled')

	lbl_modelp=Label(tela_cadastrop,width=6,bd=4, height=2,bg ='DarkTurquoise',text= 'Modelo',fg='black',font=('arial',14,'bold'))
	lbl_modelp.place(relx=0.55, rely = 0.30)
	txt_model = Entry(tela_cadastrop,width=11,bd=4, bg ='white',cursor='X_cursor',fg='black',font=('arial',14,'bold'))
	txt_model.place(relx=0.65, rely = 0.31)
	#txt_model.config(state='disabled')
	
	lbl_datap=Label(tela_cadastrop,width=15,bd=4, height=2,bg ='DarkTurquoise',text= 'Data do Cadastro',fg='black',font=('arial',14,'bold'))
	lbl_datap.place(relx=0.05, rely = 0.50)
	txt_data = Label(tela_cadastrop,width=21,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_data.place(relx=0.23, rely = 0.51)
	txt_data.config(text=data_atual)
	#txt_datav.insert(0,data_atual)
	txt_data.config(state='disabled')

	lbl_tipoa=Label(tela_cadastrop,bd=4,bg ='DarkTurquoise',text= 'Registrar *',fg='black',font=('arial',14,'bold'))
	lbl_tipoa.place(relx=0.55, rely = 0.50)
	
	comboFluxo = ttk.Combobox(tela_cadastrop,values=["Entrada", "Saída"],state="readonly",font=('arial',14,'bold'))
	comboFluxo.place(relx=0.65, rely = 0.51)
	comboFluxo.current(0)

	global btn_pesquisarp
	btn_pesquisarp = Button(tela_cadastrop,bg='DodgerBlue',image=pesquisaimgbtn ,compound = LEFT,bd=8, text="Pesquisar", fg='black',font=('arial',14,'bold'))
	btn_pesquisarp.place(relx=0.05, rely = 0.7)
	btn_pesquisarp["command"] = reali_pesquisa

	btn_alterarp = Button(tela_cadastrop,bg='DodgerBlue',bd=8,image=alterarimgbtn ,compound = LEFT, text="Registrar", fg='black',font=('arial',14,'bold'),command=rel_cadastarv)
	btn_alterarp.place(relx=0.20, rely = 0.7)

	#btn_excluir = Button(tela_cadastrop,bg='DodgerBlue',image=alterarimgbtn ,compound = LEFT,bd=8, text="   Saída    ", fg='black',font=('arial',14,'bold'),command=rel_alterar)
	#btn_excluir.place(relx=0.45, rely = 0.7)

	btn_saidasp = Button(tela_cadastrop,bg='DodgerBlue',bd=8,image=voltarimg ,compound = LEFT, text="     Voltar     ", fg='black',font=('arial',14,'bold'),command=lambda: limpar('pesquisa'))
	btn_saidasp.place(relx=0.35, rely = 0.7)

	lbl_fotos=Label(tela_cadastrop,bd=4, image=image2,bg ='DarkTurquoise')
	lbl_fotos.place(relx=0.8, rely = 0.2)
	
	global radionbuton
	radionbuton = IntVar()
	radionbuton.set(2)
	R1 = Radiobutton(tela_cadastrop, text="Morador",bg="DodgerBlue", variable=radionbuton, value=1,command=chek_morador,font=('arial',14,'bold'))
	R1.place(relx=0.05, rely = 0.03)

	R2 = Radiobutton(tela_cadastrop, text="Visitante",bg="DodgerBlue", variable=radionbuton, value=2,command=chek_morador,font=('arial',14,'bold'))
	R2.place(relx=0.15, rely = 0.03)

	'''R3 = Radiobutton(tela_cadastrop, text="Dependente",bg="DodgerBlue", variable=radionbuton, value=3,command=chek_morador,font=('arial',14,'bold'))
	R3.place(relx=0.25, rely = 0.03)'''

	#tabela movimentos
	global tb_movimento

	frame = Frame(tela_cadastrop,bg='SkyBlue')
	frame.place(relx=0.5, rely = 0.65)
	titu_dep=Label(frame,width=25,bd=4,bg='SkyBlue', height=2,text= 'Entradas e Saídas',fg='black',font=('arial',14,'bold'))
	titu_dep.pack(side=TOP)
	tb_movimento = ttk.Treeview(frame, column=(1,2,3,4), show='headings', height=10)
	tb_movimento.pack(side=LEFT)
	#tb_movimento.heading('#0', text='', anchor=CENTER)
	tb_movimento.heading(1, text='Cpf')
	tb_movimento.heading(2, text='Nome')
	tb_movimento.heading(3, text='Registro')
	tb_movimento.heading(4, text='Data')
	sb = Scrollbar(frame, orient=VERTICAL)
	sb.pack(side=RIGHT, fill=Y)
	tb_movimento.config(yscrollcommand=sb.set)
	sb.config(command=tb_movimento.yview)
	style = ttk.Style()
	style.theme_use("default")
	style.map("Treeview")



def tela_adm():
	#pesquisas
	global txt_nomea
	global txt_cpfa
	global txt_emaila
	global comboTipo
	global txt_senhaa
	global txt_senhaac
	data_atual = datetime.now()
	data_atual = data_atual.strftime('%d/%m/%Y %H:%M:%S')
	btn_cadastro.config(state='disabled')
	btn_visitante.config(state='disabled')
	btn_pesquisar.config(state='disabled')
	btn_saidas.config(state='disabled')

	
	global tela_adm
	tela_adm = Frame(tinicial,width=w*0.9, height=h*0.8,bg ='DarkTurquoise')
	tela_adm.place(relx=0.02, rely = 0.10)

	lbl_menup=Label(tela_adm,width=20,bd=4, height=1,bg ='DarkTurquoise',text= 'Pesquisar Cadastros',fg='black',font=('arial',25,'bold'))
	lbl_menup.place(relx=0.4, rely = 0)

	lbl_nomea=Label(tela_adm,bd=4,bg ='DarkTurquoise',text= 'Nome Completo *',fg='black',font=('arial',14,'bold'))
	lbl_nomea.place(relx=0.55, rely = 0.10)
	txt_nomea = Entry(tela_adm,width=23,bd=4, bg ='white',cursor='X_cursor',fg='black',font=('arial',14,'bold'))
	txt_nomea.place(relx=0.65, rely = 0.11)
	#txt_nome.config(state='disabled')

	lbl_cpfa=Label(tela_adm,bd=4,bg ='DarkTurquoise',text= 'CPF *',fg='black',font=('arial',14,'bold'))
	lbl_cpfa.place(relx=0.05, rely = 0.10)
	txt_cpfa = Entry(tela_adm,width=11,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_cpfa.place(relx=0.23, rely = 0.11)
	#txt_cpfa.bind('<Return>', enter_apert)

	
	lbl_emaila=Label(tela_adm,bd=4,bg ='DarkTurquoise',text= 'Email *',fg='black',font=('arial',14,'bold'))
	lbl_emaila.place(relx=0.05, rely = 0.20)
	txt_emaila = Entry(tela_adm,width=23,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_emaila.place(relx=0.23, rely = 0.21)
	#txt_emaila.bind('<Return>', enter_apert)

	#txt_bloco.config(state='disabled')
	lbl_tipoa=Label(tela_adm,bd=4,bg ='DarkTurquoise',text= 'Tipo *',fg='black',font=('arial',14,'bold'))
	lbl_tipoa.place(relx=0.55, rely = 0.20)
	#txt_tipoa = Entry(tela_adm,width=11,bd=4, bg ='white',cursor='X_cursor',fg='black',font=('arial',14,'bold'))
	#txt_tipoa.place(relx=0.23, rely = 0.31)
	global comboTipo
	comboTipo = ttk.Combobox(tela_adm,values=["Usuário", "ADM"],state="readonly",font=('arial',14,'bold'))
	comboTipo.place(relx=0.65, rely = 0.21)
	comboTipo.current(0)
	

	lbl_senhaa=Label(tela_adm,bd=4,bg ='DarkTurquoise',text= 'Senha *',fg='black',font=('arial',14,'bold'))
	lbl_senhaa.place(relx=0.05, rely = 0.30)
	txt_senhaa = Entry(tela_adm,width=23,bd=4,show="*", bg ='white',fg='black',font=('arial',14,'bold'))
	txt_senhaa.place(relx=0.23, rely = 0.31)
	#txt_tipo.config(state='disabled')
	
	lbl_senhaac=Label(tela_adm,bd=4,bg ='DarkTurquoise',text= 'Confirma Senha *',fg='black',font=('arial',14,'bold'))
	lbl_senhaac.place(relx=0.55, rely = 0.30)
	txt_senhaac = Entry(tela_adm,width=23,bd=4, show="*" , bg ='white',fg='black',font=('arial',14,'bold'))
	txt_senhaac.place(relx=0.65, rely = 0.31)

	lbl_datap=Label(tela_adm,width=15,bd=4, height=2,bg ='DarkTurquoise',text= 'Data do Cadastro',fg='black',font=('arial',14,'bold'))
	lbl_datap.place(relx=0.05, rely = 0.50)
	txt_data = Label(tela_adm,width=21,bd=4, bg ='white',fg='black',font=('arial',14,'bold'))
	txt_data.place(relx=0.23, rely = 0.51)
	txt_data.config(text=data_atual)
	#txt_datav.insert(0,data_atual)
	txt_data.config(state='disabled')

	global btn_pesquisarp
	btn_pesquisarp = Button(tela_adm,bg='DodgerBlue',image=pesquisaimgbtn ,compound = LEFT,bd=8, text="Pesquisar", fg='black',font=('arial',14,'bold'))
	btn_pesquisarp.place(relx=0.05, rely = 0.7)
	btn_pesquisarp["command"] = reali_pesquisa_usuarios

	#btn_alterarp = Button(tela_adm,bg='DodgerBlue',bd=8,image=alterarimgbtn ,compound = LEFT, text="   Alterar    ", fg='black',font=('arial',14,'bold'),command=rel_alterar)
	#btn_alterarp.place(relx=0.25, rely = 0.7)
	btn_cadastrarv = Button(tela_adm,bg='DodgerBlue',image=cadastrarimg ,compound = LEFT,bd=6, text="Cadastrar", fg='black',font=('arial',14,'bold'),command=rel_cadastarUsuarioAdm)
	btn_cadastrarv.place(relx=0.20, rely = 0.7)

	btn_excluir = Button(tela_adm,bg='DodgerBlue',image=excluirimgbtn ,compound = LEFT,bd=8, text="     Excluir     ", fg='black',font=('arial',14,'bold'),command=excluirUsuarioAdm)
	btn_excluir.place(relx=0.35, rely = 0.7)

	btn_saidasp = Button(tela_adm,bg='DodgerBlue',bd=8,image=voltarimg ,compound = LEFT, text="     Voltar     ", fg='black',font=('arial',14,'bold'),command=lambda: limpar('adm'))
	btn_saidasp.place(relx=0.50, rely = 0.7)

	btn_gerar = Button(tela_adm,bg='DodgerBlue',bd=8,image=btnexcel ,compound = LEFT, text="Gerar Rel_Excel", fg='black',font=('arial',14,'bold'),command=lambda: gerarrel(tela_adm))
	btn_gerar.place(relx=0.65, rely = 0.7)

	
class App(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)
		self.start()

	def callback(self):
		self.root.quit()

	def run(self):
		global tinicial
		tinicial = tk.Tk()
		global h , w
		w,h = tinicial.winfo_screenwidth(),tinicial.winfo_screenheight()
		tinicial.geometry("%dx%d+0+0" % (w, h))
		tinicial.title("MB - PORTARIA ")
		#tinicial.resizable(width=False, height=False)
		tinicial['bg'] = 'DodgerBlue'
		tinicial.iconphoto(True, PhotoImage(file='./arquivos/MB.png'))
		image3=PhotoImage(file='./arquivos/MB2.png')
		global image2
		image2=PhotoImage(file='./arquivos/foto.png')
		global moradia
		moradia=PhotoImage(file='./arquivos/morador.png')
		global visitacao
		visitacao=PhotoImage(file='./arquivos/visitante.png')
		global pesquisaimg
		pesquisaimg=PhotoImage(file='./arquivos/pesquisar.png')
		global sairimg
		sairimg=PhotoImage(file='./arquivos/sair.png')
		global admimg
		admimg=PhotoImage(file='./arquivos/adm.png')
		global cadastrarimg
		cadastrarimg=PhotoImage(file='./arquivos/cadastrar.png')
		global voltarimg
		voltarimg=PhotoImage(file='./arquivos/voltar.png')
		global pesquisaimgbtn
		pesquisaimgbtn=PhotoImage(file='./arquivos/pesquisarbtn.png')
		global alterarimgbtn
		alterarimgbtn=PhotoImage(file='./arquivos/alterar.png')
		global excluirimgbtn
		excluirimgbtn=PhotoImage(file='./arquivos/excluir.png')
		global btnexcel
		btnexcel=PhotoImage(file='./arquivos/btnexecel.png')


		global borda_esq
		global falinha
		global tela_cadastrov
		global tela_cadastro
		global tela_adm
		#global progress1
		#importante para progressbar
		#s = ttk.Style() 
		#s.theme_use('default') 
		#s.configure("SKyBlue1.Horizontal.TProgressbar", foreground='Green', background='MediumSlateBlue')

		data_atual = datetime.now()
		data_atual = data_atual.strftime('%d/%m/%Y %H:%M')
		hf=h*0.8 #medidaparaframe
		wf=w*0.7

		

		
		borda_esq = Frame(tinicial,width=300, height=200,bg ='DodgerBlue')
		borda_esq.place(relx=0.01, rely = 0.05)

		lbl_bemvindo= Label(tinicial, width=30, height=2,bg ='DodgerBlue',text= 'Seja Bem-Vindo ao MB Portaria',fg='black',font=('arial',25,'bold'))
		lbl_bemvindo.place(relx=0.4, rely = 0.0)
		global btn_cadastro
		btn_cadastro = Button(borda_esq,image=moradia ,bg='DodgerBlue',bd=8,compound = TOP, text="Cadastrar Morador", fg='black',font=('arial',14,'bold'),command=tela_morador)
		btn_cadastro.grid(column=1, row=1, sticky=tk.W)
		lbl_espaco=Label(borda_esq, width=16,bg='DodgerBlue')
		lbl_espaco.grid(column=1, row=0, sticky=tk.W)
		
		global btn_visitante
		btn_visitante = Button(borda_esq,image=visitacao ,bg='DodgerBlue',bd=8,compound = TOP, text="Cadastrar Visitante", fg='black',font=('arial',14,'bold'),command=tela_visitante)
		btn_visitante.grid(column=1, row=3, sticky=tk.W)
		lbl_espaco2=Label(borda_esq, width=16,bg='DodgerBlue')
		lbl_espaco2.grid(column=1, row=2, sticky=tk.W)
		global btn_pesquisar
		btn_pesquisar = Button(borda_esq,image=pesquisaimg ,bg='DodgerBlue',bd=8,compound = TOP, text="        Pesquisar         ", fg='black',font=('arial',14,'bold'),command=tela_pesquisa)
		btn_pesquisar.grid(column=1, row=5, sticky=tk.W)
		lbl_espaco3=Label(borda_esq, width=9,bg='DodgerBlue')
		lbl_espaco3.grid(column=1, row=4, sticky=tk.W)
		global btn_saidas
		btn_saidas = Button(borda_esq,image=sairimg ,bg='DodgerBlue',bd=8,compound = TOP, text="              Sair              ", fg='black',font=('arial',14,'bold'),command=saindo)
		btn_saidas.grid(column=1, row=7, sticky=tk.W)
		lbl_saidas=Label(borda_esq, width=4,bg='DodgerBlue')
		lbl_saidas.grid(column=1, row=6, sticky=tk.W)
		if login.tipo_buscado == "ADM":
			global btn_adm
			btn_adm = Button(borda_esq,image=admimg ,bg='DodgerBlue',bd=8,compound = TOP, text="              ADM              ", fg='black',font=('arial',14,'bold'),command=tela_adm)
			btn_adm.grid(column=1, row=9, sticky=tk.W)
			lbl_adm=Label(borda_esq, width=4,bg='DodgerBlue')
			lbl_adm.grid(column=1, row=8, sticky=tk.W)
		else:
			pass	
		lbl_menu=Label(tinicial,image=image3,bd=4, bg ='DodgerBlue')
		lbl_menu.place(relx=0.4, rely = 0.3)

		lbl_aviso=Label(tinicial,bd=4, bg ='DodgerBlue',text="Encontra-se em vigor a Lei Geral de Proteção de Dados Pessoais (“LGPD”, Lei federal nº 13.709), que introduz em nosso país a disciplina de direitos e deveres de proteção de dados pessoais dos indivíduos.\n Fica sob responsabilidade da empresa contratante e seus usúarios, manter a segurança e veracidade dos dados aqui registrados!", fg='black',font=('arial',9,'bold'))
		lbl_aviso.place(relx=0.2, rely = 0.9)



		tinicial.mainloop()
		#progress1 =ttk.Progressbar(robozinho, orient=HORIZONTAL, length=61, style="SKyBlue1.Horizontal.TProgressbar",mode='determinate')
		#progress1.place(relx=0.485, rely = 0.266)
	

		


#app = App()
