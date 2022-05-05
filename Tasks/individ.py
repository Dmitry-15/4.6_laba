#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import sys
from typing import List
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class Human:
    name: str
    zodiac: str
    year: str


@dataclass
class People:
    people: List[Human] = field(default_factory=lambda: [])

    def add(self, name, zodiac, year):
        self.people.append(
            Human(
                name=name,
                zodiac=zodiac,
                year=year,
            )
        )
        self.people.sort(key=lambda human: human.name)

    def __str__(self) -> str:
        # Заголовок таблицы.
        table = []
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        table.append(line)
        table.append(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "No",
                "Ф.И.О.",
                "Группа",
                "Успеваемость"
            )
        )
        table.append(line)
        # Вывести данные о всех сотрудниках.
        for idx, human in enumerate(self.people, 1):
            table.append(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    human.name,
                    human.zodiac,
                    human.year
                )
            )
        table.append(line)
        return '\n'.join(table)

    def select(self, nom: str):
        count = 0
        result = []
        # Проверить сведения людей из списка.
        for i, num in enumerate(self.people, 1):
            if nom == num.name:
                count += 1
                result.append(human)
            return result

    def load(self, filename):
        with open(filename, "r", encoding="utf-8") as fin:
            xml = fin.read()

        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.fromstring(xml, parser=parser)

        self.people = []
        for human_element in tree:
            name, zodiac, year = None, None, None

            for element in human_element:
                if element.tag == 'name':
                    name = element.text
                elif element.tag == 'zodiac':
                    zodiac = element.text
                elif element.tag == 'year':
                    year = element.text

                if name is not None and zodiac is not None \
                        and year is not None:
                    self.people.append(
                        Human(
                            name=name,
                            zodiac=zodiac,
                            year=year
                        )
                    )

    def save(self, filename: str) -> None:
        root = ET.Element('people')
        for human in self.people:
            human_element = ET.Element('human')

            name_element = ET.SubElement(human_element, 'name')
            name_element.text = human.name

            post_element = ET.SubElement(human_element, 'zodiac')
            post_element.text = human.zodiac

            year_element = ET.SubElement(human_element, 'year')
            year_element.text = human.year

            root.append(human_element)

        tree = ET.ElementTree(root)
        with open(filename, "w", encoding="utf-8") as fout:
            tree.write(fout, encoding="utf-8", xml_declaration=True)


if __name__ == '__main__':
    schedule = People()
    while True:
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        elif command == 'add':
            # Запросить данные о человеке.
            name = input("ФИО: ")
            zodiac = input("Знак зодиака: ")
            year = input("Дата рождения: ")

            schedule.add(name, zodiac, year)

        elif command == 'list':
            # Вывести список людей.
            print(schedule)

        elif command.startswith('select '):
            parts = command.split(maxsplit=1)
            # Запросить работника по имени.
            selected = schedule.select()

            # Вывести результаты запроса.
            if selected:
                for idx, human in enumerate(selected, 1):
                    print(
                        '{:>4}: {}'.format(idx, human.name)
                        )

            else:
                print("Человек с данным именем не найден.")

        elif command.startswith('load '):
            # Разбить команду на части для имени файла.
            parts = command.split(maxsplit=1)
            # Загрузить данные из файла.
            schedule.load(parts[1])

        elif command.startswith('save '):
            # Разбить команду на части для имени файла.
            parts = command.split(maxsplit=1)
            # Сохранить данные в файл.
            schedule.save(parts[1])

        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить человека;")
            print("list - вывести список людей;")
            print("select <ФИО> - запросить человека с заданным именем;")
            print("load <имя_файла> - загрузить данные из файла;")
            print("save <имя_файла> - сохранить данные в файл;")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)
