from gravadormanual import gravar_corrida_manual
from ver_corridas import visualizar_corridas
from algoritmo_genetico import algoritmo_genetico

def menu():
    while True:
        print("\nMenu:")
        print("1. Iniciar uma nova corrida unica.")
        print("2. corridas automatizadas")
        print("3. Visualizar dados de corridas anteriores.")
        print("4. Algoritmo genetico.")
        print("5. Sair.")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            gravar_corrida_manual()
        elif escolha == "2":
            print("teste")
        elif escolha == "3":
            visualizar_corridas()
        elif escolha == "4":
            algoritmo_genetico()
        elif escolha == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

if __name__ == "__main__":
    menu()