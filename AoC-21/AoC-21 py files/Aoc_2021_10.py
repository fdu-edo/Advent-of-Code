from aocd.models import Puzzle
from pprint      import pprint

import sys
sys.path.append('../../PSA/SCALIAN__GENERIC/1_COMMON_TOOLS')
from CMN_TOOLS_DEBUG import timer3, get_time

def load_data(datafile):
    try:
        with open(datafile, encoding='utf-8', mode = 'r')as input_file:
            return input_file.read().strip().split('\n')
    except: 
        print('→ File not found ! ←')
        return None

chars_op = '([{<'    
chars_cl = ')]}>'    
err_score = {')':3, ']':57, '}':1197, '>':25137}
cpl_score = {')':1, ']':2, '}':3, '>':4}

opp = lambda c: chars_cl[chars_op.index(c)] if c in chars_op else chars_op[chars_cl.index(c)]


#@timer3
def part_1(data):
    """ looking at the corrupted lines : stop analysys at first closing delimiter that doesn't 
        match the last opening one """    
    error_score = 0
    last_opened = ''
    corrupted   = []
    for line in data:
        for char in line:
            if    char in chars_op: 
                last_opened += char
            else:
                if opp(char) != last_opened[-1]:
                    error_score += err_score[char]
                    corrupted += [line]
                    break
                else:
                    last_opened = last_opened[:-1]
    part_1.corrupted = corrupted               
    return error_score
    

#@timer3
def part_2(data):
    """ looking at the corrupted lines : in a legal line  each opening delimiter *
        should have a closing one corresponding. stacking/unstacking delimiters, 
        at the end of a line's reading, only the unmatched delimiters remain.
        invert them and use them in score formulae """    
    scores = []
    for line in data:
        last_opened = ''
        for char in line:
            if char in chars_op: last_opened += char
            else: last_opened = last_opened[:-1]         
            score = 0
            for char in [opp(char) for char in last_opened[::-1]]: score = score *5 + cpl_score[char]        
        scores += [score]
    scores = sorted(scores)
    return scores[len(scores)//2]
    
if __name__ == '__main__':
    year, day = 2021, 10
    puzzle    = Puzzle(year, day)
    source = 'txt'
    
    pz_data = load_data(f'AoC-{str(year)[2:]} {source} files/Aoc_{year}_{day:02d}.{source}')   
    if pz_data == None: sys.exit()
    

    result_1 = part_1(pz_data)    
    
    ''' remove the corrupted lines for further analysis '''
    for corrupted in part_1.corrupted : pz_data.remove(corrupted)  
    result_2 = part_2(pz_data)    
          
    print(f'{chr(10)+"—"*50+chr(10)}my solutions for "{puzzle.title}" on {source} are: "'\
          f'{chr(10)}   part1: {result_1}{chr(10)}   part2: {result_2}')    
    