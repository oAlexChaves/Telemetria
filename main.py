import customtkinter as ctk
from ver_corridas import visualizar_corridas

# Inicialização do aplicativo
app = ctk.CTk()
app.geometry("600x500")
app.title("LinePID Monitor")

# Criação do Tabview
tabview = ctk.CTkTabview(app)
tabview.pack(expand=True, fill="both")

# Adição das abas
home_tab = tabview.add("Home")
gravador_tab = tabview.add("gravador")
races_tab = tabview.add("Ver Corridas")

# Configuração da aba Home
label = ctk.CTkLabel(home_tab, text="LinePID Monitor", fg_color="transparent", font=('', 40))
label.pack(pady=10)

texto_gravar_corrida = ctk.CTkLabel(home_tab, text="Gravar corrida", fg_color="transparent", font=('', 20))
texto_gravar_corrida.pack(pady=15)

botao_gravar = ctk.CTkButton(home_tab, text="CTkButton")  # Adicione a função de gravação aqui
botao_gravar.pack(pady=15)

# Chama a função visualizar_corridas e passa a aba races_tab como parent
visualizar_corridas(races_tab)

# Início do aplicativo
app.mainloop()
