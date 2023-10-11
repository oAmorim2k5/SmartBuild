#Imports
import customtkinter, time
import tkinter as tk
import smartbd

from customtkinter import CTkFont, CTkImage
from PIL import Image, ImageTk
from tkinter import PhotoImage

from smartbd import conect #Conectando com o banco de dados no arquivo smartbd.py
connection = conect()

login_window = customtkinter.CTk() #Criando a janela
#Configurações da janela
login_window.resizable(False, False) 
login_window.geometry("720x480") 
login_window.title("SmartBuild - Login")
login_window.iconbitmap('./img/icon.ico') #iCONE DA JANELA
actMode = customtkinter.set_appearance_mode("Dark")

#Centralizando a janela no meio da tela do usuario
window_width_login = 720
window_height_login = 480

screen_width_login = login_window.winfo_screenwidth() # Obtém a largura e altura da tela
screen_height_login = login_window.winfo_screenheight()

x = int((screen_width_login/2) - (window_width_login/2)) # Calcular a posição x e y para centralizar a janela
y = int((screen_height_login/2) - (window_height_login/2))

login_window.geometry("{}x{}+{}+{}".format( # Configurar a janela para abrir no centro da tela
                                        window_width_login, 
                                        window_height_login,
                                        x,
                                        y))

#Fontes Pré-Definidas
font_bold_title = CTkFont( #Criando uma font bold - para o titulo
                family="Arial",
                size=35,
                weight="bold"
)
font_bold = CTkFont( #Criando uma font bold
                family="Arial",
                size=14,
                weight="bold"
                )
font_bold2 = CTkFont( #CrCriando uma font bold
                family="Arial",
                size=12,
                weight="bold"
                )
winlog_font_bold = CTkFont( #Criando uma font bold - Para o botão login
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

def login(event): #Função login conectando banco e testando parametros
    email_username = inputEmail.get()
    senha = inputSenha.get()

    cursor = connection.cursor()
    cursor.execute("SELECT email_smart, username_smart, senha_smart FROM cadastro WHERE email_smart = %s OR username_smart = %s", (email_username, email_username))
    row = cursor.fetchone()

    if email_username == "" or senha == "":
        empty_inputs = []
        if email_username == "":
            empty_inputs.append("E-mail ou Nome de usuario")
        if senha == "":
            empty_inputs.append("Senha")
        tk.messagebox.showinfo("Error", "Os seguintes campos estão vazios: " + ", ".join(empty_inputs))
        print("Erro ao enviar formulário... espera-se que nenhum campo fique vazio")
        return

    if row is None:
        tk.messagebox.showerror("Error", "E-mail/Nome de usuario ou senha incorretos, tente novamente.")
        return
    else:
        email_db, username_db, senha_db = row
        if senha == senha_db:
            cursor.fetchall()
            cursor.close()
            connection.close()
            smartbd.email = email_db
            smartbd.senha = senha
            login_window.destroy()
            time.sleep(0.5)
            from user import userwin
        else:
            tk.messagebox.showerror("Error", "E-mail/Nome de usuario ou senha incorretos, tente novamente.")
            return

def register(): #Função registro para abrir tela de registro
    login_window.destroy()
    time.sleep(0.5)
    from register import register_window

def on_enter(e): #Função para mudar cor do texto (criar conta) ao colocar mouse em cima
    register_label.configure(text_color='#FF0000')
def on_leave(e):
    register_label.configure(text_color='#619FEF')

login_window.bind("<Return>", login)

#Frames
label_login_frame = customtkinter.CTkFrame( #Frame com logo e label "Login"
                                master=login_window,
                                width=270,
                                height=479,
                                corner_radius=0,
                                fg_color="#F47D29"
)
label_login_frame.place(
        x=1,
        y=1,
)

frame = customtkinter.CTkFrame( #Main frame com os contents
                    master=login_window,
                    width=449,
                    height=479,
                    corner_radius=0,
                    fg_color="#333333"
) 
frame.place(
        x=271,
        y=1,
)

#Imagens
imagem_path = './img/logo.png' #Puxando imagem da logo
imagem = PhotoImage(file=imagem_path)
label_imagem = tk.Label(master=label_login_frame, image=imagem, width=190, height=190)
label_imagem.place(x= 37, y=100)

imagem_path_user = './img/user.png' #Puxando imagem boneco user
imagem_user = PhotoImage(file=imagem_path_user)
label_imagem_user = tk.Label(master=frame, image=imagem_user, width=140, height=140)
label_imagem_user.place(x= 150, y=30)


#Labels
login_label = customtkinter.CTkLabel( #Label Login
                            master=label_login_frame, 
                            text="Login",
                            text_color="white",
                            font=font_bold_title,
                            )
login_label.place(
        y=255,
        x=90
        )

register_label = customtkinter.CTkLabel( #Label que puxa tela registro
    master=frame,
    text="Ainda não tem uma conta ? registre-se aqui.",
    font=("Arial", 12),
    cursor="hand2",
    text_color="#619FEF"
)
register_label.place(
                x=105,
                y=440)
register_label.bind("<Button-1>", lambda event: register()) #Funções label
register_label.bind("<Enter>", on_enter)
register_label.bind("<Leave>", on_leave)

#Entry - Inputs
inputEmail = customtkinter.CTkEntry( #Login input "Email" or "Username"
                                master=frame, 
                                placeholder_text="E-mail ou Nome de Usuario*",
                                placeholder_text_color="#7D7D7D",
                                font=("Arial", 11),
                                corner_radius=5,
                                border_color="",
                                text_color="#0E0E0E",
                                fg_color="#ffffff",
                                width=180,
                                height=37
                                )
inputEmail.place(
            y=200,
            x=135
            )

inputSenha = customtkinter.CTkEntry( #Login input "Password"
                                master=frame, 
                                placeholder_text="Senha*",
                                placeholder_text_color="#7D7D7D",
                                font=("Arial", 11),
                                show="*",
                                corner_radius=5,
                                text_color="#0E0E0E",
                                border_color="",
                                fg_color="#ffffff",
                                width=180,
                                height=37
                                )
inputSenha.place(
            y=260,
            x=135
            )

#Buttons
btnLogin = customtkinter.CTkButton( #Login Button
                                master=frame, 
                                text="Login",
                                font=winlog_font_bold,
                                corner_radius=5,
                                width=180,
                                height=30,
                                text_color="white",
                                fg_color="#F47D29",
                                hover_color="#ED6404",
                                )
btnLogin.place(
            y=350,
            x=135
            )
btnLogin.bind("<Button-1>", login)
checkbox = customtkinter.CTkCheckBox( #Remember checkbox (OFFLINE)
                                master=frame, 
                                text="Lembre-se de mim",
                                font=("Arial", 14),
                                hover_color="#F47D29"
)

checkbox_var = tk.IntVar()

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
    command=mostrar_senha_senha
)
eye_button_senha.place(x=146, y=5)
login_window.mainloop()
