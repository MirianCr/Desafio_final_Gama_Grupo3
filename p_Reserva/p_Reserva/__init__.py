import p_abreMenu
import p_conexaoDB
from datetime import datetime

def f_MenuReserva():

    opcao = 0

    print("===============================")
    print("= Escolha uma opção:")
    print("===============================")
    print("= 1 - Nova reserva: ")
    print("= 2 - Excluir reserva: ")
    print("= 3 - Checkin: ")
    print("= 4 - Checkout:")
    print("= 5 - Consulta:")
    print("= 6 - Voltar ao menu principal:")
    print("===============================")

    try:
        opcao=(int(input("Digite a opcao desejada: ")))
    except:
        print("============================================")
        print("= Verifique as informações e tente novamente")
        print("============================================")
    else:
        if opcao < 1 and opcao > 6:
            print("============================================")
            print("= Verifique as informações e tente novamente")
            print("============================================")
        else:
            if opcao == 1:
                f_criaReserva()
            elif opcao == 2:
                f_excluiReserva()
            elif opcao == 3:
                f_realizaCheckin()
            elif opcao == 4:
                f_realizaCheckout()
            elif opcao == 5:
                f_consultaReserva()
            else:
                p_abreMenu.fMenu()

def f_realizaCheckout():
    idCliente = 0
    reservaCli = []
    cliSelecionado = []
    cliSelForm = []
    confimado = ""
    idQuarto = 0
    idReserva = 0
    continua = ''

    print("======================================")
    try:
        idCliente=int(input("= Insira o código do cliente: "))
    except ValueError:
        print("=============================================================")
        print("= Entrada inválida, verifica as informações e tente novamente")
        print("=============================================================")
    else:
        p_conexaoDB.cursor.execute(
            "SELECT idReserva, reserva.idCliente, idQuarto, cliente.nome, cliente.cpf, cliente.email,"
            " dtEntrada, dtSaidaPrevista "
            "FROM dbpousada.reserva "
            "inner join dbpousada.cliente "
            "on cliente.idcliente = reserva.idcliente "
            "where reserva.idCliente = %s "
            " and reserva.dtEntrada > '00.00.0000' "
            " and reserva.dtSaidaRealizada is null "
            "order by dtEntrada desc", (idCliente,)
        )

        cliSelecionado = p_conexaoDB.cursor.fetchone()

        if p_conexaoDB.cursor.rowcount == 0:
            print("===================================================")
            print(f"= Não há reserva com o código do cliente {idCliente}")
        else:
            print("======================================")
            print("=       Dados da Reserva Ativa       =")
            print("======================================")
            print(f"= Código da Reserva: {cliSelecionado[0]}")
            print(f"= Código do Cliente: {cliSelecionado[1]}")
            print(f"= Código da Quarto:  {cliSelecionado[2]}")
            print(f"= Nome:              {cliSelecionado[3]}")
            print(f"= CPF:               {cliSelecionado[4]}")
            print(f"= E-mail:            {cliSelecionado[5]}")
            print(f"= Data da entrada:   {cliSelecionado[6]}")
            print("======================================")

            confimado = input("= Digite S[sim] para confirmar o checkout: ")
            idQuarto = int(cliSelecionado[2])

            if confimado == "S" or confimado == "s":
                p_conexaoDB.cursor.execute(
                    "UPDATE dbpousada.quarto "
                    "SET ocupado=%s "
                    "WHERE ocupado=%s and idQuarto=%s", ('N', 'S', idQuarto,)
                )
                if p_conexaoDB.cursor.rowcount > 0:
                    idReserva = int(cliSelecionado[0])
                    p_conexaoDB.cursor.execute(
                        "UPDATE dbpousada.reserva "
                        "SET dtSaidaRealizada=Now() "
                        "WHERE idReserva=%s;", (idReserva,)
                    )
                    if p_conexaoDB.cursor.rowcount > 0:
                        p_conexaoDB.conn.commit()
                        print("======================================")
                        print(f"= Checkout atualizado com sucesso! ")
                        print("======================================")
                    else:
                        print("===========================================")
                        print("= Por favor verifique a reserva do cliente")
                        print("= Checkout não realizado")
                        print("===========================================")
                else:
                    print("===========================================")
                    print("= Por favor verifique a reserva do cliente")
                    print("= Checkout não realizado")
                    print("===========================================")
            else:

                print("======================================")
                print(f"= Checkout cancelado ")
                print("======================================")

        continua = input("Voltar ao menu? (S,N) ")

        if continua == 'S' or continua =='s':
            p_abreMenu.fMenu()

def f_realizaCheckin():
    idCliente = 0
    idQuarto = 0
    diaSaida = ''
    listaReserva = []
    idReserva = 0
    idResVal = False
    dataAtual = ''
    dataIniReserva = ''
    dataFimReserva = ''

    try:
        idCliente = int(input("Digite o código do cliente: "))

        #verifique se a reserva existe e quais os dados do cliente
        p_conexaoDB.cursor.execute(
            "SELECT reserva.idReserva, reserva.idQuarto, cliente.nome, cliente.cpf,"
            " dtEntradaPrevista, dtSaidaPrevista "
            "FROM reserva "
            "inner join cliente "
            "on cliente.idcliente = reserva.idcliente "
            "where reserva.idCliente = %s "
            "and reserva.dtEntrada is Null", (idCliente,)
        )

        if p_conexaoDB.cursor.rowcount == 0:
            print("===========================================================")
            print(f"= Não há reserva para o cliente de id: {idCliente}")
            print("= Verifique as informações tente novamente")
            print("===========================================================")
        else:
            print("=============================================================================")
            print("Id Reserva, Id Quarto, Nome do Cliente, CPF, Entrada Prevista, Saída Prevista")
            print("=============================================================================")

            for reserva in p_conexaoDB.cursor.fetchall():
                listaReserva.append(reserva)

            for reserva in listaReserva:
                print(f"{reserva[0]}, {reserva[1]}, {reserva[2]}, {reserva[3]}, {reserva[4]}, {reserva[5]}")

            idReserva = int(input("Digite a reserva desejada: "))

            #verificar se o id da reserva está na lista
            for idRes in listaReserva:
                if idRes[0] == idReserva:
                    idResVal = True
                    idQuarto = idRes[1]
                    dataIniReserva = idRes[4]
                    dataFimReserva = idRes[5]

            # verificar se a data de entrada é igual ou mais antigo e a data de saída seja futura

            if idResVal:
                dataAtual = datetime.today().date()
                if dataIniReserva <= dataAtual <= dataFimReserva:
                    # atualiza situação do quarto
                    p_conexaoDB.cursor.execute(
                        "UPDATE quarto "
                        "SET ocupado=%s "
                        "WHERE ocupado=%s and idQuarto=%s", ('S', 'N', idQuarto,)
                    )

                    # verifique se atualizou 1 linha
                    if p_conexaoDB.cursor.rowcount == 0:
                        print("============================================")
                        print("= Não foi possível fazer checkin")
                        print("= Verifique as informações e tente novamente")
                        print("============================================")
                    else:
                        p_conexaoDB.cursor.execute("UPDATE reserva "
                                                   "SET dtEntrada= now()"
                                                   " WHERE idReserva=%s; ", (idReserva,))

                        if p_conexaoDB.cursor.rowcount == 0:
                            print("============================================")
                            print("= Não foi possível fazer checkin")
                            print("= Verifique as informações e tente novamente")
                            print("============================================")
                        else:
                            p_conexaoDB.conn.commit()
                            print(f" Checkin realizado com sucesso para a reserva {idReserva}")
                else:
                    print("Reserva não disponível para Checkin - Verificar data de entrada prevista")
            else:
                    print("Reserva não disponível para Checkin")

    except ValueError:
        print("============================================")
        print("= Verifique as informações e tente novamente")
        print("============================================")
    else:
        pass

def f_criaReserva():

    idCliente = 0
    idQuarto = 0
    idReserva = 0
    entradaPrevista = ''
    saidaPrevista = ''
    dataAtual = ''
    entradaDigitada = ''
    saidaDigitada = ''

    try:

        idCliente = int(input("Digite o código do cliente: (apenas números) "))

        p_conexaoDB.cursor.execute("SELECT idCliente "
                                   "FROM cliente "
                                   "WHERE idCliente = %s;", (idCliente,))

        if p_conexaoDB.cursor.rowcount == 0:
            print("cliente não encontrado")
        else:
            idQuarto = int(input("Digite o código do quarto: (apenas números) "))
            p_conexaoDB.cursor.execute("SELECT idQuarto "
                                       "FROM quarto "
                                       "WHERE idQuarto = %s "
                                       "  and ocupado = 'N';", (idQuarto,))

            # verifica se o quarto está desocupado
            if p_conexaoDB.cursor.rowcount == 0:
                print("quarto não disponível")
            else:
                p_conexaoDB.cursor.execute("SELECT idQuarto "
                                           "FROM reserva "
                                           "WHERE idQuarto = %s "
                                           "  and dtEntrada is Null;", (idQuarto,))

                # verifica se o quarto não está reservado
                if p_conexaoDB.cursor.rowcount == 0:

                    entradaDigitada = input("Digite a data prevista de entrada: (formato dia/mes/ano) ")
                    entradaPrevista = datetime.strptime(entradaDigitada, "%d/%m/%Y").date()
                    saidaDigitada = input("Digite a data prevista de saída: (formato dia/mes/ano) ")
                    saidaPrevista = datetime.strptime(saidaDigitada, "%d/%m/%Y").date()

                    dataAtual = datetime.today().date()

                    if entradaPrevista >= dataAtual:
                        if saidaPrevista >= entradaPrevista:

                            p_conexaoDB.cursor.execute("INSERT INTO reserva "
                                                       "(idCliente, idQuarto, dtEntradaPrevista, "
                                                       "dtSaidaPrevista ) "
                                                       "VALUES(%s, %s, %s, %s);",
                                                       (idCliente, idQuarto, entradaPrevista, saidaPrevista))
                            if p_conexaoDB.cursor.rowcount == 0:
                                print("Tivemos problemas ao criar a reserva")
                            else:
                                p_conexaoDB.conn.commit()
                                #verificar o id da reserva para aquele cliente
                                p_conexaoDB.cursor.execute("SELECT max(idReserva) "
                                                           "FROM reserva "
                                                           "WHERE idCliente = %s "
                                                           "  and dtEntrada is Null;", (idCliente,))

                                idReserva = p_conexaoDB.cursor.fetchone()

                                print(f"Reserva cadastrada com sucesso com o id: {idReserva[0]}")
                        else:
                            print("saída prevista inválida")
                    else:
                        print("data escolhida como entrada mais antiga que a atual")
                else:
                    print("quarto reservado")


    except ValueError:
        print("Favor verificar dados digitados:")
    else:
        pass

def f_excluiReserva():
    idReserva = 0
    resSelecionado = []
    confirmado = ''
    continua = ''

    print("======================================")
    try:
        idReserva = int(input("= Insira o código da reserva: "))
    except ValueError:
        print("=============================================================")
        print("= Entrada inválida, verifica as informações e tente novamente")
        print("=============================================================")
    else:
        p_conexaoDB.cursor.execute(
            "SELECT idReserva, reserva.idCliente, idQuarto, cliente.nome, cliente.cpf, cliente.email,"
            " dtEntrada, dtSaidaRealizada, dtEntradaPrevista, dtSaidaPrevista "
            "FROM dbpousada.reserva "
            "inner join dbpousada.cliente "
            "on cliente.idcliente = reserva.idcliente "
            "where idReserva = %s ", (idReserva,)
        )

        resSelecionado = p_conexaoDB.cursor.fetchone()

        if p_conexaoDB.cursor.rowcount == 0:
            print("===========================================================")
            print(f"= A reserva {idReserva} não está disponível para exclusão")
            print("= Verifique as informações da reserva e tente novamente")
            print("===========================================================")
        else:
            print("======================================")
            print("=       Dados da Reserva             =")
            print("======================================")
            print(f"= Código da Reserva: {resSelecionado[0]}")
            print(f"= Código do Cliente: {resSelecionado[1]}")
            print(f"= Código da Quarto:  {resSelecionado[2]}")
            print(f"= Nome:              {resSelecionado[3]}")
            print(f"= CPF:               {resSelecionado[4]}")
            print(f"= E-mail:            {resSelecionado[5]}")
            print(f"= Entrada realizada: {resSelecionado[6]}")
            print(f"= Saída realizada:   {resSelecionado[7]}")
            print(f"= Entrada prevista:  {resSelecionado[8]}")
            print(f"= Saída prevista:    {resSelecionado[9]}")
            print("======================================")

            confimado = input("= Digite S[sim] para confirmar a exclusao: ")

            if confirmado == 'S' or confimado == 's':
                p_conexaoDB.cursor.execute("DELETE FROM dbpousada.reserva"
                                           " WHERE dtEntrada is null "
                                           " and idReserva= %s; ", (idReserva,))

                if p_conexaoDB.cursor.rowcount > 0:
                    p_conexaoDB.conn.commit()
                    print("=============================================================")
                    print(f"= A reserva {idReserva} excluída com sucesso")
                    print("=============================================================")
                else:
                    print("=============================================================")
                    print(f"= Não foi possivel a exclusão da reserva {idReserva}")
                    print("= Verifique as informações e tente mais tarde")
                    print("=============================================================")
            else:
                print("=============================================================")
                print("= Exclusão cancelada")
                print("=============================================================")

        continua = input("Voltar ao menu? (S,N) ")

        if continua == 'S' or continua =='s':
            p_abreMenu.fMenu()

def f_consultaReserva():
    listaReserva=[]

    try:
        p_conexaoDB.cursor.execute("SELECT idReserva, idCliente, idQuarto, dtEntradaPrevista, dtSaidaPrevista, "
                                   " dtEntrada, dtSaidaRealizada FROM reserva;")
        print("=========================================================================================================")
        print("= Id Reserva, Id Cliente, Id Quarto, Entrada Prevista, Saída Prevista, Entrada Realizada, Saída Realizada")
        print("=========================================================================================================")
        for reserva in p_conexaoDB.cursor.fetchall():
            listaReserva.append(reserva)

        for reserva in listaReserva:
            print(f"{reserva[0]}, {reserva[1]}, {reserva[2]}, {reserva[3]}, {reserva[4]}, "
                  f"{reserva[5]}, {reserva[6]},")

        print(
            "=========================================================================================================")

    except:
        print("Infelizmente tivemos problemas ao selecionar as Reservas. Tente novamente mais tarde...")
