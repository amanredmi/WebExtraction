import ply.lex as lex
import ply.yacc as yacc

# Define the tokens
tokens = (
    'GROUP_NAME',
    'TEAM_NAME',
    'GOALS_FOR',
    'GOALS_AGAINST',
    'FIXTURES',
    'RESULTS',
    'SCORER',
    'STADIUM',
    'ATTENDANCE',
    'REFEREE',
)

# Define the regular expressions for the tokens
t_GROUP_NAME = r'[Gg]roup [A-H]'
t_TEAM_NAME = r'[A-Za-z ]+'
t_GOALS_FOR = r'\d+ goals forwarded'
t_GOALS_AGAINST = r'\d+ goals conceded'
t_FIXTURES = r'[Ff]ixtures'
t_RESULTS = r'[Rr]esults'
t_SCORER = r'[Ss]corer'
t_STADIUM = r'[Ss]tadium'
t_ATTENDANCE = r'[Aa]ttendance'
t_REFEREE = r'[Rr]eferee'

# Define the error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Define the grammar rules
def p_query(p):
    """
    query : group_details
          | team_details
          | knockout_details
    """

def p_group_details(p):
    """
    group_details : GROUP_NAME teams_advanced
                  | GROUP_NAME match_details
    """

def p_teams_advanced(p):
    """
    teams_advanced : 'Teams advanced for knockouts:'
                   | 'Teams qualified for knockout stage:'
    """

def p_match_details(p):
    """
    match_details : TEAM_NAME 'vs' TEAM_NAME match_info
    """

def p_match_info(p):
    """
    match_info : STADIUM ATTENDANCE goal_scorer REFEREE
               | STADIUM REFEREE
               | ATTENDANCE REFEREE
               | goal_scorer REFEREE
               | STADIUM ATTENDANCE REFEREE
               | STADIUM ATTENDANCE goal_scorer
               | STADIUM goal_scorer
               | ATTENDANCE goal_scorer
    """

def p_goal_scorer(p):
    """
    goal_scorer : SCORER
                | SCORER 'and' SCORER
    """

def p_team_details(p):
    """
    team_details : TEAM_NAME stats_info
    """

def p_stats_info(p):
    """
    stats_info : GOALS_FOR GOALS_AGAINST
    """

def p_knockout_details(p):
    """
    knockout_details : FIXTURES
                     | TEAM_NAME 'vs' TEAM_NAME knockout_info
    """

def p_knockout_info(p):
    """
    knockout_info : RESULTS
                  | SCORER
                  | STADIUM
                  | ATTENDANCE
                  | REFEREE
    """

# Define the error handling rule
def p_error(p):
    print("Syntax error in input!")
lexer = lex.lex()
parser = yacc.yacc()

# Read the HTML file and parse it
with open('Fifa_data.html', 'r') as f:
    data = f.read()
    parser.parse(data)