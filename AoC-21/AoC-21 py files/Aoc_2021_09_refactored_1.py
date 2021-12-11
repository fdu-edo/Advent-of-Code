from   aocd.models import Puzzle
from   pprint import pprint
from   functools import cache, reduce
import pandas

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

sort_by_key  = lambda dico: {k: v for k, v in sorted(dico.items(), key=lambda item: item[0])} 
sort_by_val  = lambda dico: {k: v for k, v in sorted(dico.items(), key=lambda item: item[1])} 

def add_border(data):
    maxx, maxy = max([pt[0] for pt in data]), max([pt[1] for pt in data]) 
    for i in range(0, maxx+2) : data[(i,0)], data[(i,maxy+1)] = [False, 'A'], [False, 'A']
    for j in range(0, maxy+2) : data[(0,j)], data[(maxx+1,j)] = [False, 'A'], [False, 'A']
    return data

def print_map(data, erase= '*'):
    """ display the lower points map or the basins map """
    maxx, maxy = max([pt[0] for pt in data.keys()]), max([pt[1] for pt in data.keys()])
    print('\nLower Points:\n' if erase == '*' else '\nSmoke Basins:\n')
    for j in range(1, maxy+1):
        for i in range(1, maxx+1):
            try:    flag, value = data[(i,j)][0], data[(i,j)][1]
            except: flag, value = False, '-'
            if flag :
                print(f'({value})'.replace(str(erase),' '), end='')
            else:
                print(f' {value} '.replace(str(erase),' '), end='')
        print()
    print('\n')

def is_lower(mappoints, x, y):
    """ check if adjacents points (← → ↑ ↓) are lower than given point """
    for near in (mappoints[(x-1,y)][1], mappoints[(x+1,y)][1], mappoints[(x,y-1)][1], mappoints[(x,y+1)][1]):
        if near <= mappoints[(x,y)][1]: return False, int(mappoints[(x,y)][1])
    return True, int(mappoints[(x,y)][1])

#@timer3
def part_1(data):
    """ for each point inside the border search lower points """   
    maxx, maxy = max([pt[0] for pt in data]), max([pt[1] for pt in data]) 
    points   = dict()
    for i in range(1, maxx):
        for j in range(1, maxy):   
            points[(i,j)]= [*is_lower(data, i, j)]
    part_1.points = points
    return sum([points[pt][1] + 1 for pt in points if points[pt][0]])
    

def check_near(mappoints, x, y):
    """ check if adjacents points (← → ↑ ↓) are borders (value = 'A') or 
        higher points (value = 9) or already explored (flag = True)
        if not each one is explored. all points flagged True belong to the same 
        basin starting from the initial lower point """
    if mappoints[(x-1,y)][1] not in ['A', 9] and not mappoints[(x-1,y)][0]: 
         mappoints[(x-1,y)] = [True, mappoints[(x-1,y)][1]]
         check_near(mappoints, x-1, y)
         
    if mappoints[(x+1,y)][1] not in ['A', 9] and not mappoints[(x+1,y)][0]: 
         mappoints[(x+1,y)] = [True, mappoints[(x+1,y)][1]]
         check_near(mappoints, x+1, y)

    if mappoints[(x,y-1)][1] not in ['A', 9] and not mappoints[(x,y-1)][0]: 
         mappoints[(x,y-1)] = [True, mappoints[(x,y-1)][1]]
         check_near(mappoints,  x, y-1)

    if mappoints[(x,y+1)][1] not in ['A', 9] and not mappoints[(x,y+1)][0]: 
         mappoints[(x,y+1)] = [True, mappoints[(x,y+1)][1]]
         check_near(mappoints, x, y+1)
  
#@timer3
def part_2(lowerpoints):
    """ for each lowerpoints qualify the adjacent points """   
    basins_size = []
    for point in [pt for pt in lowerpoints if lowerpoints[pt][0]]:
        # set all points flag to False in a map copy before walking
        basinspoints = {pt:[False, lowerpoints[pt][1]] for pt in lowerpoints}
        check_near(basinspoints, point[0], point[1])
        basinspoints = [pt for pt in basinspoints if basinspoints[pt][0]]
        basins_size.append(len(basinspoints))
    return reduce(lambda x,y:x*y,sorted(basins_size)[-3:])
    
    
if __name__ == '__main__':
    year, day = 2021, 9
    puzzle    = Puzzle(year, day)
    source = 'txt'
    
    pz_data = load_data(f'AoC-{str(year)[2:]} {source} files/Aoc_{year}_{day:02d}.{source}')   
    if pz_data == None: sys.exit()
   
    """ add a 'A'' border around the heightmap in input """
    dt_data, maxx, maxy = dict(), len(pz_data[0]), len(pz_data)
    for i in range(maxx):
        for j in range(maxy):
            dt_data[(i+1, j+1)] = [False, pz_data[j][i]]
    dt_data = add_border(dt_data)
       
    result_1 = part_1(dt_data)    
    if source == 'tst':
        print_map(part_1.points)
    
    dt_data = add_border(part_1.points)
    result_2 = part_2(dt_data)    
    if source == 'tst':
        print_map(part_1.points, erase = 9)
          
    print(f'{chr(10)+"—"*50+chr(10)}my solutions for "{puzzle.title}" on {source} are: "'\
          f'{chr(10)}   part1: {result_1}{chr(10)}   part2: {result_2}')    
    
