from threading import Thread
from random import randint
from time import sleep
import queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:
    def __init__(self, *args):
        self.q = queue.Queue()
        self.tables = args
        self.cafe = {}

    def guest_arrival(self, *guests):
        for guest in guests:
            for table in self.tables:
                if table is self.tables[-1] and table.guest is not None:
                    self.q.put(guest)
                    print(f'{guest.name} в очереди')
                elif table.guest is None:
                    table.guest = guest
                    table.guest.start()
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    break

    def discuss_guests(self):
        while True:
            guest_stop = True
            for table in self.tables:
                if table.guest is not None:
                    guest_stop = False

            if guest_stop and self.q.empty():
                print('Все гости обслужены!')
                return

            for table in self.tables:
                if table.guest is not None:
                    if not table.guest.is_alive():
                        print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                        table.guest = None
                        print(f'Стол номер {table.number} свободен')
                        if not self.q.empty():
                            new_guest = self.q.get()
                            table.guest = new_guest
                            table.guest.start()
                            print(f'{new_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')

# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()


