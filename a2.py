import os
#pip3 install ply
#import ply.lex as lex
#import ply.yacc as yacc
from urllib.request import Request , urlopen

req= Request('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup',headers={'User-Agent':'Mozilla/5.0'})
webpage=urlopen(req).read()
mydata=webpage.decode("utf8")
f=open('Fifa_data.html','w',encoding="utf-8")
f.write(mydata)
f.close
print('done')
