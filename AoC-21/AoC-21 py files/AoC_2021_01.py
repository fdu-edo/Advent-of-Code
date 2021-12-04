# -*- coding: utf-8 -*-
# !/usr/bin/env python
# created on Fri Sep 10 09:14:54 2021 by fdu

#╔═══════════════════════════════════════════════════════════════════════════════════════╦════════╗
#║ MAIN                                                                                  ║V - 0.1 ║
#╚═══════════════════════════════════════════════════════════════════════════════════════╩════════╝

from aocd.models import Puzzle
sep = '\n   '

def get_data(datafile):
    with open(datafile, encoding='utf-8', mode = "r") as input_file:
            return input_file.read().strip().split('\n')
        
def part_1(data):
    return sum([1 if data[i+1] > data[i] else 0 for i in range(len(data)-1)])

def part_2(data):
    return sum([1 if data[i+3] > data[i] else 0 for i in range(len(data)-3)])


if __name__ == '__main__':
    year   = 2021
    day    = 1
    puzzle = Puzzle(year, day)
    
    source = 'web' # web, txt, tst
   
    if   source == 'web': pz_data = puzzle.input_data.strip().split('\n')
    elif source == 'txt': pz_data = get_data(f'Aoc_{year}_{day:02d}.txt')
    elif source == 'tst': pz_data = get_data(f'Aoc_{year}_{day:02d}.tst')
    else : print('¯\\_(ツ)_/¯')

    pz_data = puzzle.input_data.strip().split('\n')
    pz_data = [int(elt) for elt in pz_data] 

    result_1 = part_1(pz_data)
    result_2 = part_2(pz_data)
    

    print(f'my solutions for "{puzzle.title}" on {source} are: {sep}part1: {result_1}{sep}part2: {result_2}')    
    
    
