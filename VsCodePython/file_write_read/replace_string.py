#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# replace strings in text

import os


def Replace(file_name, rep_word, new_word):
    with open(file_name) as f:
        content = []
        count = 0

        for eachline in f:
            if rep_word in eachline:
                count += eachline.count(rep_word)
                eachline = eachline.replace(rep_word, new_word)
            content.append(eachline)

        decide = input('The File [{0}] contains [{2}] {1} times\nAre you sure about replacing all [{3}] with [{4}]?\n[YES/NO]：'.format\
                (file_name, count, rep_word, rep_word, new_word))

        if decide in ['YES', 'Yes', 'yes']:
            with open(file_name, 'w') as f:
                f.writelines(content)
            print('Succeed!')
        else:
            print('Exit!')


if __name__ == '__main__':
    while True:

        file_name = input('Please enter file name: ').strip()

        if os.path.exists(file_name):   # 判断文件是否存在
            rep_word = input('Please enter the word or character to be replaced: ')
            new_word = input('Please enter a new word or character: ')
            Replace(file_name, rep_word, new_word)
            break
        else:
            print('Do not find such a file {}'.format(file_name))

'''
examples:

>>>Please input file name: H:/file_test1.txt
>>>Please enter the word or character to be replaced: GPGGA
>>>Please enter a new word or character: QXWZ
The File [H:/file_test1.txt] contains [GPGGA] 6 times
>>>Are you sure about replacing all [GPGGA] with [QXWZ]?
[YES/NO]：yes
Succeed!

'''
