# -*- coding: utf-8 -*-
# !/usr/bin/env python
# created on Wed Dec  8 08:28:44 2021 by fdu
# 🐍 Spyder

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
digits = {'abcefg': '0', 'cf': '1', 'acdeg': '2', 'acdfg': '3', 'bcdf': '4',
          'abdfg': '5', 'abdefg': '6', 'acf': '7', 'abcdefg': '8', 'abcdfg': '9'}

invert_dict  = lambda dico: dict((v,k) for k,v in dico.items()) # exchange keys ↔ values
sort_by_val  = lambda dico: {k: v for k, v in sorted(dico.items(), key=lambda item: item[1])} # sort dict by values
get_by_val   = lambda dico, occ: [k for k in dico if dico[k] == occ] # get the keys occuring occ times
order        = lambda string: ''.join([car if car in string else '' for car in 'abcdefg']) # reorder the chars in astring
remove       = lambda string, cars : ''.join(['' if c in cars else c for c in string]) # remove from string the chars in cars
keep         = lambda string, occ  : ''.join(set([c if string.count(c) == occ else '' for c in string])) # keep the char occuring occ times in string
unique       = lambda string       : ''.join(set([c for c in string])) # keep only one occ of each char
decode       = lambda string, ciph : ''.join([ciph[c] for c in string]) # use code to decode a string
    
@timer3
def part_1(data):
    """ just keep the displays part, count the groups of letters with a length
        corresponding to 1, 4, 7 and 8 i.e 2, 4, 3 and 7 segments """    
    displays = ''.join([line.split('|')[1] for line in data])  
    lengths  = [len( digit) for digit in displays.split()]
    count    = sum([1 if l in [2, 4, 3, 7] else 0 for l in lengths])
    return count

def process_line(line):
    inputs, outputs  = str.strip(line).split('|')   
    inputs  = str.strip(inputs)
    outputs = str.strip(outputs)
    
    signals = inputs.split()
    signals = {sig:len(sig) for sig in signals}
    
    code = dict()
    d_1          = get_by_val(signals, 2) # find segments associated to 1 (2 segs : CF)   
    d_7          = get_by_val(signals, 3) # find segments associéted to 7 (3 segs : ACF)  
    code['A']    = remove(d_7[0], d_1[0]) # A segment is the one not shared by 1 & 7
    code['C']    = d_1[0] # C segment could have both values not shared by 1 & 7
    code['F']    = d_1[0] # same for F
    
    d_4          = get_by_val(signals, 4) # find segments associated to 4 (4 segs : BCDF) 
    code['B']    = remove(d_4[0], d_1[0]) # B segment could have values not shared with 1 (CF) 
    code['D']    = remove(d_4[0], d_1[0]) # same for D 
    
    d_235        = ''.join(s for s in get_by_val(signals, 5)) # find segments associated to 2,3,5 (5 segs in ABCDEFG)
    d_235_common = keep(d_235, 3) # keep the three common segments : A,D,G are common to 2,3,5
    code['G']    = remove(d_235_common , code['A'] + code['D']) # remove A and D (2 values) → G is defined
    code['D']    = remove(d_235_common , code['A'] + code['G']) # remove A and G → D is defined
    
    code['B']    = remove(code['B'], code['D']) # as D is known, B is known
    code['E']    = remove(keep(d_235, 1), code['B']) # C,F are shared 2 by 2 2,3,5 E is unique → E is defined 
    
    d_069        = ''.join(s for s in get_by_val(signals, 6)) # find segments associated to 0,6,9 (6 segs in ABCDEFG)
    d_069_common = keep(d_069, 3) # A,B,G,F are shared between 0,6,9 and appear 3 times
    code['F']    = remove(d_069_common , code['A'] + code['B'] + code['G']) # A,B,G are known → F is defined
    code['C']    = remove(code['C'], code['F']) # C can't tale the F value (and is last value available)
    
    code         = invert_dict(code) # ready to decode
       
    # return int(''.join([str(digits[order(str.lower(decode(output, code)))]) for output in outputs.split()]))
    value = ''
    for output in outputs.split():
        output = decode(output, code) # decode 
        output = str.lower(output) # lower code to match digits keys
        output = order(output) # chars in alphabet's order
        output = digits[output]
        value += output
    return int(value)
@timer3
def part_2(data):
    """ just keep the inputs part  """  
    value = 0
    for line in data:
        value += process_line(line)
    return value
    
if __name__ == '__main__':
    year, day = 2021, 8
    puzzle    = Puzzle(year, day)
    source = 'txt'
    
    pz_data = load_data(f'AoC-{str(year)[2:]} {source} files/Aoc_{year}_{day:02d}.{source}')   
    if pz_data == None: sys.exit()
        
    print()
    result_1 = part_1(pz_data)    
    result_2 = part_2(pz_data)    
          
    print(f'{chr(10)+"—"*50+chr(10)}my solutions for "{puzzle.title}" on {source} are: "'\
          f'{chr(10)}   part1: {result_1}{chr(10)}   part2: {result_2}')    
    
