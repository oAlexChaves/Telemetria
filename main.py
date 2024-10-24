from gravador import gravar_corrida
from ver_corridas import visualizar_corridas
from algoritmo_genetico import algoritmo_genetico

def menu():
    print("teste")
    while True:
        try:
            print("Menu:")
            print("1. Iniciar uma nova corrida.")
            print("2. Visualizar dados de corridas anteriores.")
            print("3. Algoritmo genetico.")
            print("4. Sair.")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                print("teste 1")
            elif escolha == "2":
                print("teste 1")
            elif escolha == "3":
                print("teste 1")
            elif escolha == "4":
                print("Saindo...")
                break
            else:
                print("Opção inválida. Por favor, escolha novamente.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            print("Tente novamente ou verifique as configurações.")

menu()