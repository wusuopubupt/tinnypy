#!/usr/bin/env python
#encoding=utf-8
import os
import sys

all_words_file="all_words_file.txt"
black_words_file="black_words_file.txt"


def clean_word(all_words, black_words):
    for word in all_words:
        in_black = False
        for black in black_words:
            #  check if a substring in a string
            if black in word:
                in_black = True

        if not in_black:
            print word

def main():
    # all words dict
    all_words = []
    f_all = open(all_words_file, "r")
    f_all_lines = f_all.readlines()
    for line in f_all_lines:
        line = line.strip()
        if not line:
            continue
        all_words.append(line)
    f_all.close()

    # black words dict
    black_words = []
    f_black = open(black_words_file, "r")
    f_black_lines = f_black.readlines()
    for line in f_black_lines:
        line = line.strip()
        if not line:
            continue
        black_words.append(line)
    f_black.close()

    clean_word(all_words, black_words)

if __name__ == '__main__':
    main()
