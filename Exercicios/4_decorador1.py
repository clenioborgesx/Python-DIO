def decorador(func):
    def envelope():
        print("Faz antes")
        func()
        print("Faz depois")
        
    return envelope

@decorador
def ola_mundo():
    print("Olá Mundo!")
    
#ola_mundo = decorador(ola_mundo)
ola_mundo()