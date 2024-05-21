from gravador import gravar_corrida
from ver_corridas import visualizar_corridas
from algoritmo_genetico import algoritmo_genetico

def menu():
    while True:
        print("\nMenu:")
        print("1. Iniciar uma nova corrida.")
        print("2. Visualizar dados de corridas anteriores.")
        print("3. Algoritmo genetico.")
        print("4. Sair.")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            gravar_corrida()
        elif escolha == "2":
            visualizar_corridas()
        elif escolha == "3":
            algoritmo_genetico()
        elif escolha == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

if __name__ == "__main__":
    menu()