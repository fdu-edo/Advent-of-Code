from aocd.models import Puzzle

def load_data(datafile):
    with open(datafile, encoding='utf-8', mode = 'r') as input_file:
            return input_file.read().strip().split('\n')

def cross_board(board, drw):
    """ replace numner already drawn by # in a board"""
    return [['#' if board[i][j] == drw else board[i][j] for j in range(5)] for i in range(5)]

def calc_board(board):
    """ sum the ramaining number of a board """    
    return sum([board[i][j] if board[i][j] != '#' else 0 for i in range(5) for j in range(5)])

def transpose_board(board):
    """ transpose a board """
    return [[board[j][i] for j in range(5)] for i in range(5)]

def check_board(board):
    """ check if one of the lines is full of # 
        then transpose the board and check again (ie check columns) """
    res1  = sum([1 if line == ['#',]*5 else 0 for line in board])
    board = transpose_board(board)
    res2  = sum([1 if line == ['#',]*5 else 0 for line in board])
    return res1 or res2

def part_1(drws, brds):
    """ for each drawn number replace the number by a # in boards
        then check if board is a win, if yes calculate result with current board
        and current drawn number. Else continue to cross/check boards """       
    for draw in drws:
        tmp_boards = []
        for board in brds:
            board = cross_board(board, draw)
            check = check_board(board)
            tmp_boards.append(board)
            if check: 
                return calc_board(board) * draw
            else:
                brds = tmp_boards
    
def part_2(drws, brds):
    """ for each drawn number replace the number by a # in boards
        then check if board is a win, if yes keep the drawn number, remove 
        the winning board and continue. The last board remaining and the last 
        drawn number give the result """       
    last_draw = 0
    for draw in drws:
        tmp_boards = []
        for board_id, board in enumerate(brds):
            board = cross_board(board, draw)
            check = check_board(board)
            if check: 
                last_draw = draw
            else:
                tmp_boards.append(board)
        brds = tmp_boards
    return calc_board(board) * last_draw
    
if __name__ == '__main__':
    year, day = 2021, 4
    puzzle    = Puzzle(year, day)
    source = 'tst'

    with open(f'Aoc_{year}_{day:02d}.{source}', encoding='utf-8', mode = 'r')as input_file:
        pz_data = input_file.read().strip().split('\n')
              
    draws  = [int(result) for result in pz_data[0].split(',')]
    boards = [[int(result) for result in  packed_result.split()] 
              for packed_result in pz_data[1:] if packed_result != '']
    boards = [[elt for elt in boards[board*5:(board+1)*5]] for board in range(len(boards)//5)]
             
    result_1 = part_1(draws, boards)    
    result_2 = part_2(draws, boards)
        
    print(f'{chr(10)+"—"*50+chr(10)}my solutions for "{puzzle.title}" on {source} are: "'\
          f'{chr(10)}   part1: {result_1}{chr(10)}   part2: {result_2}')    
    
