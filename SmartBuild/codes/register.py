#Imports
import customtkinter, time, re, pyautogui
import tkinter as tk

from PIL import Image, ImageTk
from tkinter import PhotoImage
from customtkinter import CTkFont, CTkImage

from smartbd import conect #Conectando com o banco de dados no arquivo smartbd.py
connection = conect()

register_window = customtkinter.CTk() #Criando janela
#Configurações da janela
register_window.resizable(False, False)
register_window.geometry("720x480") 
register_window.title("SmartBuild - Cadastro")
register_window.iconbitmap('./img/icon.ico') #iCONE DA JANELA
winreg_actMode = customtkinter.set_appearance_mode("Dark")

winreg_window_width = 720
winreg_window_height = 480

winreg_screen_width = register_window.winfo_screenwidth() # Obter a largura e altura da tela
winreg_screen_height = register_window.winfo_screenheight()

x = int((winreg_screen_width/2) - (winreg_window_width/2)) # Calcular a posição x e y para centralizar a janela
y = int((winreg_screen_height/2) - (winreg_window_height/2))

register_window.geometry("{}x{}+{}+{}".format( # Configurar a janela para abrir no centro da tela
                                        winreg_window_width, 
                                        winreg_window_height,
                                        x,
                                        y))

#Variaveis
parameteruser = ["0", "1", "2"]
test_user_var = "1"

#Fontes Pré-Definidas
font_bold = CTkFont( #Cria uma fonte itpo bold
                family="Arial",
                size=35,
                weight="bold"
)
winreg_font_bold = CTkFont( #Cria uma fonte itpo bold
                family="Arial",
                size=14,
                weight="bold"
                )

#Funções

def mostrar_senha_senha():
    global mostrar_senha
    mostrar_senha = not mostrar_senha

    if mostrar_senha:
        inputSenha.configure(show="")
        eye_button_senha.configure(image=photo_senha_open)
    else:
        inputSenha.configure(show="*")
        eye_button_senha.configure(image=photo_senha_closed)

def mostrar_senha_senhaAg():
    global mostrar_senhaAg
    mostrar_senhaAg = not mostrar_senhaAg

    if mostrar_senhaAg:
        inputsenhaAg.configure(show="")
        eye_button_senhaAg.configure(image=photo_senha_open)
    else:
        inputsenhaAg.configure(show="*")
        eye_button_senhaAg.configure(image=photo_senha_closed)

def ctrl():
    pyautogui.hotkey("ctrl")
def test_user(event): #Verifica a disponibilidade do nome de usuario
        global test_user_var
        user = inputUsername.get()
        user = user.replace(" ", "")
        testuser = 0
        for let in user:
            if let.isalpha():
                testuser+=1

        username = inputUsername.get()
        connection = conect()
        cursor = connection.cursor()
        cursor.execute("SELECT username_smart FROM cadastro")
        username_no_banco = [row[0] for row in cursor.fetchall()]

        if username in username_no_banco or username == "":
            dot.configure(bg="red")
            test_user_var = "2"
        elif testuser < 4:
             dot.configure(bg="red")
             test_user_var = "1"
        else:
            dot.configure(bg="green")
            test_user_var = "0"
        ctrl

def email_ja_existe(email): #Verifica se o email ja não foi cadastrado
        connection = conect()
        cursor = connection.cursor()
        cursor.execute("SELECT email_smart FROM cadastro")
        emails_no_banco = cursor.fetchall()
        test = 0
        if (email,) in emails_no_banco:
            test +=1
        else:
            test==0
        return test

def is_valid_email(email): #validando email
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$", email)

def is_valid_password(senha): #Validando senha
    return re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$%^*()<>+-={}]).*$", senha)

def nome_count(nome): #Verifica quantidade de caracteres á no nome do usuario
    nome = nome.replace(" ", "")
    testnome = 0
    for let in nome:
        if let.isalpha():
            testnome+=1
    return testnome

def senha_count(senha): #Verifica parâmetros da senha ex: espaços na senha
    testsenha = 0
    for lets in senha:
        if lets.isalpha() or lets.isdigit() or lets.isspace():
            testsenha+=1
    return testsenha

def checkbox_pressed(): #Ao pressionar a Checkbox
    if winreg_checkbox_var.get() == 1:
        print("Checkbox selecionado")
    else:
        winreg_checkbox_var == 0
        print("Checkbox não selecionado")
    

def register(event): #enviando dados para o banco!!!!

    global test_user_var

    nome = inputNome.get()
    email = inputEmail.get()
    username = inputUsername.get()
    senha = inputSenha.get()
    senhaag = inputsenhaAg.get()

    testnome = nome_count(nome)
    testsenha = senha_count(senha)
    test = email_ja_existe(email)

    if nome == "" or email == "" or senha == "" or senhaag == "": #verificando se campos não estão vazios
        empty_inputs = []
        if nome == "":
                empty_inputs.append("Nome")
        if email == "":
                empty_inputs.append("E-mail")
        if senha == "":
                empty_inputs.append("Senha")
        if senhaag == "":
                empty_inputs.append("Repetir-Senha")
        tk.messagebox.showinfo("Error", "Os seguintes campos estão vazios: " + ", ".join(empty_inputs))
        print("Erro ao enviar formulario... espera-se que nenhum campo fique vazio")
        return
    if testnome < 8: #verifica se o nome da pessoa tiver menos que 8 letras dará erro
        tk.messagebox.showinfo("Error", "espera-se que o campo nome tenha no minimo 8 letras, tente novamente..")
        print("Erro ao enviar formulario... espera-se que o campo nome tenha no minimo 8 letras")
        testnome == 0
        return testnome
    if test > 0: #Verifica se email ja foi cadastrado
        tk.messagebox.showinfo("Error", "E-mail ja cadastrado")
        print("Erro ao enviar formulario... espera-se que seja ultilizado um email diferente")
        test == 0
        return test
    if not is_valid_email(email): #verificando email
        tk.messagebox.showinfo("Error", "E-mail inválido tente ultilizar no final do email um dos dominios a seguir: @gmail.com, @yahoo.com, @hotmail.com, @smart.com")
        print("Erro ao enviar formulario... espera-se que o campo email tenha um dominio aceitavel")
        return
    if not is_valid_password(senha): #verificando senha
        tk.messagebox.showinfo("Error", "Senha inválida deve conter na senha:\n-1 letra maiúscula,\n-1 letra minúscula,\n-1 número,\n-1 caracter especial,\n-Não pode conter espaços.")
        print("Erro ao enviar formulario... espera-se que o campo senha tenha uma sintaxe aceitavel")
        return
    if senha != senhaag: #se as senhas não coincidirem dará erro
        tk.messagebox.showinfo("Error", "As senhas não coincidem")
        print("Erro ao enviar formulario... espera-se que nenhum campo fique vazio")
        return 
    if testsenha < 6: #verifica se a senha contem pelomenos 6 caracteres
        tk.messagebox.showinfo("Error", "espera-se que o campo senha tenha no minimo 6 caracteres, tente novamente..")
        print("Erro ao enviar formulario... espera-se que o campo nome tenha no minimo 6 caracteres")
        testsenha == 0
        return testsenha
    if winreg_checkbox_var.get() == 0: #Termos de segurança não aceitos
        tk.messagebox.showinfo("Error", "É necessario aceitar os termos para realizar o cadastro!!")
        print("Erro ao enviar formulario... é necessario aceitar os termos para realizar o cadastro!!")
        return 
    if test_user_var == "1": #Se o usuario tentar registrar com um usuario contendo menos que 4 caracteres
        tk.messagebox.showinfo("Error", "Nome de usuario necessita ter ao menos 4 caracteres")
        print("Erro ao enviar formulario... nome de usuario menor que o esperado!!")
        return 
    if test_user_var == "2": #Se o nome de usuario ja foi cadastrado da um error
        tk.messagebox.showinfo("Error", "Nome de usuario ja cadastrado, tente outro")
        print("Erro ao enviar formulario... nome de usuario ja cadastrado!!")
        return 
    else: #Se passar por todos os parâmetros inseri os dados ao Banco de Dados
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO cadastro (nome_smart, email_smart, senha_smart, username_smart) VALUES (%s, %s, %s, %s)", (nome, email, senha, username))

        connection.commit()
        connection.close()
        tk.messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!!")
        print("Sucesso ao enviar formulario...")
        register_window.destroy()
        from login import login_window

def winreg_on_enter(e): #Quando entrar mudar a cor do texto
    back_label.configure(text_color='#FF0000')
def winreg_on_leave(e):
    back_label.configure(text_color='#619FEF')
def backwindow():
    register_window.destroy()
    time.sleep(0.5)
    from login import login_window

#Frames
register_label_frame = customtkinter.CTkFrame( #Frame laranja para logo e label login
                                master=register_window, 
                                width=270, 
                                height=479, 
                                corner_radius=0, 
                                fg_color="#F47D29"
)
register_label_frame.place(
        x=1,
        y=1,
)

winreg_frame = customtkinter.CTkFrame( #Main frame para os contents de registro
                        master=register_window,
                        width=449,
                        height=479,
                        corner_radius=0,
                        fg_color="#333333"
) 
winreg_frame.place(
        x=271,
        y=1,
)
dot = customtkinter.CTkCanvas( #Quadrado teste do nome de usuario
                master=winreg_frame,
                width=10,
                height=10,
                bg="#FFFFFF",
                border=0 
)
dot.place(
     x=335, 
     y=210
)

#Imagens
imagem_path = './img/logo.png' #Puxando logo
imagem = PhotoImage(file=imagem_path)
label_imagem = tk.Label(master=register_label_frame, image=imagem, width=190, height=190)
label_imagem.place(x= 37, y=100)

#Labels
registro_label = customtkinter.CTkLabel( #Label "Registro" titulo
                            master=register_label_frame, 
                            text="Registro",
                            font=font_bold,
                            text_color="white"
                            )
registro_label.place(
        y=255,
        x=70
        )

back_label = customtkinter.CTkLabel( #Label para voltar a area de login
    master=winreg_frame,
    text="Você ja tem uma conta?.",
    font=("Arial", 12),
    cursor="hand2",
    text_color="#619FEF"
)
back_label.place(
            x=155,
            y=440
)
back_label.bind("<Button-1>", lambda event: backwindow()) #Funções label
back_label.bind("<Enter>", winreg_on_enter)
back_label.bind("<Leave>", winreg_on_leave)

Smartbuild_label = customtkinter.CTkLabel( #Label "Smartbuild"
                                master=winreg_frame, 
                                text="SmartBuild", 
                                text_color="#ffffff", 
                                font=font_bold
)
Smartbuild_label.place(
                x=134,
                y=10
)

#Entry - Inputs
inputNome = customtkinter.CTkEntry( #Login input "Nome"
                                master=winreg_frame, 
                                placeholder_text="Digite seu nome*",
                                placeholder_text_color="#7D7D7D",
                                font=("Arial", 11),
                                corner_radius=6,
                                border_color="",
                                text_color="#0E0E0E",
                                fg_color="#FFFFFF",
                                width=180,
                                height=37
                                )
inputNome.place(
            y=100,
            x=135
            )

inputEmail = customtkinter.CTkEntry( #Login input "Email"
                                master=winreg_frame, 
                                placeholder_text="Digite seu E-mail*",
                                placeholder_text_color="#7D7D7D",
                                font=("Arial", 11),
                                corner_radius=6,
                                border_color="",
                                text_color="#0E0E0E",
                                fg_color="#FFFFFF",
                                width=180,
                                height=37
                                )
inputEmail.place(
            y=150,
            x=135
            )

inputUsername = customtkinter.CTkEntry( #Login input "Usename"
                            master=winreg_frame, 
                            placeholder_text="Digite Nome de Usuario*",
                            placeholder_text_color="#7D7D7D",
                            font=("Arial", 11),
                            corner_radius=6,
                            border_color="",
                            text_color="#0E0E0E",
                            fg_color="#FFFFFF",
                            width=180,
                            height=37
)
inputUsername.place(
            y=200,
            x=135
            )
inputUsername.bind("<KeyRelease>", test_user)

inputSenha = customtkinter.CTkEntry( #Login input "Senha"
                                master=winreg_frame, 
                                placeholder_text="Digite sua senha*",
                                placeholder_text_color="#7D7D7D",
                                font=("Arial", 11),
                                show="*",
                                corner_radius=6,
                                text_color="#0E0E0E",
                                border_color="",
                                fg_color="#FFFFFF",
                                width=180,
                                height=37
                                )
inputSenha.place(
            y=250,
            x=135
            )

inputsenhaAg = customtkinter.CTkEntry( #Login input "Senha denovo"
                                master=winreg_frame, 
                                placeholder_text="Digite senha Novamente*",
                                placeholder_text_color="#7D7D7D",
                                font=("Arial", 11),
                                show="*",
                                corner_radius=6,
                                text_color="#0E0E0E",
                                border_color="",
                                fg_color="#FFFFFF",
                                width=180,
                                height=37
                                )
inputsenhaAg.place(
            y=300,
            x=135
            )

#Buttons
winreg_checkbox_var = tk.IntVar() #Botão checkbox
winreg_checkbox = tk.Checkbutton(
                    master=winreg_frame, 
                    text="Aceitar os termos",
                    font=("Arial", 9),
                    width=12,
                    height=1,
                    bg="#333333",
                    activebackground="#333333",
                    fg="#ffffff",
                    activeforeground="#000000",
                    cursor="hand2",
                    selectcolor="#333333",
                    variable=winreg_checkbox_var,
                    relief="flat",
                    command=checkbox_pressed,
)
winreg_checkbox.place(y=340, x=137)

image_senha_open = Image.open(".\img\openEye.png").resize((26, 26))
photo_senha_open = ImageTk.PhotoImage(image_senha_open)

image_senha_closed = Image.open(".\img\closedEye.png").resize((26, 26))
photo_senha_closed = ImageTk.PhotoImage(image_senha_closed)

mostrar_senha = False
mostrar_senhaAg = False

eye_button_senha = tk.Button(
    master=inputSenha,
    image=photo_senha_closed,
    border=False,
    highlightthickness=0,
    command=mostrar_senha_senha,
)
eye_button_senha.place(x=146, y=5)

eye_button_senhaAg = tk.Button(
    master=inputsenhaAg,
    image=photo_senha_closed,
    border=False,
    highlightthickness=0,
    command=mostrar_senha_senhaAg,
)
eye_button_senhaAg.place(x=146, y=5)


btnregister = customtkinter.CTkButton( #Botão registro
                                master=winreg_frame, 
                                text="Registrar",
                                font=winreg_font_bold,
                                corner_radius=5,
                                width=180,
                                height=30,
                                text_color="white",
                                fg_color="#F47D29",
                                hover_color="#ED6404",
                                )
btnregister.place(
            y=400,
            x=135
            )
btnregister.bind("<Button-1>", register)

register_window.bind("<Return>", register)
register_window.mainloop()