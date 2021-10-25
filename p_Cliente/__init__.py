import p_conexaoDB
import p_abreMenu

def CadastrarCliente():

    try:
        cliente = {}
        cliente["nome"] = input("Digite o nome do Cliente: ")
        cliente["cpf"] = int(input("Digite o Cpf do Cliente (apenas números): "))
        cliente["email"] = input("Digite o email do Cliente: ")

        p_conexaoDB.cursor.execute("insert into cliente (nome, cpf, email) "
                       "values (%s, LPAD(%s,11,'0'), %s)", (cliente["nome"], cliente["cpf"],
                                                   cliente["email"]))
        p_conexaoDB.conn.commit()
        print("Cliente cadastrado com sucesso...")
    except:
        print("Infelizmente tivemos um erro no cadastro do cliente. Tente novamente mais tarde...")

def VisualizarCliente():

    listaClientes = []

    try:
        p_conexaoDB.cursor.execute("select idCliente, nome, cpf, email from Cliente")
        print("======================================")
        print("id do Cliente, Nome, CPF, E-mail      ")
        print("======================================")

        for cliente in p_conexaoDB.cursor.fetchall():
            listaClientes.append(cliente)

        for cliente in listaClientes:
            print(f"{cliente[0]}, {cliente[1]}, {cliente[2]}, {cliente[3]}")
    except:
        print("Infelizmente tivemos problemas ao selecionar Clientes. Tente novamente mais tarde...")

def ExcluirCliente():
    try:
        nomeBD = ''
        clienteEntrada = {}
        listaCliente =[]
        idCliente = 0
        valido = False

        clienteEntrada["nome"] = input("Digite o nome do Cliente: ")
        nomeBD = "%" + clienteEntrada["nome"] + "%"

        p_conexaoDB.cursor.execute("SELECT idCliente, nome, cpf, email FROM cliente where nome like %s ", (nomeBD,))

        if p_conexaoDB.cursor.rowcount == 0:
            print("==========================================")
            print(f"Não há cliente cadastrado para o nome: {clienteEntrada['nome']} ")
            print("==========================================")
        else:
            for cliente in p_conexaoDB.cursor.fetchall():
                listaCliente.append(cliente)

            print("=================================")
            print("Id do Cliente, Nome, CPF, E-mail")
            print("=================================")

            for cliente in listaCliente:
                print(f"{cliente[0]}, {cliente[1]}, {cliente[2]}, {cliente[3]}")

            print("=================================")
            idCliente = int(input("Digite o Id do cliente que queira excluir: "))
            print("=================================")

            for cliente in listaCliente:
                if cliente[0] == idCliente:
                    valido = True
                else:
                    valido = False

            if valido:
                p_conexaoDB.cursor.execute(f"DELETE FROM cliente WHERE idCliente = {idCliente}")

                if p_conexaoDB.cursor.rowcount == 0:
                    print("Cliente não encontrado")
                else:
                    print(f"Cliente {idCliente} excluído com sucesso")
                    p_conexaoDB.conn.commit()
            else:
                print("==============================================")
                print("ID digitado não é referente ao nome pesquisado")
                print("Verifique as informações e tente novamente")
                print("==============================================")
    except ValueError:
        print("==========================================")
        print("Verifique as informações e tente novamente")
        print("==========================================")

def f_menuCliente():

    opcao = 0

    print("===============================")
    print("= Escolha uma opção:")
    print("===============================")
    print("= 1 - Nova Inclusão: ")
    print("= 2 - Nova Exclusão: ")
    print("= 3 - Consultar clientes: ")
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
                CadastrarCliente()
            elif opcao == 2:
                ExcluirCliente()
            elif opcao == 3:
                VisualizarCliente()
            else:
                p_abreMenu.fMenu()
