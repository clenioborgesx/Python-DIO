def calculadora(op):
    def soma(a,b):
        return a + b
    def subtracao(a,b):
        return a - b
    def multiplicacao(a,b):
        return a * b
    def divisao(a,b):
        return a / b
    
    match op:
        case "+":
            return soma
        case "-":
            return subtracao
        case "*":
            return multiplicacao
        case "/":
            return divisao
        
print(calculadora("+")(2,2))
print(calculadora("-")(2,2))
print(calculadora("*")(2,2))
print(calculadora("/")(2,2))