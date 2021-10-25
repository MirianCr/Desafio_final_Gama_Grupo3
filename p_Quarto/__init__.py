import p_conexaoDB
import p_abreMenu

def CadastrarQuarto():

    numero = ''
    numeroDB = 0

    try:
        Quarto = {}
        Quarto["numero"] = int(input("Digite o Número do Quarto: "))

        Quarto["andar"] = int(input("Digite o Andar do Quarto (apenas números): "))
        Quarto["qtdHospede"] = int(input("Digite a Quantidade de Hospedes do Quarto: "))
        numero = str(Quarto["andar"]) + str(Quarto["numero"])
        numeroDB = int(numero)

        p_conexaoDB.cursor.execute("insert into Quarto (numero, andar, qtdHospede, ocupado)"
                       "values (%s, %s, %s, 'N')", (numeroDB, Quarto["andar"],
                                               Quarto["qtdHospede"]))
        p_conexaoDB.conn.commit()
        print("Quarto cadastrado com sucesso...")
    except:
        print("Infelizmente tivemos um erro no cadastro do quarto. Tente novamente mais tarde...")

def VisualizarQuarto():
    listaQuartos = []

    try:
        p_conexaoDB.cursor.execute("SELECT idQuarto, ocupado, andar, qtdHospede, numero "
                                   "FROM dbpousada.quarto")

        print("==================================================")
        print("id do Quarto, Ocupado?, Andar, Capacidade, Número ")
        print("==================================================")

        for quarto in p_conexaoDB.cursor.fetchall():
            listaQuartos.append(quarto)

        for quarto in listaQuartos:
            print(f"{quarto[0]}, {quarto[1]}, {quarto[2]}, {quarto[3]}, {quarto[4]}")
    except:
        print("Infelizmente tivemos problemas ao selecionar Quartos. Tente novamente mais tarde...")

def ExcluirQuarto():
    try:
        idQuarto = 0
        idQuarto = int(input("Digite o id do quarto: "))
        p_conexaoDB.cursor.execute("DELETE FROM quarto "
                                   "WHERE idQuarto = %s "
                                   " and ocupado = 'N' ", (idQuarto,))
        if p_conexaoDB.cursor.rowcount == 0:
            print("============================================")
            print(f"= Não foi possível a exclusão do quarto {idQuarto}")
            print("============================================")
        else:
            print("============================================")
            print(f"= O quarto de id {idQuarto} foi excluído com sucesso")
            print("============================================")
            p_conexaoDB.conn.commit()
    except ValueError:
        print("============================================")
        print("= Verifique as informações e tente novamente")
        print("============================================")

def f_menuQuarto():

    opcao = 0

    print("===============================")
    print("= Escolha uma opção:")
    print("===============================")
    print("= 1 - Nova Inclusão: ")
    print("= 2 - Nova Exclusão: ")
    print("= 3 - Consultar quartos: ")
    print("= 4 - Voltar ao menu principal:")
    print("===============================")

    try:
        opcao=(int(input("Digite a opcao desejada: ")))
    except:
        print("============================================")
        print("= Verifique as informações e tente novamente")
        print("============================================")
    else:
        if opcao < 1 or opcao > 4:
            print("============================================")
            print("= Verifique as informações e tente novamente")
            print("============================================")
        else:
            if opcao == 1:
                CadastrarQuarto()
            elif opcao == 2:
                ExcluirQuarto()
            elif opcao == 3:
                VisualizarQuarto()
            else:
                p_abreMenu.fMenu()
