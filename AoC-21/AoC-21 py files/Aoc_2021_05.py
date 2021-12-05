# created on Sun Dec 05 08:28:54 2021 by fdu
from collections import Counter
from aocd.models import Puzzle

import sys
sys.path.append('../../PSA/SCALIAN__GENERIC/1_COMMON_TOOLS')
import CMN_TOOLS_DEBUG

def load_data(datafile):
    with open(datafile, encoding='utf-8', mode = 'r') as input_file:
            return input_file.read().strip().split('\n')

@CMN_TOOLS_DEBUG.timer3
def calc_freq_over_two(pairs_of_points):
    """ create a dict with pair of points as key and frquency as value 
        then keep only the freq >= 2 and count how many pairs"""
    freq = Counter(pairs_of_points)
    return len({key:freq[key] for key in freq.keys() if freq[key] >= 2})

def complete_hv_line(line):
    """ looking at the direction of vector (c-a,d-b) 
        and retrieve points in between if relevant """
    s1, e1, s2, e2 = line[0], line[1], line[2], line[3]
    if s1 == s2:   # if vector is vertical (0,y)
        inter = [(s1, min(e1, e2) + j) for j in range(abs(e2-e1) + 1)] 
    elif e1 == e2: # if vector is horizontal (x,0)
        inter = [(min(s1, s2) + i, e1) for i in range(abs(s2 - s1)+ 1)]
    else: return []
    return inter

def complete_hvd_line(line):    
    """ looking at the direction of vector (c-a,d-b) 
        and retrieve points in between if relevant """
    s1, e1, s2, e2 = line[0], line[1], line[2], line[3]
    if s1 == s2:   # if vector is vertical (0,y)
        inter = [(s1, min(e1, e2) + j) for j in range(abs(e2-e1) + 1)] 
    elif e1 == e2: # if vector is horizontal (x,0)
        inter = [(min(s1, s2) + i, e1) for i in range(abs(s2 - s1)+ 1)]
    elif s2-s1 == e2-e1: # if vector is diagonal (1,1)  
        inter = [(min(s1, s2) + i, min(e1,e2) + i) for i in range(abs(e2-e1)+1)]
    elif s2-s1 == e1-e2: # if vector is diagonal (1,-1)  
        inter =  [(min(s1, s2) + i, max(e1,e2) - i) for i in range(abs(e2-e1)+1)]
    else: inter = []   
    return inter

def part_1(data):
    """ looping on [a,b,c,d] vector, add the retrieved points in between 
        to the list of potential dangerous points """       
    points = []
    for line in data:
        points += complete_hv_line(line)
    return calc_freq_over_two(points)
    
def part_2(data):
    """ looping on [a,b,c,d] vector, add the retrieved points in between 
        to the list of potential dangerous points """       
    points = []
    for line in data:
        points += complete_hvd_line(line)
    return calc_freq_over_two(points)
    
if __name__ == '__main__':
    year, day = 2021, 5
    puzzle    = Puzzle(year, day)
    source = 'txt'

    with open(f'Aoc_{year}_{day:02d}.{source}', encoding='utf-8', mode = 'r')as input_file:
        pz_data = input_file.read().strip().split('\n')
        
    # convert each a,b → c,d line in a [a,b,c,d] vector
    pz_data = [[int(res) for res in line.replace(' -> ',' ').replace(',',' ').split(' ')] for line in pz_data]

    result_1 = part_1(pz_data)    
    result_2 = part_2(pz_data)
        
    print(f'{chr(10)+"—"*50+chr(10)}my solutions for "{puzzle.title}" on {source} are: "'\
          f'{chr(10)}   part1: {result_1}{chr(10)}   part2: {result_2}')    
    
