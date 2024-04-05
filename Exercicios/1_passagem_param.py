def mensagem(nome):
    print("Executando mensagem: ")
    return f'Oi {nome}'
def mensagem_maior(nome):
    print("Executando mensagem maior: ")
    return f'Olá {nome} tudo bem com você?'
def executar(funcao, nome):
    print("Executando: ")
    return funcao(nome)

print(executar(mensagem, "Clenio"))
print(executar(mensagem_maior, "Clenio"))