from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime, timedelta
from decimal import Decimal

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            return True
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self._saques_hoje = 0
        self._data_ultimo_saque = None

    def sacar(self, valor):
        if self._data_ultimo_saque != datetime.today().date():
            self._saques_hoje = 0

        if self._saques_hoje >= self.limite_saques:
            raise Exception("Limite de saques diários atingido")

        if valor > self.limite:
            raise Exception("Valor do saque excede o limite")

        if super().sacar(valor):
            self._saques_hoje += 1
            self._data_ultimo_saque = datetime.today().date()
            return True

        return False

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

def main():
    cliente = PessoaFisica("João", "01-01-1990", "12345678900", "Rua A, 123")
    conta = ContaCorrente("0001", cliente)
    cliente.adicionar_conta(conta)

    for _ in range(10):
        try:
            cliente.realizar_transacao(conta, Saque(50))
        except Exception as e:
            print(f"Erro ao realizar saque: {str(e)}")

    try:
        cliente.realizar_transacao(conta, Saque(50))
    except Exception as e:
        print(f"Erro ao realizar saque: {str(e)}")

    print(f"Saldo final: {conta.saldo}")

if __name__ == "__main__":
    main()
