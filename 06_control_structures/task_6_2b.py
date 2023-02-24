# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
ip = input('Enter ip: ')
# for symbol in ip:
#    if not (symbol.isdigit() or symbol == '.'):
octets = ip.split('.')
flag = True

if len(octets) == 4:
   for octet in octets:
      if not (octet.isdigit() and int(octet) >= 0 and int(octet) <= 255):
         flag = False
         break
else: 
   flag = False

if not(flag):
    print('неправильный ip-адрес')

while not(flag):
    ip = input('')
    octets = ip.split('.')
    if len(octets) == 4:
        for octet in octets:
            if octet.isdigit() and int(octet) >= 0 and int(octet) <= 255:
                flag = True
    else: 
        flag = False

f_ip = int(octets[0])
if f_ip <= 223 and f_ip > 0:
    print('unicast')
elif f_ip <= 239 and f_ip >= 224:
    print('multicast')
elif ip == '255.255.255.255':
    print('local broadcast')
elif ip == '0.0.0.0':
    print('unassigned')
else:
    print('unused')