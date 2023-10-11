#Imports
import customtkinter, time, os, glob, json, pyautogui
import tkinter as tk

from tkinter import ttk, messagebox, filedialog
from smartbd import email, senha
from ttkthemes import ThemedStyle
from tkinter import *
from PIL import Image, ImageTk

from smartbd import conect
from customtkinter import CTk, CTkFont, CTkImage


connection = conect() #Conectando com o banco de dados no arquivo smartbd.py
cursor = connection.cursor()
def get_username(email, senha): #Conecta com o Banco de Dados e puxa o Username do usuario 
    cursor = connection.cursor()

    cursor.execute("SELECT username_smart FROM cadastro WHERE email_smart = %s AND senha_smart = %s", (email, senha))
    data = cursor.fetchone()

    cursor.close()
    connection.close()

    if data:
        username = data[0]
        return username
    else:
        return None
username = get_username(email, senha)
if username:
    print("Username do usuário:", username)
else:
    print("Nenhum usuário encontrado com o email e senha fornecidos.")

userwin = customtkinter.CTk() #Criando janela
#Configurações da janela
userwin.title("SmartBuild - Area do Usuario")
userwin.resizable(False, False)
userwin.iconbitmap('./img/icon.ico') #iCONE DA JANELA
actAppearance = customtkinter.set_appearance_mode("Dark") 

window_width = 920 
window_height = 480

screen_width = userwin.winfo_screenwidth() # Obter a largura e altura da tela
screen_height = userwin.winfo_screenheight()

x = int((screen_width/2) - (window_width/2)) # Calcular a posição x e y para centralizar a janela
y = int((screen_height/2) - (window_height/2))

userwin.geometry("{}x{}+{}+{}".format( # Configurar a janela para abrir no centro da tela
                                        window_width, 
                                        window_height,
                                        x,
                                        y))

#Fontes Pré-Definidas
font_username = CTkFont( #Cria uma fonte itpo bold
                size=20,
)
font_criando = CTkFont( #Cria uma fonte itpo bold
                family="Arial",
                size=25,
                weight="bold"
)
font_creating = CTkFont( #Cria uma fonte itpo bold
                family="Arial",
                size=15,
                weight="bold"
)
font_bold = CTkFont( #Cria uma fonte itpo bold
                family="Arial",
                size=12,
                weight="bold"
)
font_bold2 = CTkFont( #Cria uma fonte itpo bold
                family="Arial",
                size=15,
                weight="bold"
)

#Variaveis
lista_projetos = []
selecionado_estrutura = 0
frame_newProject_isopen = 0
custom_estrutura = None
nome_arquivo = ""
project_is_open = 0

#Variaveis software
frame_select_isopen = 0
button_state = 0 #Criar e destruir frame_select para fazer objeto
frame_select = None
frame_select_isopen = 0

x_inicial, y_inicial = 0, 0
objeto_selecionado_local = None

canvas_width = 720
canvas_height = 480

button_quadrado = 0
button_circulo = 0
button_linha = 0
button_triangulo = 0
contador_quadrado = 0
contador_circulo = 0
contador_triangulo = 0
contador_linha = 0
objetos = []

last_x, last_y = None, None  # Variáveis para rastrear a última posição do mouse
is_moving = False 
zoom_value = 100 #zoom
username = "oAmorim"
#Funções
def buscar_projetos_por_usuario(user_projeto): #busca no banco de dados os projetos criados pelo usuario
    connection = conect()
    cursor = connection.cursor()
    cursor.execute("SELECT id_projeto, nome_projeto, tipo_projeto, tipo_medida, descricao_projeto FROM projeto WHERE user_projeto = %s", (user_projeto,))
    projetos = cursor.fetchall()
    cursor.close()
    connection.close()

    return projetos

class Projeto: #Classe criação de projetos
    def __init__(self, projeto_id, nome, tipo_proj, tipo_medida, descricao):
        self.projeto_id = projeto_id
        self.nome = nome
        self.tipo_proj = tipo_proj
        self.descricao = descricao
        self.tipo_medida = tipo_medida
        
def exibir_projetos_na_tela(projetos): #Busca no Banco de Dados para exibir projetos na tela
    global nome_arquivo
    def abrir_projeto(proj):
        connection = conect()
        cursor = connection.cursor()
        cursor.execute("SELECT nome_projeto FROM projeto WHERE id_projeto = %s", (proj,))
        projeto = cursor.fetchone()
        cursor.close()
        if projeto:
            nome = projeto[0]
            print(f"ID do Projeto: {proj}")
            print(f"Nome do Projeto: {nome}")
        else:
            print(f"Nenhum projeto encontrado com o ID {proj}")
        open_project(nome)
        

    def atualizar_lista_projetos():
            global lista_projetos
            projetos_do_usuario = buscar_projetos_por_usuario(username)
            lista_projetos = projetos_do_usuario
            exibir_projetos_na_tela(projetos_do_usuario)
            userwin.update()
    
    def excluir_projeto(projeto):
        nome_arquivo = f"{projeto.nome}.json"
        caminhos_arquivos = glob.glob(os.path.join("E:\SmartBuild\Projetos", nome_arquivo))
        resposta = messagebox.askquestion("Confirmação", "Tem certeza de que deseja excluir o projeto?")

        if caminhos_arquivos and resposta == "yes":
            try:
                connection = conect()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM projeto WHERE id_projeto = %s", (projeto.projeto_id,))
                connection.commit()

                try:
                    os.remove("E:\SmartBuild\Projetos")
                    print(f"Arquivo {nome_arquivo} excluído com sucesso.")
                except OSError as e:
                    print(f"Erro ao excluir o arquivo {nome_arquivo}: {e}")

                tk.messagebox.showinfo("Sucesso", "Projeto excluído com sucesso!!")
                print("Sucesso ao excluir projeto...")
                atualizar_lista_projetos()
                
            except Exception as e:
                print("Erro ao excluir projeto:", e)
                print(f"Nenhum arquivo com o nome {nome_arquivo} encontrado na pasta C:\SmartBuild\Projetos.")
                tk.messagebox.showerror("Erro", f"Erro ao excluir projeto, Nenhum arquivo com o nome {nome_arquivo} encontrado na pasta C:\SmartBuild\Projetos.")
        else:
            return

    def mostrar_desc_projeto(event, projeto):
        global popup
        popup= tk.Label(
                master=userwin,
                text=f"Descrição: {projeto.descricao}",
                font=("Arial", 10),
                anchor="e",
                bg="#1e1e1e",
                fg="#ffffff",
                )
        popup.place(x=1, y=1)

    def sumir_desc_projeto(event, projeto):
        global popup
        popup.destroy()
        

    def scroll_canvas(event):
        canvas_projetos.yview_scroll(-1 * (event.delta // 120), "units")

    
    canvas_projetos = tk.Canvas(userwin, bg="#242424", width=720, height=460, highlightthickness=0)
    canvas_projetos.place(x=200, y=10)

    scrollbar_projetos = ttk.Scrollbar(userwin, orient=tk.VERTICAL, command=canvas_projetos.yview)

    canvas_projetos.bind("<Configure>", lambda e: canvas_projetos.configure(scrollregion=canvas_projetos.bbox("all")))
    canvas_projetos.bind_all("<MouseWheel>", scroll_canvas)
    canvas_projetos.configure(yscrollcommand=scrollbar_projetos.set)

    y_position = 20
    for projeto in projetos:

        projetos_frame = customtkinter.CTkFrame(master=canvas_projetos, width=700, height=100, corner_radius=3, border_width=1, border_color="#1e1e1e")
        canvas_projetos.create_window((10, y_position), window=projetos_frame, anchor=tk.NW)

        projeto_obj = Projeto(projeto[0], projeto[1], projeto[2], projeto[3], projeto[4])

        picture_img = tk.Frame(projetos_frame, width=70, height=70, highlightthickness=1, highlightbackground="#1e1e1e", bg="#2b2b2b")
        id_label = tk.Label(projetos_frame, text=f"ID do Projeto: {projeto_obj.projeto_id}",font=font_bold, bg="#2b2b2b", fg="white")
        nome_label = tk.Label(projetos_frame, text=f"Nome do Projeto: {projeto_obj.nome}",font=font_bold, bg="#2b2b2b", fg="white")
        tipo_estrutura_label = tk.Label(projetos_frame, text=f"Estrutura de um(a): {projeto_obj.tipo_proj}",font=font_bold, bg="#2b2b2b", fg="white")
        tipo_medida_label = tk.Label(projetos_frame, text=f"Medida: {projeto_obj.tipo_medida}",font=font_bold, bg="#2b2b2b", fg="white")
        descricao_label = tk.Label(projetos_frame, text="Descrição do Projeto: ",font=font_bold, bg="#2b2b2b", fg="white")
        descricao_label_event = tk.Label(projetos_frame, text="...", font=font_bold2, bg="#2b2b2b", fg="white", cursor="hand2")
        descricao_label_event.bind("<Enter>", lambda event, proj=projeto_obj: mostrar_desc_projeto(event, proj))
        descricao_label_event.bind("<Leave>", lambda event, proj=projeto_obj: sumir_desc_projeto(event, proj))

        button_entrar = tk.Button(projetos_frame, text="entrar", font=font_bold, bg="#2b2b2b", fg="white", highlightthickness=1, highlightcolor="white", activebackground="white", relief="ridge", command=lambda proj=projeto_obj.projeto_id: abrir_projeto(proj))
        button_entrar.place(x=647, y=70)

        button_deletar = tk.Button(projetos_frame, text="excluir", font=font_bold, bg="#991010", fg="white", highlightthickness=1, highlightcolor="white", activebackground="white", relief="ridge", command=lambda proj=projeto_obj: excluir_projeto(proj) )
        button_deletar.place(x=590, y=70)

        picture_img.place(x=15, y=15)
        id_label.place(x=600, y=12)
        nome_label.place(x=100, y=12)
        tipo_estrutura_label.place(x=100, y=40)
        tipo_medida_label.place(x=600, y=35)
        descricao_label.place(x=100, y=68)
        descricao_label_event.place(x=225, y=67)
        nome_arquivo = projeto_obj.nome
        y_position += 110
projetos_do_usuario = buscar_projetos_por_usuario(username)
if projetos_do_usuario:
    print(f"Projetos de {username}:")
    exibir_projetos_na_tela(projetos_do_usuario)
else:
    print(f"Usuário {username} não possui projetos.")

def open_project(nome): #ABRIR PROJETO
    global project_is_open
    if project_is_open == 1:
        return
    else:
        project_is_open += 1
        softwin = customtkinter.CTk() #Criando janela

        class MovableResizableQuadrado: #class para mover objeto quadrado
            contador_quadrado = 0
            def __init__(self, canvas, x, y, altura, largura, fill):
                global objetos
                self.canvas = canvas
                self.quadrado = canvas.create_rectangle(x, y, x + largura, y + altura, fill=fill, outline="black")
                self.nomeobj = f"Quadrado-{MovableResizableQuadrado.contador_quadrado + 1}"
                self.canvas.tag_bind(self.quadrado, '<ButtonPress-1>', self.iniciar_movimento)
                self.canvas.tag_bind(self.quadrado, '<B1-Motion>', self.mover)
                self.canvas.tag_bind(self.quadrado, '<ButtonRelease-1>', self.parar_movimento)
                self.height = altura
                self.width = largura
                self.fill = fill
                self.mover_ativo = False
                self.x_inicial = 0
                self.y_inicial = 0

                MovableResizableQuadrado.contador_quadrado += 1

                self.padx = self.canvas.coords(self.quadrado)[0]
                self.pady = self.canvas.coords(self.quadrado)[1]
                self.new_square_list()

            def new_square_list(self):
                new_obj = {
                    "nome": self.nomeobj,
                    "x": self.canvas.coords(self.quadrado)[0],
                    "y": self.canvas.coords(self.quadrado)[1],
                    "width": self.width,
                    "height": self.height,
                    "color": self.fill
                }
                objetos.append(new_obj)

            def iniciar_movimento(self, event):
                self.mover_ativo = True
                self.x_inicial = event.x
                self.y_inicial = event.y
                

            def mover(self, event):
                if self.mover_ativo:
                    dx = event.x - self.x_inicial
                    dy = event.y - self.y_inicial
                    self.canvas.move(self.quadrado, dx, dy)
                    self.x_inicial = event.x
                    self.y_inicial = event.y

            def parar_movimento(self, event):
                self.mover_ativo = False
                self.new_position(event)

            def new_position(self, event):
                global objetos
                info = f"\nNome: {self.nomeobj}\nAltura: {self.height}\nLargura: {self.width}\nCor: {self.fill}\nPosição X: {self.canvas.coords(self.quadrado)[0]}\nPosição Y: {self.canvas.coords(self.quadrado)[1]}"
                for objeto in objetos:
                    if objeto["nome"] == self.nomeobj:
                        objeto["x"] = self.canvas.coords(self.quadrado)[0]
                        objeto["y"] = self.canvas.coords(self.quadrado)[1]
                os.system("cls")
                print(info)
                print(objetos)


        class MovableResizableTriangle: #class para mover objeto triangulo
            contador_triangulo = 0
            global objetos
            def __init__(self, canvas, x, y, width, height, fill):
                self.canvas = canvas
                self.width = width
                self.height = height
                self.triangle = None
                self.nomeobj = f"Triangulo-{MovableResizableTriangle.contador_triangulo + 1}"
                self.fill = fill
                self.is_dragging = False
                self.start_x_drag = 0
                self.start_y_drag = 0

                self.create_triangle(x, y, fill)
                self.canvas.tag_bind(self.triangle, "<ButtonPress-1>", self.on_press)
                self.canvas.tag_bind(self.triangle, "<B1-Motion>", self.on_drag)
                self.canvas.tag_bind(self.triangle, "<ButtonRelease-1>", self.on_release)

                MovableResizableTriangle.contador_triangulo += 1
            
            def create_triangle(self, x, y, fill):
                x1 = x - self.width / 2
                y1 = y + self.height / 2
                x2 = x + self.width / 2
                y2 = y + self.height / 2
                x3 = x
                y3 = y - self.height / 2
                self.triangle = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=fill, outline="black")
                self.padx = self.canvas.coords(self.triangle)[0]
                self.pady = self.canvas.coords(self.triangle)[1]
                self.new_triangle_list()

            def new_triangle_list(self):
                new_obj = {
                    "nome": self.nomeobj,
                    "x": self.canvas.coords(self.triangle)[0],
                    "y": self.canvas.coords(self.triangle)[1],
                    "width": self.width,
                    "height": self.height,
                    "color": self.fill
                }
                objetos.append(new_obj)

            def on_press(self, event):
                self.is_dragging = True
                self.start_x_drag = event.x
                self.start_y_drag = event.y
                print(objetos)

            def on_drag(self, event):
                if self.is_dragging:
                    dx = event.x - self.start_x_drag
                    dy = event.y - self.start_y_drag
                    self.canvas.move(self.triangle, dx, dy)
                    self.start_x_drag = event.x
                    self.start_y_drag = event.y
                    

            def on_release(self, event):
                self.is_dragging = False
                self.new_position(event)

            def new_position(self, event):
                global objetos
                info = f"\nNome: {self.nomeobj}\nAltura: {self.height}\nLargura: {self.width}\nCor: {self.fill}\nPosição X: {self.canvas.coords(self.triangle)[0]}\nPosição Y: {self.canvas.coords(self.triangle)[1]}"
                for objeto in objetos:
                    if objeto["nome"] == self.nomeobj:
                        objeto["x"] = self.canvas.coords(self.triangle)[0]
                        objeto["y"] = self.canvas.coords(self.triangle)[1]
                os.system("cls")
                print(info)
                print(objetos)

        class MovableResizableCircle:
            contador_circulo = 0
            
            def __init__(self, canvas, x, y, width, height, fill):
                self.canvas = canvas
                self.width = width
                self.height = height
                self.radius_x = width / 2
                self.radius_y = height / 2
                self.oval = None
                self.nomeobj = f"Circulo-{MovableResizableCircle.contador_circulo + 1}"
                self.altura = height
                self.comprimento = width
                self.cor = fill
                self.pos_x = x
                self.pos_y = y
                self.fill = fill
                self.is_dragging = False
                self.start_x_drag = 0
                self.start_y_drag = 0

                if width == height:
                    self.create_circle(x, y, self.radius_x, fill)
                else:
                    self.create_oval(x, y, self.radius_x, self.radius_y, fill)

                self.canvas.tag_bind(self.oval, "<ButtonPress-1>", self.on_press)
                self.canvas.tag_bind(self.oval, "<B1-Motion>", self.on_drag)
                self.canvas.tag_bind(self.oval, "<ButtonRelease-1>", self.on_release)

                MovableResizableCircle.contador_circulo += 1

            def create_oval(self, x, y, radius_x, radius_y, fill):
                x1 = x - radius_x
                y1 = y - radius_y
                x2 = x + radius_x
                y2 = y + radius_y

                self.oval = self.canvas.create_oval(x1, y1, x2, y2, fill=fill, outline="black")
                self.padx = self.canvas.coords(self.oval)[0]
                self.pady = self.canvas.coords(self.oval)[1]
                self.new_oval_list()

            def create_circle(self, x, y, radius, fill):
                x1 = x - radius
                y1 = y - radius
                x2 = x + radius
                y2 = y + radius

                self.oval = self.canvas.create_oval(x1, y1, x2, y2, fill=fill, outline="black")
                self.padx = self.canvas.coords(self.oval)[0]
                self.pady = self.canvas.coords(self.oval)[1]
                self.new_oval_list()

            def new_oval_list(self):
                new_obj = {
                    "nome": self.nomeobj,
                    "x": self.canvas.coords(self.oval)[0],
                    "y": self.canvas.coords(self.oval)[1],
                    "width": self.width,
                    "height": self.height,
                    "color": self.fill
                }
                objetos.append(new_obj)

            def on_press(self, event):
                self.is_dragging = True
                self.start_x_drag = event.x
                self.start_y_drag = event.y      

            def on_drag(self, event):
                if self.is_dragging:
                    dx = event.x - self.start_x_drag
                    dy = event.y - self.start_y_drag
                    self.canvas.move(self.oval, dx, dy)
                    self.start_x_drag = event.x
                    self.start_y_drag = event.y

            def on_release(self, event):
                self.is_dragging = False
                self.new_position(event)

            def new_position(self, event):
                global objetos
                info = f"\nNome: {self.nomeobj}\nAltura: {self.height}\nLargura: {self.width}\nCor: {self.fill}\nPosição X: {self.canvas.coords(self.oval)[0]}\nPosição Y: {self.canvas.coords(self.oval)[1]}"
                for objeto in objetos:
                    if objeto["nome"] == self.nomeobj:
                        objeto["x"] = self.canvas.coords(self.oval)[0]
                        objeto["y"] = self.canvas.coords(self.oval)[1]
                os.system("cls")
                print(info)
                print(objetos)

        class MovableLine:
            contador_linha = 0
            def __init__(self, canvas, x1, y1, x2, y2, fill="black", width=2):
                self.canvas = canvas
                self.line = canvas.create_line(x1, y1, x2, y2, fill=fill, width=width)
                self.nomeobj = f"Linha-{MovableLine.contador_linha + 1}"
                self.selected = False
                self.canvas.tag_bind(self.line, "<ButtonPress-1>", self.on_press)
                self.canvas.tag_bind(self.line, "<B1-Motion>", self.on_drag)
                self.canvas.tag_bind(self.line, "<ButtonRelease-1>", self.on_release)
                self.width = width
                self.fill = fill
                self.start_x = x1
                self.start_y = y1
                self.end_x = x2
                self.end_y = y2

                MovableLine.contador_linha += 1

                self.padx = self.canvas.coords(self.line)[0]
                self.pady = self.canvas.coords(self.line)[1]
                self.new_line_list()

            def new_line_list(self):
                new_obj = {
                    "nome": self.nomeobj,
                    "x": self.canvas.coords(self.line)[0],
                    "y": self.canvas.coords(self.line)[1],
                    "width": self.width,
                    "color": self.fill
                }
                objetos.append(new_obj)

            def on_press(self, event):
                self.selected = True
                self.start_x = event.x
                self.start_y = event.y

            def on_drag(self, event):
                if self.selected:
                    dx = event.x - self.start_x
                    dy = event.y - self.start_y
                    self.canvas.move(self.line, dx, dy)
                    self.start_x = event.x
                    self.start_y = event.y
                    self.end_x += dx
                    self.end_y += dy

            def on_release(self, event):
                self.selected = False
                self.new_position(event)

            def new_position(self, event):
                global objetos
                info = f"\nNome: {self.nomeobj}\nLargura: {self.width}\nCor: {self.fill}\nPosição X: {self.canvas.coords(self.line)[0]}\nPosição Y: {self.canvas.coords(self.line)[1]}"
                for objeto in objetos:
                    if objeto["nome"] == self.nomeobj:
                        objeto["x"] = self.canvas.coords(self.line)[0]
                        objeto["y"] = self.canvas.coords(self.line)[1]
                os.system("cls")
                print(info)
                print(objetos)

        #Configurações da janela
        softwin.title(f"SmartBuild - Projeto( {nome} )")
        softwin.iconbitmap('./img/icon.ico')
        window_width = 1280
        window_height = 675

        screen_width = softwin.winfo_screenwidth() # Obter a largura e altura da tela
        screen_height = softwin.winfo_screenheight()

        x = int((screen_width/2) - (window_width/2)) # Calcular a posição x e y para centralizar a janela
        y = int((screen_height/2) - (window_height/2))

        softwin.geometry("{}x{}+{}+{}".format( # Configurar a janela para abrir no centro da tela
                                                window_width, 
                                                window_height,
                                                x,
                                                y))

        #Variaveis
        zoom_value = 100 #zoom
        #Fontes Pré-Definidas
        font_bold = CTkFont( #Criando fonte bold
                        family="Arial",
                        size=16,
                        weight="bold",
                        underline=True
        )
        font_bold2 = CTkFont( #Criando fonte bold
                        family="Arial",
                        size=15,
                        weight="bold"
        )
        font_2 = CTkFont( #Criando fonte bold
                        family="Arial",
                        size=12,
        )


        #Funções
        def create_frame_quadrado(): # CRIANDO UM FRAME PARA CRIAR QUADRADOS
            global frame_select_isopen
            if frame_select_isopen == 1:
                return
            else:   
                def create_quadrado(event): #Func para pegar as medidas do quadrado criar-lo e puxar a class MovableResizableQuadrado
                    try:
                        largura = float(inputLarg_quadrado.get())
                        altura = float(inputAltu_quadrado.get())
                        preenchimento = inputColor_quadrado.get()
                        
                        quadrado = MovableResizableQuadrado(canvas, 100, 100, altura, largura, fill=preenchimento)
                        print(objetos)
                        canvas.update_idletasks()
                    except:
                        print("...")

                def entra_input_quadrado(event): #Func para criar caixa de instrução sobre preenchimento do objeto
                    global input_quadrado
                    input_quadrado = tk.Label(
                        master=softwin,
                        text="•Caso queira um objeto sem preenchimento\ndeixe está caixa em branco.                    \n•Exemplo de input:Red or #codigo_da_cor.   ",
                        font=("Arial", 8),
                        bg="#070707",
                        fg="#ffffff"
                        )
                    input_quadrado.place(x=880, y=245, anchor="w")
                def sai_input_quadrado(event):
                    global input_quadrado

                    if input_quadrado is not None:
                        input_quadrado.destroy()
                        input_quadrado = None

                frame_select_isopen += 1
                frame_Cquadrado = customtkinter.CTkFrame( #Cria o frame para criar o quadrado
                                            master=canvas, 
                                            corner_radius=10, 
                                            width=300, 
                                            height=300
                ) 
                frame_Cquadrado.place(relx=0.99, rely=0.24, anchor="e")

                label_quadrado = customtkinter.CTkLabel( #Label criando quadrado
                                            master=frame_Cquadrado, 
                                            text="Criando quadrado", 
                                            text_color="white", 
                                            font=font_bold
                )
                label_quadrado.place(relx=0.3, rely=0.14, anchor="center")
                
                largura_quadrado = customtkinter.CTkLabel( #Largura
                                            master=frame_Cquadrado, 
                                            text="Largura: ", 
                                            text_color="white", 
                                            font=font_2
                )
                largura_quadrado.place(relx=0.1, rely=0.18)
                inputLarg_quadrado = customtkinter.CTkEntry( 
                                            master=frame_Cquadrado, 
                                            placeholder_text="Digite aqui", 
                                            font=font_2
                )
                px_quadrado = customtkinter.CTkLabel(
                                            master=frame_Cquadrado, 
                                            text=".px", 
                                            font=("Arial", 14), 
                                            text_color="gray"
                )
                inputLarg_quadrado.place(relx=0.1, rely=0.28)
                px_quadrado.place(relx=0.57, rely=0.29)

                altura_quadrado = customtkinter.CTkLabel(  #Altura 
                                            master=frame_Cquadrado, 
                                            text="Altura: ", 
                                            text_color="white", 
                                            font=font_2
                )
                altura_quadrado.place(relx=0.1, rely=0.40)
                inputAltu_quadrado = customtkinter.CTkEntry( 
                                            master=frame_Cquadrado, 
                                            placeholder_text="Digite aqui", 
                                            font=font_2
                )
                px_quadrado = customtkinter.CTkLabel(   
                                            master=frame_Cquadrado, 
                                            text=".px", 
                                            font=("Arial", 14), 
                                            text_color="gray"
                )
                inputAltu_quadrado.place(relx=0.1, rely=0.50)
                px_quadrado.place(relx=0.57, rely=0.51)
                
                preench_quadrado = customtkinter.CTkLabel( #Preenchimento
                                            master=frame_Cquadrado, 
                                            text="Preenchimento: ", 
                                            text_color="white", 
                                            font=font_2
                )
                preench_quadrado.place(relx=0.1, rely=0.62)
                inputColor_quadrado = customtkinter.CTkEntry(
                                            master=frame_Cquadrado, 
                                            placeholder_text="Digite a cor aqui*", 
                                            font=font_2
                )
                inputColor_quadrado.place(relx=0.1, rely=0.72)
                inputColor_quadrado.bind("<Enter>", entra_input_quadrado)
                inputColor_quadrado.bind("<Leave>", sai_input_quadrado)

                button_quadrado = customtkinter.CTkButton( #Button para criar o quadrado
                                            master=frame_Cquadrado, 
                                            text="Criar", 
                                            font=font_bold2, 
                                            fg_color="#F47D29", 
                                            hover_color="#ED6404",  
                )
                button_quadrado.place(relx=0.1, rely=0.87)
                button_quadrado.bind("<Button-1>", create_quadrado)
                softwin.bind("<Return>", create_quadrado)

                Cquadrado_frame_top = customtkinter.CTkFrame(   
                                                master=frame_Cquadrado, 
                                                corner_radius=5
                )
                Cquadrado_frame_top.place(x=0, y=0, relwidth=1, relheight=0.08)

                advancedQuadrado = customtkinter.CTkButton( 
                                            master= Cquadrado_frame_top,text="Avançado", 
                                            fg_color="#333333", 
                                            width=10, 
                                            height=25, 
                                            corner_radius=0, 
                                            hover_color="#2b2b2b", 
                                            border_width=1, 
                                            border_color="#2b2b2b"
                )
                advancedQuadrado.place(x=2,y=0)

                simpleQuadrado = customtkinter.CTkButton(
                                            master= Cquadrado_frame_top,text="Simples", 
                                            fg_color="#333333", 
                                            width=15, 
                                            height=25, 
                                            corner_radius=0, 
                                            hover_color="#2b2b2b", 
                                            border_width=1,
                                            border_color="#2b2b2b"
                )
                simpleQuadrado.place(x=66,y=0)

                x = customtkinter.CTkButton( #Button para fechar o frame de criação
                                master=frame_Cquadrado,
                                text="x",
                                font=("Arial", 13), 
                                text_color="#1b1b1b",
                                fg_color="#333333",
                                hover_color="#333333",
                                corner_radius=30,
                                width=5,
                                height=5, 
                                command=lambda:frame_Cquadrado_close()
                )
                x.place(x=285, y=0)

                def frame_Cquadrado_close():
                    global frame_select_isopen
                    frame_select_isopen -= 1
                    frame_Cquadrado.destroy()
                    softwin.unbind("<Return>")
        def create_frame_circulo(): # CRIANDO UM FRAME PARA CRIAR CIRCULOS
            global frame_select_isopen
            if frame_select_isopen == 1:
                return
            else:   
                def create_circulo(event):
                    largura = float(inputLarg_circulo.get())
                    altura = float(inputAltu_circulo.get())
                    preenchimento = inputColor_circulo.get()

                    objeto_nomeado = MovableResizableCircle(canvas, 200, 200, largura, altura, preenchimento)
                    print(objetos)
                    canvas.update_idletasks()
                    
                def entra_input_circulo(event):
                    global input_circulo
                    input_circulo = tk.Label(
                        master=softwin,
                        text="•Caso queira um objeto sem preenchimento\ndeixe está caixa em branco.                    \n•Exemplo de input:Red or #codigo_da_cor.   ",
                        font=("Arial", 8),
                        bg="#070707",
                        fg="#ffffff"
                        )
                    input_circulo.place(x=880, y=245, anchor="w")
                    
                def sai_input_circulo(event):
                    global input_circulo

                    if input_circulo is not None:
                        input_circulo.destroy()
                        input_circulo = None

                frame_select_isopen += 1
                frame_Ccirculo = customtkinter.CTkFrame(master=canvas, corner_radius=10, width=300, height=300) #Cria o frame novo
                frame_Ccirculo.place(relx=0.99, rely=0.24, anchor="e")

                label_circulo = customtkinter.CTkLabel(master=frame_Ccirculo, text="Criando circulo", text_color="white", font=font_bold,)
                label_circulo.place(relx=0.3, rely=0.14, anchor="center")
                
                largura_circulo = customtkinter.CTkLabel(master=frame_Ccirculo, text="Largura: ", text_color="white", font=font_2,)
                largura_circulo.place(relx=0.1, rely=0.18)
                inputLarg_circulo = customtkinter.CTkEntry(master=frame_Ccirculo, placeholder_text="Digite aqui", font=font_2)
                px_circulo = customtkinter.CTkLabel(master=frame_Ccirculo, text=".px", font=("Arial", 14), text_color="gray")
                inputLarg_circulo.place(relx=0.1, rely=0.28)
                px_circulo.place(relx=0.57, rely=0.29)

                altura_circulo = customtkinter.CTkLabel(master=frame_Ccirculo, text="Altura: ", text_color="white", font=font_2,)
                altura_circulo.place(relx=0.1, rely=0.40)
                inputAltu_circulo = customtkinter.CTkEntry(master=frame_Ccirculo, placeholder_text="Digite aqui", font=font_2)
                px_circulo = customtkinter.CTkLabel(master=frame_Ccirculo, text=".px", font=("Arial", 14), text_color="gray")
                inputAltu_circulo.place(relx=0.1, rely=0.50)
                px_circulo.place(relx=0.57, rely=0.51)
                
                preench_circulo = customtkinter.CTkLabel(master=frame_Ccirculo, text="Preenchimento: ", text_color="white", font=font_2,)
                preench_circulo.place(relx=0.1, rely=0.62)
                inputColor_circulo = customtkinter.CTkEntry(master=frame_Ccirculo, placeholder_text="Digite a cor aqui*", font=font_2)
                inputColor_circulo.place(relx=0.1, rely=0.72)
                inputColor_circulo.bind("<Enter>", entra_input_circulo)
                inputColor_circulo.bind("<Leave>", sai_input_circulo)

                button_circulo = customtkinter.CTkButton(master=frame_Ccirculo, text="Criar", font=font_bold2, fg_color="#F47D29", hover_color="#ED6404")
                button_circulo.place(relx=0.1, rely=0.87)
                button_circulo.bind("<Button-1>", create_circulo)
                softwin.bind("<Return>", create_circulo)

                Ccirculo_frame_top = customtkinter.CTkFrame(master=frame_Ccirculo, corner_radius=5)
                Ccirculo_frame_top.place(x=0, y=0, relwidth=1, relheight=0.08)

                advancedciruclo = customtkinter.CTkButton(master= Ccirculo_frame_top,text="Avançado", fg_color="#333333", width=10, height=25, corner_radius=0, hover_color="#2b2b2b", border_width=1, border_color="#2b2b2b")
                advancedciruclo.place(x=2,y=0)

                simpleciruclo = customtkinter.CTkButton(master= Ccirculo_frame_top,text="Simples", fg_color="#333333", width=15, height=25, corner_radius=0, hover_color="#2b2b2b", border_width=1, border_color="#2b2b2b")
                simpleciruclo.place(x=66,y=0)

                x = customtkinter.CTkButton(
                                    master=frame_Ccirculo,
                                    text="x",
                                    font=("Arial", 13), 
                                    text_color="#1b1b1b",
                                    fg_color="#333333",
                                    hover_color="#333333",
                                    corner_radius=30,
                                    width=5,
                                    height=5, 
                                    command=lambda:frame_Cciruclo_close())
                x.place(x=285, y=0)

                def frame_Cciruclo_close():
                    global frame_select_isopen
                    frame_select_isopen -= 1
                    frame_Ccirculo.destroy()
                    softwin.unbind("<Return>")
        def create_frame_triangulo(): # CRIANDO UM FRAME PARA CRIAR TRIANGULOS
            global frame_select_isopen
            global objetos
            if frame_select_isopen == 1:
                return
            else:
                def create_triangulo(event):
                    largura = float(inputLarg_triangulo.get())
                    altura = float(inputAltu_triangulo.get())
                    preenchimento = inputColor_triangulo.get()

                    triangulo = MovableResizableTriangle(canvas, 100, 100, altura, largura, fill=preenchimento)
                    print(objetos)
                    canvas.update_idletasks()
                    
                    
                def entra_input_triangulo(event):
                    global input_triangulo
                    input_triangulo = tk.Label(
                        master=softwin,
                        text="•Caso queira um objeto sem preenchimento\ndeixe está caixa em branco.                    \n•Exemplo de input:Red or #codigo_da_cor.   ",
                        font=("Arial", 8),
                        bg="#070707",
                        fg="#ffffff"
                        )
                    input_triangulo.place(x=880, y=245, anchor="w")
                    
                def sai_input_triangulo(event):
                    global input_triangulo

                    if input_triangulo is not None:
                        input_triangulo.destroy()
                        input_triangulo = None

                frame_select_isopen += 1
                frame_Ctriangulo = customtkinter.CTkFrame(master=canvas, corner_radius=10, width=300, height=300) #Cria o frame novo
                frame_Ctriangulo.place(relx=0.99, rely=0.24, anchor="e")

                label_triangulo = customtkinter.CTkLabel(master=frame_Ctriangulo, text="Criando triangulo", text_color="white", font=font_bold,)
                label_triangulo.place(relx=0.3, rely=0.14, anchor="center")
                
                largura_triangulo = customtkinter.CTkLabel(master=frame_Ctriangulo, text="Largura: ", text_color="white", font=font_2,)
                largura_triangulo.place(relx=0.1, rely=0.18)
                inputLarg_triangulo = customtkinter.CTkEntry(master=frame_Ctriangulo, placeholder_text="Digite aqui", font=font_2)
                px_triangulo = customtkinter.CTkLabel(master=frame_Ctriangulo, text=".px", font=("Arial", 14), text_color="gray")
                inputLarg_triangulo.place(relx=0.1, rely=0.28)
                px_triangulo.place(relx=0.57, rely=0.29)

                altura_triangulo = customtkinter.CTkLabel(master=frame_Ctriangulo, text="Altura: ", text_color="white", font=font_2,)
                altura_triangulo.place(relx=0.1, rely=0.40)
                inputAltu_triangulo = customtkinter.CTkEntry(master=frame_Ctriangulo, placeholder_text="Digite aqui", font=font_2)
                px_triangulo = customtkinter.CTkLabel(master=frame_Ctriangulo, text=".px", font=("Arial", 14), text_color="gray")
                inputAltu_triangulo.place(relx=0.1, rely=0.50)
                px_triangulo.place(relx=0.57, rely=0.51)
                
                preench_triangulo = customtkinter.CTkLabel(master=frame_Ctriangulo, text="Preenchimento: ", text_color="white", font=font_2,)
                preench_triangulo.place(relx=0.1, rely=0.62)
                inputColor_triangulo = customtkinter.CTkEntry(master=frame_Ctriangulo, placeholder_text="Digite a cor aqui*", font=font_2)
                inputColor_triangulo.place(relx=0.1, rely=0.72)
                inputColor_triangulo.bind("<Enter>", entra_input_triangulo)
                inputColor_triangulo.bind("<Leave>", sai_input_triangulo)

                button_triangulo = customtkinter.CTkButton(master=frame_Ctriangulo, text="Criar", font=font_bold2, fg_color="#F47D29", hover_color="#ED6404")
                button_triangulo.place(relx=0.1, rely=0.87)
                button_triangulo.bind("<Button-1>", create_triangulo)
                softwin.bind("<Return>", create_triangulo)

                Ctriangulo_frame_top = customtkinter.CTkFrame(master=frame_Ctriangulo, corner_radius=5)
                Ctriangulo_frame_top.place(x=0, y=0, relwidth=1, relheight=0.08)

                advancedtriangulo = customtkinter.CTkButton(master= Ctriangulo_frame_top,text="Avançado", fg_color="#333333", width=10, height=25, corner_radius=0, hover_color="#2b2b2b", border_width=1, border_color="#2b2b2b")
                advancedtriangulo.place(x=2,y=0)

                simpletriangulo = customtkinter.CTkButton(master= Ctriangulo_frame_top,text="Simples", fg_color="#333333", width=15, height=25, corner_radius=0, hover_color="#2b2b2b", border_width=1, border_color="#2b2b2b")
                simpletriangulo.place(x=66,y=0)

                x = customtkinter.CTkButton(
                                    master=frame_Ctriangulo,
                                    text="x",
                                    font=("Arial", 13), 
                                    text_color="#1b1b1b",
                                    fg_color="#333333",
                                    hover_color="#333333",
                                    corner_radius=30,
                                    width=5,
                                    height=5, 
                                    command=lambda:frame_Ctriangulo_close())
                x.place(x=285, y=0)

                def frame_Ctriangulo_close():
                    global frame_select_isopen
                    frame_select_isopen -= 1
                    frame_Ctriangulo.destroy()
                    softwin.unbind("<Return>")
        def create_linha(): #CRIANDO LINHA
            global frame_select_isopen
            linha = MovableLine(canvas, 100, 100, 500, 100, fill="black",width=1)
            print(objetos)
            canvas.update_idletasks()   
                
            """frame_select_isopen += 1
            frame_Clinha = customtkinter.CTkFrame(master=canvas, corner_radius=10, width=300, height=300) #Cria o frame novo
            frame_Clinha.place(relx=0.99, rely=0.24, anchor="e")

            label_linha = customtkinter.CTkLabel(master=frame_Clinha, text="Criando linha", text_color="white", font=font_bold,)
            label_linha.place(relx=0.3, rely=0.14, anchor="center")

            x = customtkinter.CTkButton(
                                master=frame_Clinha,
                                text="x",
                                font=("Arial", 13), 
                                text_color="#1b1b1b",
                                fg_color="#333333",
                                hover_color="#333333",
                                corner_radius=30,
                                width=5,
                                height=5, 
                                command=lambda:frame_Clinha_close())
            x.place(x=285, y=0)

            def frame_Clinha_close():
                global frame_select_isopen
                frame_select_isopen -= 1
                frame_Clinha.destroy()
"""
        def on_canvas_scroll(event):
            global zoom_value
            if event.state == 12:
                if event.delta > 0 and zoom_value <= 4950:
                    zoom_value *= 1.1
                    canvas.scale("all", event.x, event.y, 1.1, 1.1)
                elif event.delta < 0 and zoom_value > 1:
                    zoom_value *= 0.9
                    canvas.scale("all", event.x, event.y, 0.9, 0.9)
                zoom_label.config(text=f"{zoom_value:.0f}%")

        def move_canvas_up(event):
            canvas.move("all", 0, -10)

        def move_canvas_down(event):
            canvas.move("all", 0, 10)

        def move_canvas_left(event):
            canvas.move("all", -10, 0)

        def move_canvas_right(event):
            canvas.move("all", 10, 0)

        #Funções mouse entra/sai
        def mouse_entra_quadrado(event): #Button criar quadrado txt
            global button_quadrado
            global button_quadrado_btn
            button_quadrado_btn = tk.Label(
                master=canvas,
                text="•Criar Quadrado",
                font=("Arial", 8),
                bg="#070707",
                fg="#ffffff"
            )
            button_quadrado_btn.place(x=5, y=3)
        def mouse_sai_quadrado(event):
            global button_quadrado
            global button_quadrado_btn

            if button_quadrado is not None:
                button_quadrado_btn.destroy()
                button_quadrado_btn = None    
                
        def mouse_entra_triangulo(event): #Button crirar triangulo txt
            global button_triangulo
            global button_triangulo_btn
            button_triangulo_btn = tk.Label(
                master=canvas,
                text="•Criar Triângulo",
                font=("Arial", 8),
                bg="#070707",
                fg="#ffffff"
            )
            button_triangulo_btn.place(x=58, y=3)
        def mouse_sai_triangulo(event):
            global button_triangulo
            global button_triangulo_btn

            if button_triangulo is not None:
                button_triangulo_btn.destroy()
                button_triangulo_btn = None   

        def mouse_entra_circulo(event): #Button crirar circulo txt
            global button_circulo
            global button_circulo_btn
            button_circulo_btn = tk.Label(
                master=canvas,
                text="•Criar Circulo",
                font=("Arial", 8),
                bg="#070707",
                fg="#ffffff"
            )
            button_circulo_btn.place(x=111, y=3)
        def mouse_sai_circulo(event):
            global button_circulo
            global button_circulo_btn

            if button_circulo is not None:
                button_circulo_btn.destroy()
                button_circulo_btn = None 

        def mouse_entra_linha(event): #Button crirar circulo txt
            global button_linha
            global button_linha_btn
            button_linha_btn = tk.Label(
                master=canvas,
                text="•Criar linha",
                font=("Arial", 8),
                bg="#070707",
                fg="#ffffff"
            )
            button_linha_btn.place(x=164, y=3)
        def mouse_sai_linha(event):
            global button_linha
            global button_linha_btn

            if button_linha is not None:
                button_linha_btn.destroy()
                button_linha_btn = None 
        
        #Ler arquivos
        arquivo_path = f"E:\\SmartBuild\\Projetos\\{nome}.json"

        def ler_arquivo_json(arquivo_path):
            try:
                with open(arquivo_path, "r") as arquivo_json:
                    dados_projeto = json.load(arquivo_json)
                return dados_projeto
            except FileNotFoundError:
                print(f"Arquivo {arquivo_path} não encontrado.")
                return None
            except json.JSONDecodeError:
                print(f"Erro ao decodificar o arquivo JSON {arquivo_path}.")
                return None
            
        dados_do_projeto = ler_arquivo_json(arquivo_path)

        if dados_do_projeto:

            estrutura = dados_do_projeto["Estrutura"]
            nome = dados_do_projeto["Nome"]
            medida = dados_do_projeto["Medida"]
            largura = dados_do_projeto["Largura"]
            comprimento = dados_do_projeto["Comprimento"]
            informacoes = dados_do_projeto["Informacoes"]

            os.system('cls')
            print("Estrutura:", estrutura)
            print(f"Nome do arquivo: {nome}.json")
            print("Tipo de medida:", medida)
            print("Largura terreno:", largura)
            print("Comprimento terreno:", comprimento)
            print("Informacoes:", informacoes)
            
        def salvar_projeto():
            estrutura = dados_do_projeto["Estrutura"]
            nome = dados_do_projeto["Nome"]
            medida = dados_do_projeto["Medida"]
            largura = dados_do_projeto["Largura"]
            comprimento = dados_do_projeto["Comprimento"]
            informacoes = dados_do_projeto["Informacoes"]

            projeto_data = {
                        "Estrutura": estrutura,
                        "Nome": nome,
                        "Medida": medida,
                        "Largura": largura,
                        "Comprimento": comprimento,
                        "Informacoes": informacoes,
                        "Objetos": objetos
                    }   
            
            with open(arquivo_path, "w") as arquivo_json:
            #dump para escrever a lista no arquivo JSON
                json.dump(projeto_data, arquivo_json, indent=4)
                print("Salvando...")
            tk.messagebox.showinfo("Sucesso", f"Projeto salvo em {nome}.json com exito!!!")
            softwin.lift()
            print(f"Os dados foram salvos em {nome}.json")
        
        def criar_quadrado(canvas, objeto):
            x = objeto["x"]
            y = objeto["y"]
            largura = objeto["width"]
            altura = objeto["height"]
            preenchimento = objeto["color"]
            
            quadrado = MovableResizableQuadrado(canvas, x, y, altura, largura, fill=preenchimento)

        def criar_triangulo(canvas, objeto):
            x = objeto["x"]
            y = objeto["y"]
            largura = objeto["width"]
            altura = objeto["height"]
            preenchimento = objeto["color"]
            
            triangulo = MovableResizableTriangle(canvas, x, y, altura, largura, fill=preenchimento)

        def criar_circulo(canvas, objeto):
            x = objeto["x"]
            y = objeto["y"]
            largura = objeto["width"]
            altura = objeto["height"]
            preenchimento = objeto["color"]
            
            oval = MovableResizableQuadrado(canvas, x, y, altura, largura, fill=preenchimento)
        
        def criar_linha(canvas, objeto):
            x = objeto["x"]
            y = objeto["y"]
            largura = objeto["width"]
            preenchimento = objeto["color"]
            
            line = MovableResizableQuadrado(canvas, x, y, largura, fill=preenchimento)

        #Frames
        canvas = tk.Canvas( #Main canvas do projeto
                master=softwin, 
                width=1036, 
                height=522, 
                bg="#ffffff", 
                highlightthickness=0
        )
        canvas.place(x=3, y=127, relwidth=0.996, relheight=1)
        canvas.bind_all("<MouseWheel>", on_canvas_scroll)
        canvas.bind_all("<MouseWheel>", on_canvas_scroll)
        
        frame_settings = customtkinter.CTkFrame( #Frame settings ao topo da tela
                                    master=softwin, 
                                    height=25, 
                                    corner_radius=0
        )
        frame_settings.place(x=0,y=0)
        frame_settings.place(relwidth=1)

        frame_boardtop = customtkinter.CTkFrame( #Frame com os contents, objetos e afins
                                    master=softwin, 
                                    height=99, 
                                    corner_radius=0
        )
        frame_boardtop.place(x = 2, rely=0.039, relwidth=0.996)

        frame_nothing = customtkinter.CTkFrame( #Frame abaixo da janela
                                master=softwin, 
                                height=27, 
                                corner_radius=0
        )
        frame_nothing.place(relx=0.0, rely=1.0, anchor='s')
        frame_nothing.place(relwidth=2)


        #Frame setting content
        file_menu = tk.Menu( #File
                        frame_settings,
                        tearoff=False,
                        bg="#2b2b2b",
                        fg="#ffffff",
                        activebackground="#2b2b2b",
                        activeforeground="#ffffff"
        )
        file_menu.add_command(label="Novo", command=None, activebackground="#191919")
        file_menu.add_command(label="Abrir", command=None, activebackground="#191919")
        file_menu.add_command(label="Salvar", command=salvar_projeto, activebackground="#191919")
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=None, activebackground="#191919")
        file_button = customtkinter.CTkButton(# Cria um botão no frame_settings para abrir o menu
                                            master=frame_settings,
                                            text="Arquivo",
                                            width=30,
                                            height=24,
                                            bg_color="#2b2b2b",
                                            fg_color="#2b2b2b",
                                            hover_color="#191919",
                                            corner_radius=0,
                                            command=lambda: file_menu.tk_popup(file_button.winfo_rootx(),
                                                                            file_button.winfo_rooty()+
                                                                            file_button.winfo_height())
                                        )
        file_button.place(x=1,y=0)

        #Labels
        zoom_label = tk.Label( #Zoom label no Canvas
                            master=canvas,
                            text=f"{zoom_value}%",
                            font=("Arial", 10)
                            )
        zoom_label.place(relx=0.001, rely=0.74)

        #Botões
        button_quadrado = customtkinter.CTkButton( #Button para cirar quadrado
                        master=frame_boardtop,
                        text="▢",
                        font=("Arial", 40),
                        image=None ,
                        width=50,
                        height=60,
                        corner_radius=5,
                        fg_color="#2b2b2b",
                        hover_color="#242424",
                        border_color="#242424",
                        border_width=1,
                        command=create_frame_quadrado
                        )
        button_quadrado.place(x=5, rely=0.35)
        button_quadrado.bind("<Enter>", mouse_entra_quadrado)
        button_quadrado.bind("<Leave>", mouse_sai_quadrado)

        button_triangulo = customtkinter.CTkButton( #Button para criar triangulo
                        master=frame_boardtop,
                        text="△",
                        font=("Arial", 25),
                        image=None ,
                        width=50,
                        height=60,
                        corner_radius=5,
                        fg_color="#2b2b2b",
                        hover_color="#242424",
                        border_color="#242424",
                        border_width=1,
                        command=create_frame_triangulo
                        )
        button_triangulo.place(x=58, rely=0.35)
        button_triangulo.bind("<Enter>", mouse_entra_triangulo)
        button_triangulo.bind("<Leave>", mouse_sai_triangulo)

        button_circulo = customtkinter.CTkButton( #Button para criar circulo
                        master=frame_boardtop,
                        text="O",
                        font=("Arial", 25),
                        image=None ,
                        width=50,
                        height=60,
                        corner_radius=5,
                        fg_color="#2b2b2b",
                        hover_color="#242424",
                        border_color="#242424",
                        border_width=1,
                        command=create_frame_circulo
                        )
        button_circulo.place(x=111, rely=0.35)
        button_circulo.bind("<Enter>", mouse_entra_circulo)
        button_circulo.bind("<Leave>", mouse_sai_circulo)
        
        button_linha = customtkinter.CTkButton( #Button para criar linha
                        master=frame_boardtop,
                        text="/",
                        font=("Arial", 25),
                        image=None ,
                        width=50,
                        height=60,
                        corner_radius=5,
                        fg_color="#2b2b2b",
                        hover_color="#242424",
                        border_color="#242424",
                        border_width=1,
                        command=create_linha
                        )
        button_linha.place(x=164, rely=0.35)
        button_linha.bind("<Enter>", mouse_entra_linha)
        button_linha.bind("<Leave>", mouse_sai_linha)

        move_up_button = customtkinter.CTkButton(canvas, text="↑", fg_color="#2b2b2b", border_color="#242424", border_width=1, width=40, height=40, hover_color="#242424", corner_radius=5)
        move_up_button.place(x=1175, y=425)
        move_up_button.bind("<Button-1>", move_canvas_up)
        softwin.bind("<Up>", move_canvas_up)

        move_down_button = customtkinter.CTkButton(canvas, text="↓", fg_color="#2b2b2b", border_color="#242424", border_width=1, width=40, height=40, hover_color="#242424", corner_radius=5)
        move_down_button.place(x=1175, y=470)
        move_down_button.bind("<Button-1>", move_canvas_down)
        softwin.bind("<Down>", move_canvas_down)

        move_left_button = customtkinter.CTkButton(canvas, text="←", fg_color="#2b2b2b", border_color="#242424", border_width=1, width=40, height=40, hover_color="#242424", corner_radius=5)
        move_left_button.place(x=1130, y=470)
        move_left_button.bind("<Button-1>", move_canvas_left)
        softwin.bind("<Left>", move_canvas_left)

        move_right_button = customtkinter.CTkButton(canvas, text="→", fg_color="#2b2b2b", border_color="#242424", border_width=1, width=40, height=40, hover_color="#242424", corner_radius=5)
        move_right_button.place(x=1220, y=470)
        move_right_button.bind("<Button-1>", move_canvas_right)
        softwin.bind("<Right>", move_canvas_right)
        
        def on_close(event):
            global project_is_open
            global nome_arquivo
            project_is_open -= 1
            nome_arquivo = ""
        softwin.bind("<Destroy>", on_close)

        with open(arquivo_path, "r") as file: #Verifica se tem algum objeto com o nome quadrado no arquivo.json
            data = json.load(file)
            a = 1
            for objeto in data["Objetos"]:
                if objeto["nome"] == f"Quadrado-{a}":
                    criar_quadrado(canvas, objeto)
                    a += 1

        with open(arquivo_path, "r") as file: #Verifica se tem algum objeto com o nome triangulo no arquivo.json
            data = json.load(file)
            a = 1
            for objeto in data["Objetos"]:
                if objeto["nome"] == f"Triangulo-{a}":
                    criar_quadrado(canvas, objeto)
                    a += 1

        with open(arquivo_path, "r") as file: #Verifica se tem algum objeto com o nome circulo no arquivo.json
            data = json.load(file)
            a = 1
            for objeto in data["Objetos"]:
                if objeto["nome"] == f"Circulo-{a}":
                    criar_quadrado(canvas, objeto)
                    a += 1

        with open(arquivo_path, "r") as file: #Verifica se tem algum objeto com o nome linha no arquivo.json
            data = json.load(file)
            a = 1
            for objeto in data["Objetos"]:
                if objeto["nome"] == f"Linha-{a}":
                    criar_quadrado(canvas, objeto)
                    a += 1

        softwin.mainloop()
    
  
def create_new_project():  #cria novo projeto  
    global frame_newProject_isopen
    if frame_newProject_isopen == 1:
        return
    else:
        style = ThemedStyle(userwin)
        style.set_theme("clam")

        estruturas = ["Casa", "Sobrado", "Apartamento", "Comércio", "SuperMercado", "Customizado"]
        medidas = ["Metros", "Pés"]

        def on_estrutura_selection(event):
            global custom_estrutura
            global selecionado_estrutura

            selected_estrutura = tipo_estrutura_lista.get()

            if selected_estrutura == "Customizado":
                custom_estrutura_lbl = customtkinter.CTkLabel(master=newProjectbtn_frame, text="Estrutura personalizada:")
                custom_estrutura_lbl.place(x=251, y=135)
                custom_estrutura = customtkinter.CTkEntry(master=newProjectbtn_frame, width=190, height=28, corner_radius=3 ,placeholder_text="Digite aqui")
                custom_estrutura.place(x=250, y=160)
                print("Estrutura selecionada:", selected_estrutura)
                selecionado_estrutura += 1

            if selected_estrutura == "Casa" or selected_estrutura == "Sobrado" or selected_estrutura == "Apartamento" or selected_estrutura == "Comércio" or selected_estrutura == "SuperMercado":
                print("Estrutura selecionada:", selected_estrutura)
                if selecionado_estrutura == 1:
                    custom_estrutura.place_forget()
                    selecionado_estrutura -= 1
        
        def on_medida_selection(event):
            medida = medida_list.get()
            print("Tipo de medida selecionado: ", medida)

        def scroll_canvas(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        def newProjectbtn_frame_close():
            global frame_newProject_isopen
            canvas.unbind("<MouseWheel>")
            newProjectbtn_frame.unbind("<MouseWheel>")
            scrollbar.destroy()
            canvas.destroy()
            atualizar_lista_projetos()
            frame_newProject_isopen -= 1

        canvas = tk.Canvas(userwin, bg="#242424", width=720, height=480, highlightthickness=0)
        canvas.place(x=200, y=0)

        scrollbar = ttk.Scrollbar(userwin, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        style.configure("TScrollbar", troughcolor="#242424", background="#F47D29", gripcount=0 )

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<MouseWheel>", scroll_canvas)

        newProjectbtn_frame = customtkinter.CTkFrame(master=canvas, width=720, height=700, corner_radius=0, fg_color="#242424")
        canvas.create_window((0, 0), window=newProjectbtn_frame, anchor=tk.NW)
        newProjectbtn_frame.bind("<MouseWheel>", scroll_canvas)

        criando = customtkinter.CTkLabel(master=newProjectbtn_frame, text="Criando novo projeto:", font=font_criando)
        criando.place(x=10, y=10)

        workbentch_lbl = customtkinter.CTkLabel(master=newProjectbtn_frame, text="Mesa de trabalho:", font=font_creating, cursor="hand2")
        workbentch_lbl.place(x=20, y=50)

        nome_input_lbl = customtkinter.CTkLabel(master=newProjectbtn_frame, text="Nome do projeto:")
        nome_input_lbl.place(x=31, y=75)
        nome_input = customtkinter.CTkEntry(master=newProjectbtn_frame, width=200, height=28, placeholder_text="Nome do projeto", corner_radius=3)
        nome_input.place(x=30, y=100)

        estruta_list_lbl = customtkinter.CTkLabel(master=newProjectbtn_frame, text="Planta de um(a):")
        estruta_list_lbl.place(x=31, y=135)
        tipo_estrutura_lista = customtkinter.CTkOptionMenu(master=newProjectbtn_frame, width=200, height=28, values=estruturas, fg_color="#3F4042",button_color="#F47D29", button_hover_color="#ED6404", corner_radius=3, command=on_estrutura_selection)
        tipo_estrutura_lista.place(x=30, y=160)

        medida_list_lbl = customtkinter.CTkLabel(master=newProjectbtn_frame, text="Medida que será usada:")
        medida_list_lbl.place(x=31, y=195)
        medida_list = customtkinter.CTkOptionMenu(master=newProjectbtn_frame, width=200, height=28, values=medidas, fg_color="#3F4042",button_color="#F47D29", button_hover_color="#ED6404", corner_radius=3, command=on_medida_selection)
        medida_list.place(x=30, y=220)

        terreno_lbl = customtkinter.CTkLabel(master=newProjectbtn_frame, text="Sobre o terreno:", font=font_creating, cursor="hand2")
        terreno_lbl.place(x=20, y=300)

        largura_terreno_lbl = customtkinter.CTkLabel(master=newProjectbtn_frame, text="Largura do lote:")
        largura_terreno_lbl.place(x=31, y=325)
        largura_terreno = customtkinter.CTkEntry(master=newProjectbtn_frame, width=220, height=28, corner_radius=3, placeholder_text="Digite a largura do lote: ")
        largura_terreno.place(x=30, y=350)

        comprimento_terreno_lbl = customtkinter.CTkLabel(master=newProjectbtn_frame, text="Comprimento do lote:")
        comprimento_terreno_lbl.place(x=31, y=385)
        comprimento_terreno = customtkinter.CTkEntry(master=newProjectbtn_frame, width=220, height=28, corner_radius=3, placeholder_text="Digite o comprimento do lote: ")
        comprimento_terreno.place(x=30, y=410)

        legendaBox_lbl = customtkinter.CTkLabel(master=newProjectbtn_frame, text="Digite aqui informações referentes ao seu projeto: ")
        legendaBox_lbl.place(x=31, y=445)
        legendaBox = customtkinter.CTkTextbox(master=newProjectbtn_frame, text_color="white", fg_color="#2b2b2b", border_color="#1e1e1e", border_width=1)
        legendaBox.place(x=30, y=470)
        
        button_criar = customtkinter.CTkButton(master=newProjectbtn_frame, text="Criar projeto", font=font_bold2, fg_color="#F47D29", hover_color="#ED6404", command=lambda:create_project())
        button_criar.place(x = 500, y=640)

        x = customtkinter.CTkButton(
                            master=newProjectbtn_frame,
                            text=" X ",
                            font=("Arial", 13), 
                            text_color="black",
                            fg_color="#F47D29",
                            hover_color="#ED6404",
                            border_color="white",
                            border_width=2,
                            corner_radius=30,
                            width=10,
                            height=10, 
                            command=lambda:newProjectbtn_frame_close())
        x.place(x=670, y=10)


        def atualizar_lista_projetos():
            global lista_projetos
            projetos_do_usuario = buscar_projetos_por_usuario(username)
            lista_projetos = projetos_do_usuario
            exibir_projetos_na_tela(projetos_do_usuario)
            userwin.update()

        def create_project():
            global frame_newProject_isopen
            global custom_estrutura

            value_before_x = None
            value_after_x = None


            estrutura = tipo_estrutura_lista.get() 
            custestrutura = None
            if custom_estrutura:
                custestrutura = custom_estrutura.get()

            nome = nome_input.get()
            medida = medida_list.get()
            largura = largura_terreno.get()
            comprimento = comprimento_terreno.get()
            informacoes = legendaBox.get("1.0", "end-1c")
            largura_table = value_before_x if value_before_x else "N/A"
            comprimento_table = value_after_x if value_after_x else "N/A"

            if nome == "" or largura == "" or comprimento == "":
                empty_inputs = []
                if nome == "":
                    empty_inputs.append("Nome")
                if largura == "":
                    empty_inputs.append("largura")
                if comprimento == "":
                    empty_inputs.append("comprimento")        
                tk.messagebox.showinfo("Error", "Os seguintes campos estão vazios: " + ", ".join(empty_inputs))
                print("Erro ao criar projeto... espera-se que nenhum campo (exceto informações) fique vazio")
                return

            if estrutura == "Customizado" and custom_estrutura is None:
                tk.messagebox.showinfo("Error", "Você selecionou uma estrutura personalizada, mas não preencheu o campo personalizado.")
                print("Erro ao criar projeto... estrutura personalizada sem preenchimento")
                return
            
            else:
                filetypes = (("Arquivo SmartBuild", "*.json"), ("Todos os arquivos", "*.*"))
                arquivo = filedialog.asksaveasfile(mode="w", defaultextension=".json", filetypes=filetypes, initialfile=nome , initialdir="E:\SmartBuild\Projetos")
                if arquivo is not None:
                    
                    arquivo_nome = f"{nome}.json"  # Nome do arquivo é definido com base no nome do projeto
                    arquivo_path = os.path.join("E:\SmartBuild\Projetos", arquivo_nome)  # Caminho completo do arquivo

                    projeto_data = {
                        "Estrutura": estrutura,
                        "Nome": nome,
                        "Medida": medida,
                        "Largura": largura,
                        "Comprimento": comprimento,
                        "Informacoes": informacoes
                    }   

                    with open(arquivo_path, "w") as arquivo_json:
                        json.dump(projeto_data, arquivo_json)
                    connection = conect()
                    cursor = connection.cursor()
                        
                    cursor.execute("INSERT INTO projeto (user_projeto, nome_projeto, tipo_projeto, terreno_largura, terreno_comprimento, tipo_medida, descricao_projeto ) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, nome, estrutura, largura, comprimento, medida, informacoes ))

                    connection.commit()
                    connection.close()
                    tk.messagebox.showinfo("Sucesso", "Projeto criado com sucesso!!")
                    print("Sucesso ao criar projeto...")
                    canvas.unbind("<MouseWheel>")
                    newProjectbtn_frame.unbind("<MouseWheel>")
                    frame_newProject_isopen -= 1
                    atualizar_lista_projetos()
                    scrollbar.destroy()
                    newProjectbtn_frame.destroy()
                    canvas.destroy()

                    frame_newProject_isopen += 1
                else:
                    tk.messagebox.showinfo("Error", "Caminho para salvar o arquivo.json não selecionado.")
                    print("Erro ao criar projeto... Caminho para salvar o arquivo do projeto não foi selecionado")

    
#Frames
boardleft_frame = customtkinter.CTkFrame( #Main frame a esquerda para button criar projetos e informações do usuario
                            master=userwin, 
                            width=200, 
                            height=480, 
                            border_width=1, 
                            border_color="#1e1e1e", 
                            corner_radius=0
)
boardleft_frame.place(x=0,y=0)

perfil_frame = customtkinter.CTkFrame( #Frame ao topo do frame boardleft, para foto do usuario e settings do perfil
                        master=boardleft_frame, 
                        width=170, 
                        height=50, 
                        border_width=1, 
                        border_color="#1e1e1e", 
                        corner_radius=0
)
perfil_frame.place(x=15, y= 10)

perfil_img = customtkinter.CTkFrame( #Imagem frame perfil
                        master=perfil_frame,
                        width=35,
                        height=35,
                        corner_radius=0,
                        border_width=1,
                        border_color="#1e1e1e"
)
perfil_img.place(x=10, y=8)

boardleft_frame_dados = customtkinter.CTkFrame( #Frame abaixo do perfil_frame para dados do usuario
                                master=boardleft_frame, 
                                width=170, 
                                height=400, 
                                border_width=1, 
                                border_color="#1e1e1e", 
                                corner_radius=0
)
boardleft_frame_dados.place(x=15, y=70)

newProjectbtn = customtkinter.CTkButton( #Button para criar novo projeto
                        master=boardleft_frame_dados, 
                        text="Novo Projeto", 
                        fg_color="#2b2b2b", 
                        border_width=1, 
                        border_color="#1e1e1e", 
                        corner_radius=0, 
                        hover_color="#242424", 
                        cursor="hand2", 
                        command=create_new_project 
)
newProjectbtn.place(x=15, y=365 )

#Labels
username_text = customtkinter.CTkLabel( #Label que recebe o username do usuario
                        master=perfil_frame, 
                        text=username, 
                        text_color="white", 
                        font=font_username
)
username_text.place(x=60, y=10)

userwin.mainloop()