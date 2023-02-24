# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

template = "{:<8} {:<14} {:>10}"
lines = []

vlan = input('Enter vlan: ')
vlan = int(vlan)

with open('CAM_table.txt') as f:
    for line in f:
        line = line.split()
        if len(line) != 0 and line[0].isdigit():
            line[0] = int(line[0])
            lines.append(line)
for line in lines:
    if vlan == line[0]:
        print(template.format(line[0], line[1], line[3]))