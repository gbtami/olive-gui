from nodes import *

# globals
nodelist = []


def p_empty(p):
    'empty :'
    pass

# lex & yacc transform the popeye output into a list of Nodes
# the final rule - BuildTree - transforms this list into a tree

def p_BuildTree(t):
    'BuildTree: Solution'
    nodelist = t[1]
    nodelist[0].unflatten(nodelist, 1)
    nodelist[0].linkContinuedTwins()


def p_Solution_Movelist(t):
    'Solution: MoveList'
    t[0] = [Node(), VirtualTwinNode()] + t[1]


def p_Solution_TwinList(t):
    'Solution: TwinList'
    t[0] = [Node()] + t[1]


def p_Solution_Comments(t):
    'Solution: Comments Solution'
    t[0] = t[2]
    t[0][0].setv('comments', t[1])


def p_Solution_empty(t):
    'Solution: empty'
    t[0] = [Node()] # empty input


def p_TwinList(t):
    '''TwinList: Twin
                | TwinList Twin'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = t[1] + t[2]


def p_Twin(t):
    'Twin: TwinHeader MoveList'
    t[0] = [t[1]] + t[2]


def p_TwinHeader_TwinBullet(t):
    'TwinHeader: TwinBullet'
    t[0] = t[1]


def p_TwinHeader_CommandList(t):
    'TwinHeader: TwinBullet CommandList'
    t[0] = t[1].setv('commands', t[2])


def p_TwinHeader_Comments(t):
    'TwinHeader: TwinHeader Comments'
    t[0] = t[1].setv('comments', t[2])


def p_TwinBullet(t):
    '''TwinBullet:  TwinId
                | PLUS TwinId'''
    if t[1] != '+':
        t[0] = TwinNode(t[1], False)
    else:
        t[0] = TwinNode(t[2], True)


def p_CommandList(t):
    '''CommandList: Command
                | CommandList Command'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[2]]


def p_Command(t):
    '''Command: LongPieceDecl Square LONG_ARROW Square
            | LongPieceDecl Square DOUBLE_POINTED_ARROW LongPieceDecl Square
            | DASH LongPieceDecl Square
            | PLUS LongPieceDecl Square
            | ROTATE INT
            | MIRROR Square DOUBLE_POINTED_ARROW Square
            | SHIFT Square LONG_DOUBLE_ARROW Square
            | POLISH_TYPE
            | IMITATOR SquareList'''
    if len(t) == 5 and t[3] == '-->':
        t[0] = TwinCommand("Move", [t[2], t[4]])
    elif len(t) == 6 and t[3] == '<-->':
        t[0] = TwinCommand("Exchange", [t[2], t[5]])
    elif t[1] == '-':
        t[0] = TwinCommand("Remove", [t[3]])
    elif t[1] == '+':
        t[0] = TwinCommand("Add", [t[2], t[3]])
    elif t[1] == 'rotate':
        t[0] = TwinCommand("Rotate", [t[2]])
    elif t[1] == 'mirror':
        t[0] = TwinCommand("Mirror", [t[2], t[4]])
    elif t[1] == 'shift':
        t[0] = TwinCommand("Shift", [t[2], t[4]])
    elif t[1] == 'PolishType':
        t[0] = TwinCommand("PolishType", [])
    elif t[1] == 'Imitator':
        t[0] = TwinCommand("Imitator", t[2])


def p_MoveList(t):
    '''MoveList: Move
            | MoveList Move	'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[2]]


def p_Move(t):
    '''Move: MoveNo HalfMove HalfMove
            | MoveNo HALF_ELLIPSIS HalfMove
            | MoveNo HALF_ELLIPSIS ELLIPSIS
            | MoveNo HalfMove THREAT
            | BUT MoveNo HALF_ELLIPSIS HalfMove
            | MoveNo HalfMove ZUGZWANG
            | MoveNo HalfMove'''
    pass