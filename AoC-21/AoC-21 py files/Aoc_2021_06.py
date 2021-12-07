# created on mon 12 6 HH:MM:SS 2021 by fdu
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
def part_1(fishes, days):
    """  for each day, add a new fish for every fish in 0 status
         the new fishes have a status of 9 (will be decreased before the 
         end of the day. then decrease all status by one if status > 0
         or increase to 6 if status is 0. tinally return nb of fishes """       
    for each_day in range(days):
        fishes += [9]*fishes.count(0)
        fishes =  [fish-1 if fish else 6 for fish in fishes]    
    part_1.data = fishes
    return len(fishes)
    
cache = {0:1}
def fish_family(generation):
    """ Calculate the number of heirs for a fish after multiple generations. 
        → cached recursion version : each result of f_f(g) is stored in cache 
        for a newborn it takes 8 generation to be able 
        to produce another newborn.then it takes only 6. production happens day after 
        status = 0 (shift 1). finally return nb of fishes """
    if generation <1: return 1
    if generation in cache: return cache[generation]
    cache[generation] = fish_family(generation - 7) + fish_family(generation - 9)
    return cache[generation]

@timer3
def part_2(fishes, days):
    """ count family mebers after days generations for each initial fish
        and add them to the grand total """ 
    count = 0
    for fish in fishes:
        count += fish_family(days - fishes[fish])
    return count
    
if __name__ == '__main__':
    year, day = 2021, 6
    puzzle    = Puzzle(year, day)
    source = 'txt'
    
    pz_data = load_data(f'AoC-{str(year)[2:]} {source} files/Aoc_{year}_{day:02d}.{source}')   
    if pz_data == None: sys.exit()
    
    """ convert pz_data in a list of integers (initial status of a fish)
        for part_1 non optimized solution """
    fishes_data = [int(i) for i in pz_data[0].split(',')]    
    result_1 = part_1(fishes_data, 80)    
    
    """ convert pz_data in a dict {fish_id:initial status}
        for part_1 optimized and part_2 optimized """
    fishes_data = {i:int(v) for i,v in enumerate(pz_data[0].split(','))}
    result_2 = part_2(fishes_data, 80) # to compare with part_1 time
    result_2 = part_2(fishes_data, 256)
      
    print(f'{chr(10)+"—"*50+chr(10)}my solutions for "{puzzle.title}" on {source} are: "'\
          f'{chr(10)}   part1: {result_1}{chr(10)}   part2: {result_2}')    
    
