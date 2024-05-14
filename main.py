import customtkinter as ctk
from ver_corridas import visualizar_corridas

app = ctk.CTk()
app.geometry("600x500")
app.title("LinePID Monitor")

home_frame = ctk.CTkFrame(app)
races_frame = ctk.CTkFrame(app)

label = ctk.CTkLabel(home_frame, text="LinePID Monitor", fg_color="transparent", font=('', 40))
label.pack()

texto_gravar_corrida = ctk.CTkLabel(home_frame, text="Gravar corrida", fg_color="transparent", font=('', 20))
texto_gravar_corrida.pack(side="left", pady=15)

botao_gravar = ctk.CTkButton(home_frame, text="CTkButton")
botao_gravar.pack(side="left", pady=15)

texto_ver_corridas = ctk.CTkLabel(home_frame, text="Ver corridas", fg_color="transparent", font=('', 20))
texto_ver_corridas.pack(side="left", pady=15)

botao_ver = ctk.CTkButton(home_frame, text="CTkButton", command=visualizar_corridas)
botao_ver.pack(side="left", pady=15)

def show_home():
    home_frame.pack()

def show_races():
    visualizar_corridas()

show_home()

app.mainloop()
