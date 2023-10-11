import tkinter as tk

class Quadrado:
    def __init__(self, canvas, x, y, lado, cor):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.lado = lado
        self.cor = cor
        self.quadrado = None
        self.label = None  # Rótulo de texto para mostrar a posição
        self.criar_quadrado()

        self.canvas.tag_bind(self.quadrado, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.quadrado, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.quadrado, "<ButtonRelease-1>", self.on_release)

    def criar_quadrado(self):
        x1, y1 = self.x - self.lado / 2, self.y - self.lado / 2
        x2, y2 = self.x + self.lado / 2, self.y + self.lado / 2
        self.quadrado = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.cor, outline="black")
        self.atualizar_label_posicao()  # Atualiza o rótulo de posição

    def on_press(self, event):
        self.start_x_drag = event.x
        self.start_y_drag = event.y

    def on_drag(self, event):
        dx = event.x - self.start_x_drag
        dy = event.y - self.start_y_drag
        self.canvas.move(self.quadrado, dx, dy)
        self.start_x_drag = event.x
        self.start_y_drag = event.y
        self.atualizar_label_posicao()  # Atualiza o rótulo de posição durante o arraste

    def on_release(self, event):
        pass

    def atualizar_label_posicao(self):
        if self.label:
            self.canvas.delete(self.label)  # Remove o rótulo anterior
        pos_x = self.x
        pos_y = self.y - 20  # Posição acima do quadrado
        self.label = self.canvas.create_text(pos_x, pos_y, text=f"({pos_x}, {pos_y})", anchor="s")

class Aplicacao:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Criar e Mover Quadrados")
        
        self.canvas = tk.Canvas(janela, width=400, height=400, bg="white")
        self.canvas.pack()

        self.quadrados = []

        self.botao_criar_quadrado = tk.Button(janela, text="Criar Quadrado", command=self.criar_quadrado)
        self.botao_criar_quadrado.pack()

        self.botao_salvar_quadrados = tk.Button(janela, text="Salvar Quadrados", command=self.salvar_quadrados)
        self.botao_salvar_quadrados.pack()

    def criar_quadrado(self):
        x, y = 200, 200
        lado = 50
        cor = "blue"

        novo_quadrado = Quadrado(self.canvas, x, y, lado, cor)
        self.quadrados.append(novo_quadrado)

    def salvar_quadrados(self):
        if self.quadrados:
            print("Quadrados Salvos:")
            for idx, quadrado in enumerate(self.quadrados, start=1):
                print(f"Quadrado {idx}:")
                print(f"   Posição: ({quadrado.x}, {quadrado.y})")
                print(f"   Tamanho do Lado: {quadrado.lado}")
                print(f"   Cor: {quadrado.cor}")
        else:
            print("Nenhum quadrado foi criado ainda.")

janela = tk.Tk()
app = Aplicacao(janela)
janela.mainloop()
