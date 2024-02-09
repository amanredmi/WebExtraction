import os
#pip3 install ply
import ply.lex as lex
import ply.yacc as yacc
import team_link as tl
from urllib.request import Request , urlopen

def download(squad):

    req= Request(tl.team_link[squad],headers={'User-Agent':'Mozilla/5.0'})
    webpage=urlopen(req).read()
    mydata=webpage.decode("utf8")
    filename=squad+'_data.html'
    f=open(filename,'w',encoding="utf-8")
    f.write(mydata)
    f.close
    #print('done')






###DEFINING TOKENS###
players=[]
tokens = ('BEGINTABLE', 
'OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF',
'CONTENT', 'OPENDATA', 'CLOSEDATA' ,'OPENSPAN',
'CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 'OPENSTYLE', 'CLOSESTYLE','HR','GARBAGE')
t_ignore = '\t'


###############Tokenizer Rules################

def t_BEGINTABLE(t):

    '''<span\ class="mw-headline"\ id="Current_squad">Current\ squad</span>'''
    return t


def t_OPENTABLE(t):
    '''<tbody[^>]*>'''
    return t

def t_HR(t):
    '''<hr\ />'''
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
    '''[A-Za-z0-9,\[\u00C0-\u017F\]\-\&\#\.]+'''
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
    '''<[^>]*>'''

def t_error(t):
    t.lexer.skip(1)


#########################################################################################
#Fill with parsing rules
def p_start(p):
    '''start : table'''
    p[0]=p[1]
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
                | OPENSPAN skiptag 
                | CLOSESPAN skiptag
                | HR skiptag
                | empty '''
# *pos7 *name12 *DOB21 *GOALS28 *CLUB35
def p_handleData(p):
    '''handleData : OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENHEADER OPENHREF name CLOSEHREF CLOSEHEADER OPENDATA name CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA OPENHREF CLOSEHREF content OPENHREF name CLOSEHREF skiptag CLOSEDATA
                    | OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENHEADER OPENHREF name CLOSEHREF CLOSEHEADER OPENDATA name CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA OPENHREF CLOSEHREF content OPENHREF name CLOSEHREF skiptag CLOSEDATA
                    | '''
    if len(p)==33:
        players.append([p[12],p[16],p[7],p[29],p[22]])
    if len(p)==30:
        players.append([p[9],p[13],p[4],p[26],p[19]])   

def p_handle_row(p):
    '''handleRow : OPENROW OPENHEADER skiptag CLOSEHEADER OPENHEADER skiptag CLOSEHEADER OPENHEADER skiptag CLOSEHEADER   OPENHEADER skiptag CLOSEHEADER OPENHEADER skiptag CLOSEHEADER OPENHEADER skiptag CLOSEHEADER OPENHEADER skiptag CLOSEHEADER  CLOSEROW handleRow
                    | OPENROW handleData CLOSEROW handleRow
                    | OPENROW OPENDATA CLOSEDATA CLOSEROW handleRow
                    | '''
   # print('handlerow')
def p_skip(p):
    '''skip : OPENDATA skiptag CLOSEDATA skip
            | '''
def p_table(p):
    '''table : BEGINTABLE skiptag OPENTABLE handleRow CLOSETABLE'''
   # print(p[4])

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
    tl.main()
    
    squad=input('enter team name')

    download(squad)
    filename=squad+'_data.html'
    file_obj= open(filename,'r',encoding="utf-8")
    data=file_obj.read()
    lexer = lex.lex()
    #lexer.input(data)
    parser = yacc.yacc()
    
    #print(len(team))

    #while True:
     #   tok = lexer.token()
      #  if not tok: 
       #     break      # No more input
        #print(tok)
    result = parser.parse(data)
    print('squad of '+ squad + ' is :')
    #print(len(players))
    for i in range(0,len(players)):
        print(i+1,players[i][0])
    while(1):
        id=input('enter id of player for extracting his information')
        if id=='quit':
            break
        id=int(id)
        for j in range(len(players[id-1])):
            print(players[id-1][j])
    #for i in range(0,len(team)):
     #   print(team[i])
    #########Fill the blank here for parser and lexer
    file_obj.close()

###############################################################################

if __name__ == '__main__':
    main()
