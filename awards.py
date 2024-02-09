

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

def t_BEGINTABLE(t):

    '''<h2><span\ class="mw-headline"\ id="Awards">Awards</span></h2>'''

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
    '''[A-Za-z0-9,\ć\é\í\á ]+'''
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

award1=[]
award2=[]
award3=[]
#########################################################################################
#Fill with parsing rules
def p_start(p):
    '''start : table'''
    
    p[0]=p[1]
    print('start..........')
def p_name(p):
    '''name : CONTENT
            | CONTENT name'''
    if len(p)==3:
        p[0]=p[1] + ' ' + p[2]
    else:
        p[0]=p[1]
def p_skiptag(p):
    '''skiptag : content skiptag
                | OPENHREF skiptag
                | CLOSEHREF skiptag
                | '''
def p_handleData(p):
    '''handleData : OPENDATA OPENHREF CLOSEHREF content OPENHREF  CONTENT CLOSEHREF CLOSEDATA          OPENDATA OPENHREF CLOSEHREF content OPENHREF  CONTENT CLOSEHREF CLOSEDATA    OPENDATA OPENHREF CLOSEHREF content OPENHREF CONTENT CLOSEHREF CLOSEDATA  
                    | OPENDATA CONTENT CONTENT CLOSEDATA handleData 
                    | OPENDATA OPENHREF CLOSEHREF content OPENHREF CONTENT  CLOSEHREF CLOSEDATA
                    | OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA
                    | '''
   # print('p_handledata')
    if len(p)==25:
        award2.append(p[6])
        award2.append(p[14])
        award2.append(p[22])
        #print(len(award1))
    if len(p)==7:
        award2.append(p[4])
    if len(p)==9:
        award2.append(p[6])
def p_handle_row(p):
    '''handleRow : contentprint handleRow
                    | OPENROW  handleData CLOSEROW handleRow
                    | empty'''
    #print(len(p))
    #print(len(p))
    if len(p)==9:
        print('h2')
        print(p[4])
    if len(p)==5:
        print('3')
def p_print(p):
    '''contentprint : OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT CLOSEHEADER OPENHEADER  CONTENT CLOSEHEADER CLOSEROW
                    |  OPENROW OPENHEADER OPENHREF CONTENT  CLOSEHREF CLOSEHEADER CLOSEROW'''
    #print(p[4]+' '+p[8] +' '+p[11])
    if len(p)==14:
        award1.append(p[4])
        award1.append(p[8])
        award1.append(p[11])
    #print(len(award1))
    if len(p)==8:
        award1.append(p[4])

def p_table(p):
    '''table : BEGINTABLE skiptag OPENTABLE handleRow'''
    if len(p)==5:
        print('p_table')
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
   # print(award1)
   # print(award2)
    for i in range(0,len(award2)):
        print(award1[i]+' is given to '+award2[i])
   # while True:
    #    tok = lexer.token()
     #   if not tok: 
      #      break      # No more input
       # print(tok)

    #########Fill the blank here for parser and lexer
    file_obj.close()

###############################################################################

if __name__ == '__main__':
    main()