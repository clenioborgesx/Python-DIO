import textwrap
import string

class Conta_Banco:
    def __init__(self, digito_verificador, usuario):
        self.saldo = 0
        self.extrato = "Não foram realizadas movimentações.\n"
        self.limite = 500
        self.numero_saques = 0
        self.limite_saques = 5
        self.digito_verificador = digito_verificador
        self.usuario = usuario

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("Depósito realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.limite_saques

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            self.numero_saques += 1
            print("Saque realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")

    def exibir_extrato(self):
        print("\nEXTRATO")
        print(self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")

class Sistema_Banco:
    def __init__(self):
        self.contas = []
        self.numero_conta = 1000

    def efetuar_cadastro(self):
        cpf = input("Informe o CPF (somente número): ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            print("Já existe usuário com esse CPF!")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        endereco = input("Informe o endereço (Logradouro, Número - Bairro - Cidade/Sigla estado): ")
        digito_verificador = string.ascii_uppercase.index(nome[0].upper()) + 1
        usuario = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco,
            "agencia": "0226",
            "numero_conta": self.numero_conta
        }
        conta_bancaria = Conta_Banco(digito_verificador, usuario)
        self.contas.append({"agencia": "0226", "numero_conta": self.numero_conta, "digito_verificador": digito_verificador, "usuario": usuario, "conta": conta_bancaria})
        self.numero_conta += 1
        print("Usuário criado com sucesso!")

    def filtrar_usuario(self, cpf):
        usuarios_filtrados = [usuario for usuario in self.contas if usuario["usuario"]["cpf"] == cpf]
        return usuarios_filtrados[0] if usuarios_filtrados else None

    def acessar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            print(f"Bem-vindo, {usuario['usuario']['nome']}!")
            return usuario['conta']

        print("Usuário não encontrado.")
        return None

    def listar_contas(self):
        if not self.contas:
            print("\nNenhuma conta cadastrada!")
            return

        for conta in self.contas:
            linha = f"""\
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}-{conta['digito_verificador']}
                Titular:\t{conta['usuario']['nome']}
            """
            print(textwrap.dedent(linha))
            
    def transferir(self, conta_origem):
        numero_conta_destino = int(input("Digite o número da conta para a qual deseja transferir: "))
        valor = float(input("Digite o valor que deseja transferir: "))
        
        for conta in self.contas:
            if conta['numero_conta'] == numero_conta_destino:
                print(f"Você está transferindo para {conta['usuario']['nome']}")
                confirmacao = int(input("Digite 1 para confirmar a transferência, 2 para cancelar: "))
                if confirmacao == 1:
                    if conta_origem.saldo >= valor:
                        conta_origem.saldo -= valor
                        conta['conta'].saldo += valor
                        conta_origem.extrato += f"Transferência para {conta['usuario']['nome']}:\tR$ {valor:.2f}\n"
                        conta['conta'].extrato += f"Transferência de {conta_origem.usuario['nome']}:\tR$ {valor:.2f}\n"
                        print("Transferência realizada com sucesso!")
                    else:
                        print("Saldo insuficiente para realizar a transferência.")
                elif confirmacao == 2:
                    print("Transferência cancelada.")
                else:
                    print("Opção inválida.")
                return
        print("Conta destino não encontrada.")

def menu_principal():
    sistema = Sistema_Banco()

    while True:
        print("\n1 - Acessar Conta")
        print("2 - Efetuar Cadastro")
        print("3 - Listar Contas")
        print("4 - Sair")
        opcao = int(input("Escolha uma opção: "))
        if opcao == 1:
            conta = sistema.acessar_conta()
            if conta is not None:
                menu_conta(conta, sistema)
        elif opcao == 2:
            sistema.efetuar_cadastro()
        elif opcao == 3:
            sistema.listar_contas()
        elif opcao == 4:
            print("Até Logo!")
            break
        else:
            print("Opção inválida!")

def menu_conta(conta, sistema):
    while True:
        print("\n1 - Depósito")
        print("2 - Saque")
        print("3 - Extrato")
        print("4 - Transferência")
        print("5 - Sair")
        opcao = int(input("Escolha uma opção: "))
        if opcao == 1:
            valor = float(input("Digite o valor do depósito: "))
            conta.depositar(valor)
        elif opcao == 2:
            valor = float(input("Digite o valor do saque: "))
            conta.sacar(valor)
        elif opcao == 3:
            conta.exibir_extrato()
        elif opcao == 4:
            sistema.transferir(conta)
        elif opcao == 5:
            print("Saindo da conta...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()