def verifica_digitos(N):
    resultados = []
    while N > 0:
        A = input("Digite um número grande A: ")
        B = input("Digite um número B: ")

        if A.endswith(B):
            resultados.append("encaixa")
        else:
            resultados.append("nao encaixa")

        N -= 1
    
    return resultados

N = int(input("Digite a quantidade de casos de teste: "))
print(verifica_digitos(N))