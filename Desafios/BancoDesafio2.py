import json
import textwrap
import string

class ContaBancaria:
    def __init__(self, digito_verificador):
        self.saldo = 0
        self.extrato = "Não foram realizadas movimentações.\n"
        self.limite = 500
        self.numero_saques = 0
        self.limite_saques = 5
        self.digito_verificador = digito_verificador

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        conta = cls(data['digito_verificador'])
        conta.saldo = data['saldo']
        conta.extrato = data['extrato']
        conta.limite = data['limite']
        conta.numero_saques = data['numero_saques']
        conta.limite_saques = data['limite_saques']
        return conta

    def to_json(self):
        return json.dumps({
            'saldo': self.saldo,
            'extrato': self.extrato,
            'limite': self.limite,
            'numero_saques': self.numero_saques,
            'limite_saques': self.limite_saques,
            'digito_verificador': self.digito_verificador,
        })

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

class SistemaBancario:
    def __init__(self):
        self.contas = []
        self.usuarios = self.carregar_dados()
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
        conta_bancaria = ContaBancaria(digito_verificador)
        agencia = "0226"  
        usuario = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco,
            "conta_bancaria": conta_bancaria.to_json(),
            "agencia": agencia,
            "numero_conta": self.numero_conta
        }
        self.usuarios.append(usuario)
        self.contas.append({"agencia": agencia, "numero_conta": self.numero_conta, "digito_verificador": digito_verificador, "usuario": usuario, "conta": conta_bancaria})
        self.numero_conta += 1
        self.salvar_dados(self.usuarios)
        print("Usuário criado com sucesso!")

    def filtrar_usuario(self, cpf):
        """Retorna o primeiro usuário que corresponde ao CPF fornecido."""
        usuarios_filtrados = [usuario for usuario in self.usuarios if usuario["cpf"] == cpf]
        return usuarios_filtrados[0] if usuarios_filtrados else None

    def acessar_conta(self):
        """Permite ao usuário acessar sua conta."""
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            print(f"Bem-vindo, {usuario['nome']}!")
            return ContaBancaria.from_json(usuario['conta_bancaria'])

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

    def atualizar_usuario(self, conta):
        for usuario in self.usuarios:
            if json.loads(usuario['conta_bancaria'])['digito_verificador'] == conta.digito_verificador:
                usuario['conta_bancaria'] = conta.to_json()
                break

    def salvar_dados(self, usuarios, nome_arquivo='usuarios.txt'):
        try:
            with open(nome_arquivo, 'w') as arquivo:
                json.dump(usuarios, arquivo)
        except IOError:
            print("Erro ao salvar os dados dos usuários.")

    def carregar_dados(self, nome_arquivo='usuarios.txt'):
        try:
            with open(nome_arquivo, 'r') as arquivo:
                if arquivo.read().strip():  # Verifica se o arquivo não está vazio
                    arquivo.seek(0)  # Volta ao início do arquivo
                    usuarios = json.load(arquivo)
                    for usuario in usuarios:
                        usuario['conta_bancaria'] = ContaBancaria.from_json(usuario['conta_bancaria'])
                        self.contas.append({"agencia": usuario['agencia'], "numero_conta": usuario['numero_conta'], "digito_verificador": usuario['conta_bancaria'].digito_verificador, "usuario": usuario, "conta": usuario['conta_bancaria']})
                else:
                    usuarios = []
        except (FileNotFoundError, IOError):
            usuarios = []
        return usuarios

def menu_principal():
    sistema = SistemaBancario()

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
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

def menu_conta(conta, sistema):
    while True:
        print("\n1 - Depósito")
        print("2 - Saque")
        print("3 - Extrato")
        print("4 - Sair")
        opcao = int(input("Escolha uma opção: "))
        if opcao == 1:
            valor = float(input("Digite o valor do depósito: "))
            conta.depositar(valor)
            sistema.atualizar_usuario(conta)
            sistema.salvar_dados(sistema.usuarios)
        elif opcao == 2:
            valor = float(input("Digite o valor do saque: "))
            conta.sacar(valor=valor)
            sistema.atualizar_usuario(conta)
            sistema.salvar_dados(sistema.usuarios)
        elif opcao == 3:
            conta.exibir_extrato()
        elif opcao == 4:
            print("Saindo da conta...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()
