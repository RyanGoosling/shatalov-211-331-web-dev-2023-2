# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

from sys import argv

ignore = ["duplex", "alias", "configuration"]
file = argv[1]
dest = argv[2]

with open(file) as f, open(dest, 'w') as d:
    for line in f:
        if line[0] != '!':
            has_ignore_word = False
            for ignore_word in ignore:
                if ignore_word in line:
                    has_ignore_word = True
                    break
            if not has_ignore_word:
                d.write(line)