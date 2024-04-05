def principal():
    print('Executando a principal: ')
    
    def func_1():
        print("Executando a função interna 1")
    
    def func_2():
        print("Executando a função interna 2")
        
    func_1()
    func_2()

principal()