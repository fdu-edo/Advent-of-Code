from aocd.models import Puzzle
from pprint import pprint
from copy   import deepcopy

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
    
def add_border(data, border='A'):
    maxx, maxy = max([pt[0] for pt in data]), max([pt[1] for pt in data]) 
    for i in range(0, maxx+2) : data[(i,0)], data[(i,maxy+1)] = [False, border], [False, border]
    for j in range(0, maxy+2) : data[(0,j)], data[(maxx+1,j)] = [False, border], [False, border]
    return data

def print_map(data, border='A', erase= '.', highlight= '*'):
    minx, miny = 1, 1
    maxx, maxy = max([pt[0] for pt in data.keys()]), max([pt[1] for pt in data.keys()])
    try:
        if data[(0,0)][1] == border: 
            minx, miny = 0, 0
            maxx += 1
            maxy += 1
    except:  pass
    for j in range(minx, maxy):
        for i in range(miny, maxx):
            try:    value = data[(i,j)][1]
            except: value = ' - '
            if value == highlight : value = f'({value})'
            else:  value = f' {value} '
            print(f' {value} '.replace(str(erase),'·'), end='')
        print()
    print('\n')

def propagate_flash(mappoints, x, y):
    if mappoints[(x,y)][1] > 9 and not mappoints[(x,y)][0]:
        mappoints[(x,y)][0] = True
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                try: 
                    mappoints[(i,j)][1] += 1
                    propagate_flash(mappoints, i, j)
                except: ...

#@timer3
def part_1(data, steps):
    """ for each point inside the border increase energy level """   
    flashes = 0
    maxx, maxy = max([pt[0] for pt in data]), max([pt[1] for pt in data]) 
    for _ in range(steps):
        for i in range(1, maxx):
            for j in range(1, maxy):   
                data[(i, j)][1] += 1 # increase nrj by 1 from every octopus               
        for i in range(1, maxx):
            for j in range(1, maxy):   
                if data[(i, j)][1] > 9:  
                    propagate_flash(data, i, j) 
                    data[(i, j)][0] = True
        for i in range(1, maxx):
            for j in range(1, maxy):   
                if data[(i, j)][0]:   
                    flashes += 1
                    data[(i, j)][1] = 0 # if has flashed reset nrj to 0
                data[(i, j)][0] = False # reset flash's flag 
    part_1.data = data
    return flashes
 
    
#@timer3
def part_2(data, steps):
    """ for each point inside the border increase energy level """   
    flashes = 0
    maxx, maxy = max([pt[0] for pt in data]), max([pt[1] for pt in data]) 
    for _ in range(steps):
        for i in range(1, maxx):
            for j in range(1, maxy):   
                data[(i, j)][1] += 1 # increase nrj by 1 from every octopus               
        for i in range(1, maxx):
            for j in range(1, maxy):   
                if data[(i, j)][1] > 9:  
                    propagate_flash(data, i, j) 
                    data[(i, j)][0] = True
        for i in range(1, maxx):
            for j in range(1, maxy):   
                if data[(i, j)][0]:   
                    flashes += 1
                    data[(i, j)][1] = 0 # if has flashed reset nrj to 0
                data[(i, j)][0] = False # reset flash's flag 
        if {data[pt][1] for pt in data if data[pt][1]!='-'} == {0}:  
            part_2.data = data
            return _ + 1
    part_2.data = data
    return 'no simultaneous flash yet, try again !'
    
            
    
if __name__ == '__main__':
    year, day = 2021, 11
    puzzle    = Puzzle(year, day)
    source = 'txt'
    
    pz_data = load_data(f'AoC-{str(year)[2:]} {source} files/Aoc_{year}_{day:02d}.{source}')   
    if pz_data == None: sys.exit()
    
    """ add a '-' border around the octopus map in input """
    maxx, maxy = len(pz_data[0]), len(pz_data)
    dt_data = {(i+1, j+1):[False, int(pz_data[j][i])] for i in range(maxx) for j in range(maxy)}
    dt_data = add_border(dt_data,  border= '-')
    # print('initial)')
    # print_map(dt_data)
    
    result_1 = part_1(deepcopy(dt_data), 100)    
    # print('part 1:')
    # print_map(part_1.data)

    result_2 = part_2(deepcopy(dt_data), 500)    
    # print('part 2:')
    # print_map(part_2.data)
         
    print(f'{chr(10)+"—"*50+chr(10)}my solutions for "{puzzle.title}" on {source} are: "'\
          f'{chr(10)}   part1: {result_1}{chr(10)}   part2: {result_2}')    
    
