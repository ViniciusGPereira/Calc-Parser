## Link do trabalho https://notebooks.azure.com/ViniciusPereira/libraries/calc-parser

#IMPORTAÇÃO DAS BIBLIOTECAS UTILIZADAS
import ply.lex as lex
import ply.yacc as yacc
import math
import sys


#Lista de tokens aceitos
tokens = [
    'INT',
    'FLOAT',
    'SOMA',
    'SUBTRACAO',
    'DIVISAO',
    'MULTIPLICACAO',
    'RAIZ',
    'EXPONENCIACAO',
    'PARENTESQ',
    'PARENTDIR',
    'SENO',
    'COSSENO'
]

#Simbolos que representam os tokens
t_SOMA = r'\+'
t_SUBTRACAO = r'\-'
t_DIVISAO = r'\/'
t_MULTIPLICACAO = r'\*'
t_RAIZ = r'\.r'
t_EXPONENCIACAO = r'\^'
t_PARENTESQ = r'\('
t_PARENTDIR = r'\)'
t_SENO = r'\.s'
t_COSSENO = r'\.c'

#Para identificar espaços em branco
t_ignore = r' '

#Função para identificar floats
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

#Função para identificar inteiros
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

#Reconhecimento de caracteres invalidos
def t_error(t):
    print("Caracter Inválido !")
    t.lexer.skip(1)

#Cria analisado lexico
lexer = lex.lex()

#Ordem de leitura de simbolos
precedence = (
    ('left', 'SOMA', 'SUBTRACAO'),
    ('left', 'MULTIPLICACAO', 'DIVISAO')
)

#Função para calculo
def p_calc(p):
    '''
    calc : expression
         | empty
    '''
    print(run(p[1]))

#Definição de expressão    
def p_expression(p):
    '''
    expression : expression SOMA expression
               | expression SUBTRACAO expression
               | expression MULTIPLICACAO expression
               | expression DIVISAO expression
               | expression EXPONENCIACAO expression
    '''
    p[0] = (p[2], p[1], p[3])

#Operações em um outro formato
def p_expression_operacoes_esp(p):
    '''
    expression : RAIZ PARENTESQ expression PARENTDIR 
               | SENO PARENTESQ expression PARENTDIR
               | COSSENO PARENTESQ expression PARENTDIR
    '''
    p[0] = (p[1], p[3])

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0] = p[1]

def p_error(p):
    print("Sintaxe com erro!")

#para espaços vazios
def p_empty(p):
    '''
    empty :    
    '''
    p[0] = None

#instanciando o parser
parser = yacc.yacc()

def run(p):
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '.r':
            return math.sqrt(run(p[1]))
        elif p[0] == '^':
            return math.pow(run(p[1]), run(p[2]))
        elif p[0] == '.s':
            return math.sin(math.radians(run(p[1])))
        elif p[0] == '.c':
            return math.cos(math.radians(run(p[1])))      
    else:
        return p
        
while True:
    try:
        s = input('')
    except EOFError:
            break
    parser.parse(s)
