#!/usr/bin/env python  
#coding:utf-8

# urlsafe_base64 加解密

import sys
import base64

reload(sys)
sys.setdefaultencoding('utf8')

def base64_url_encode(word):
    return base64.urlsafe_b64encode(str(word)).rstrip('=')

def base64_url_decode(word):
    return base64.urlsafe_b64decode(str(word + '=' * (4 - len(inp) % 4)))

def main():
    usage = "Usage: python inputfile"
    if(len(sys.argv) < 2):
        print usage
        return 
    inputfile = sys.argv[1]
    f = open(inputfile, 'r') 
    f_list = f.readlines()
    f.close() 
    for line in f_list:
        word = line.strip()                     
        if not len(word):
            continue                                   
        encoded_word = base64_url_encode(word)
        print "%s\t%s" % (word, encoded_word)

if __name__ == '__main__':
    main()

