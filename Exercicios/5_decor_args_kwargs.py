def decorador(func):
    def envelope(*args, **kwargs):
        print("Faz antes")
        func(*args, **kwargs)
        print("Faz depois")
        
    return envelope

@decorador
def ola_mundo(nome):
    print(f"Olá Mundo de {nome}!")
    
#ola_mundo = decorador(ola_mundo)
ola_mundo("Clenio")