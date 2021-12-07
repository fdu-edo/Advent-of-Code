# created on tue 12 7 08:16:32 2021 by fdu
from collections import Counter
from aocd.models import Puzzle

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

@timer3
def part_1(data):
    """ get the range of targets (min → max) of crabs position
        calculate for each target the lowest cost (crab's pos - target)  """    
    positions = sorted(data)
    # targets   = list(set(data))
    targets   = range(positions[0], positions[-1])
    distances = [(target,sum([abs(position - target) for position in positions])) for target in targets]
    best_pos  = min(distances, key= lambda x: x[1])
    return best_pos[1]
    
def moves_cost(deplacement):
    """ new cost calculation is based on the trinagular value of an integer
        tn = n(n+1)/2 """
    cost = int((deplacement * (deplacement + 1))/2)
    return cost

@timer3
def part_2(data):
    """ get the range of targets (min → max) of crabs position
        calculate for each target the lowest cost (crab's pos - target)  """    
    positions = sorted(data)
    # targets   = list(set(data))
    targets   = range(positions[0], positions[-1])
    distances = [(target,sum([moves_cost(abs(position - target)) for position in positions])) for target in targets]
    best_pos  = min(distances, key= lambda x: x[1])
    return best_pos[1]
    
if __name__ == '__main__':
    year, day = 2021, 7
    puzzle    = Puzzle(year, day)
    source = 'txt'
    
    pz_data = load_data(f'AoC-{str(year)[2:]} {source} files/Aoc_{year}_{day:02d}.{source}')   
    if pz_data == None: sys.exit()
    
    """  """
    pz_data = [int(i) for i in pz_data[0].split(',')]   
    # print(pz_data)
    
    print()
    result_1 = part_1(pz_data)    
    result_2 = part_2(pz_data)    
          
    print(f'{chr(10)+"—"*50+chr(10)}my solutions for "{puzzle.title}" on {source} are: "'\
          f'{chr(10)}   part1: {result_1}{chr(10)}   part2: {result_2}')    
    
