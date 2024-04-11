# Primeira função:

def exibir_mensagem():
    print("Olá mundo!")


def exibir_mensagem_2(nome):
    print(f"Seja bem vindo {nome}!")


def exibir_mensagem_3(nome="Anônimo"):
    print(f"Seja bem vindo {nome}!")

# exemplo retornando uma mensagem para usuário
def saudacao():
    nome = input("Por favor, insira seu nome: ")
    print(f"Oi, {nome}!")

# Para usar a função, basta chamar:
saudacao()
exibir_mensagem()
exibir_mensagem_2(nome="Guilherme")
exibir_mensagem_3()
exibir_mensagem_3(nome="Chappie")
