

import ply.lex as lex
import ply.yacc as yacc




###DEFINING TOKENS###

tokens = ('BEGINTABLE', 
'OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF',
'CONTENT', 'OPENDATA', 'CLOSEDATA' ,'OPENSPAN',
'CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 'OPENSTYLE', 'CLOSESTYLE','GARBAGE')
t_ignore = '\t'


###############Tokenizer Rules################
#teams=[]
stadiums=[]

def t_BEGINTABLE(t):

    '''<h3><span\sclass="mw-headline"\sid="Stadiums">Stadiums</span></h3>'''

    return t


def t_OPENTABLE(t):
    '''<tbody[^>]*>'''
    return t

def t_CLOSETABLE(t):
    '''</tbody[^>]*>'''
    return t

def t_OPENROW(t):
    '''<tr[^>]*>'''
    return t

def t_CLOSEROW(t):
    '''</tr[^>]*>'''
    return t

def t_OPENHEADER(t):
    '''<th[^>]*>'''
    return t

def t_CLOSEHEADER(t):
    '''</th[^>]*>'''
    return t

def t_OPENHREF(t):
    '''<a[^>]*>'''
    return t

def t_CLOSEHREF(t):
    '''</a[^>]*>'''
    return t

def t_OPENDATA(t):
    '''<td[^>]*>'''
    return t

def t_CLOSEDATA(t):
    '''</td[^>]*>'''
    return t

def t_CONTENT(t):
    '''[A-Za-z0-9, ]+'''
    return t

def t_OPENDIV(t):
    '''<div[^>]*>'''

def t_CLOSEDIV(t):
    '''</div[^>]*>'''

def t_OPENSTYLE(t):
    '''<style[^>]*>'''

def t_CLOSESTYLE(t):
    '''</style[^>]*>'''

def t_OPENSPAN(t):
    '''<span[^>]*>'''

def t_CLOSESPAN(t):
    '''</span[^>]*>'''

def t_GARBAGE(t):
    r'<[^>]*>'

def t_error(t):
    t.lexer.skip(1)


#########################################################################################
#Fill with parsing rules
def p_start(p):
    '''start : table'''
    p[0]=p[1]
   # print('start')
def p_name(p):
    '''name : CONTENT
            | CONTENT name'''
    if len(p)==3:
        p[0]=p[1] + ' ' + p[2]
    else:
        p[0]=p[1]
def p_skiptag(p):
    '''skiptag : CONTENT skiptag
                | OPENHREF skiptag
                | CLOSEHREF skiptag
                | '''
    #print('skiptag')
def p_handleData(p):
    '''handleData : OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA handleData
                    | OPENDATA skiptag CLOSEDATA handleData
                    | '''
    if len(p)==7:
        stadiums.append(p[3])
   # print('handledata')
def p_handle_row(p):
    '''handleRow : OPENROW OPENHEADER skiptag CLOSEHEADER OPENHEADER skiptag CLOSEHEADER OPENHEADER skiptag CLOSEHEADER CLOSEROW handleRow
                    | OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER handleData CLOSEROW handleRow
                    | OPENROW  handleData CLOSEROW handleRow
                    | '''
    #print('handlerow')
def p_table(p):
    '''table : BEGINTABLE skiptag OPENTABLE handleRow'''
    #print('p_table')
def p_empty(p):
    '''empty :'''
    pass
def p_content(p):
    '''content : CONTENT
               | empty'''
    p[0]=p[1]
def p_error(p):
    pass
#########################################################################################
#########DRIVER FUNCTION#######

def main():
    file_obj= open('Fifa_data.html','r',encoding="utf-8")
    data=file_obj.read()
    lexer = lex.lex()
    lexer.input(data)
    parser = yacc.yacc()
    result = parser.parse(data)
    for i in range(0,len(stadiums)):
        print(stadiums[i])
    #while True:
     #   tok = lexer.token()
      #  if not tok: 
       #     break      # No more input
        #print(tok)

    #########Fill the blank here for parser and lexer
    file_obj.close()

###############################################################################

if __name__ == '__main__':
    main()