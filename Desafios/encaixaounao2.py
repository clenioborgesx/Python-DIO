def verifica_encaixe(A, B):
    return A.endswith(B)

N = int(input("Digite a quantidade de casos de teste: "))
for i in range(N):
    A = input("Digite um número grande para A: ")
    B = input("Digite um número para B: ")
    if verifica_encaixe(A, B):
        print("encaixa")
    else:
        print("nao encaixa")