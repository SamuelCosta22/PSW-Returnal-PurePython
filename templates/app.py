import __init__
from views.view import SubscriptionService
from models.database import engine
from models.model import Subscription
from datetime import datetime
from decimal import Decimal

class UI:
    def __init__(self):
        self.subscription_service = SubscriptionService(engine)

    def start(self):
        while True:
            print('''
                [1] -> Adicionar assinatura
                [2] -> Remover assinatura
                [3] -> Valor total
                [4] -> Gastos últimos 12 meses
                [5] -> Pagar assinatura
                [6] -> Sair
            ''')
            
            choice = int(input("Escolha uma ação: "))

            if choice == 1:
                self.add_subscription()
            elif choice == 2:
                self.delete_subscription()
            elif choice == 3:
                self.total_value()
            elif choice == 4:
                self.subscription_service.gen_charts()
            elif choice == 5:
                self.pay_subscription()
            elif choice == 6:
                print("Goodbye!")
            else:
                print("Invalid choice")
                self.start()
    
    def add_subscription(self):
        empresa = input('Empresa: ')
        site = input('Site: ')
        data_assinatura = datetime.strptime(input('Data da assinatura (dd/mm/yyyy): '), '%d/%m/%Y')
        valor = Decimal(input('Valor: '))
        subscription = Subscription(empresa=empresa, site=site, data_assinatura=data_assinatura, valor=valor)
        self.subscription_service.create(subscription)

    def delete_subscription(self):
        subscriptions = self.subscription_service.list_all()
        print('Escolha qual assinatura deseja excluir')
        for i in subscriptions:
            print(f'[{i.id}] -> {i.empresa}')

        choice = int(input('Escolha uma assinatura: '))
        self.subscription_service.delete(choice)
        print('Assinatura excluída com sucesso!')
    
    def total_value(self):
        print('Seu valor total mensal de assinatura é de R$', self.subscription_service.total_value())

    def pay_subscription(self):
        subscriptions = self.subscription_service.list_all()
        print('Escolha qual assinatura deseja pagar')
        for i in subscriptions:
            print(f'[{i.id}] -> {i.empresa}')

        choice = input('Escolha uma assinatura: ')
        self.subscription_service.pay(choice)
        print('Assinatura paga com sucesso!')

UI().start()