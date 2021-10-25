"""
Função para aparecer o menu da pousada
Pedro Lopes - 17/10
"""

import p_Cliente
import p_Quarto
import p_Reserva

def fMenu():
    opcaoMenu = 0
    qtdErro = 0
    opcaoContinue = ''
    opcaoValida = False

    print("======================================")
    print("=          Menu Pousada              =")
    print("======================================")
    print("= 1 - Quartos                        =")
    print("= 2 - Clientes                       =")
    print("= 3 - Reserva (nova/checkin/out)     =")
    print("= 4 - Encerrar                       =")
    print("======================================")

    # tratamento da entrada
    while qtdErro < 3:
        try:
            opcaoMenu = int(input("Escolha uma opcao:"))
        except ValueError:
            print("Escolha uma opção Valida")
            qtdErro = qtdErro + 1
        else:
            if opcaoMenu < 1 or opcaoMenu > 4:
                print("Escolha uma opção Valida")
                qtdErro = qtdErro + 1
            else:
                opcaoValida=True
                qtdErro = 3


    if not opcaoValida:
        print("============================================================")
        print("= Esgotada quantidade de erros, tente novamente mais tarde =")
        print("============================================================")
        print("\n")

    # chamada da função correspondente
    if opcaoMenu == 1:
        p_Quarto.f_menuQuarto()
    elif opcaoMenu == 2:
        p_Cliente.f_menuCliente()
    elif opcaoMenu == 3:
        p_Reserva.f_MenuReserva()

    if opcaoMenu != 4:
        print("=====================================")
        opcaoContinue = input("= Deseja mais alguma coisa?(S,N):    ")

        if opcaoContinue == 'S' or opcaoContinue == 's':
            fMenu()

