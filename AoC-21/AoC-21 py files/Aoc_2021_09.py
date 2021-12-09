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

def print_map(data, erase= '*'):
    maxx, maxy = max([lwrpts[1] for lwrpts in data]), max([lwrpts[0] for lwrpts in data])
    print('part1: Lower points\n' if erase =='*' else 'part2: basins\n')
    for j in range(maxy):
        for i in range(maxx):
            if data[i+j*maxx][2]:
                print(f'({data[i+j*maxx][3]})'.replace(str(erase),' '), end='')
            else:
                print(f' {data[i+j*maxx][3]} '.replace(str(erase),' '), end='')
        print()
    print('\n')

def get_point(data, j, i):
    maxx, maxy = max([lwrpts[1] for lwrpts in data]), max([lwrpts[0] for lwrpts in data])
    if i in (0, maxx+1) or j in (0,maxy+1): 
        return (i, j , False, 'A')
    else:     
        return data[(i-1)+(j-1)*maxx]

def set_point_flag(data, j, i, value):
    maxx = max([lwrpts[1] for lwrpts in data])
    index = (i-1)+(j-1)*maxx
    data[index] = (data[index][0], data[index][1], value, data[index][3])

def is_lower(df, x, y):
    for near in (df.iloc[x-1,y], df.iloc[x+1,y], df.iloc[x,y-1], df.iloc[x,y+1]):
        if near <= df.iloc[x,y]: return False, int(df.iloc[x,y])
    return True, int(df.iloc[x,y])

@timer3
def part_1(data):
    """ for each point inside the border search lower point """   
    points   = []
    for i in range(1, data.shape[0]-1):
        for j in range(1, data.shape[1]-1):   
            points += [(i, j, *is_lower(data, i, j))]
    return sum([lwrpts[3] + 1 for lwrpts in points if lwrpts[2]]), points
    
def check_near(mappoints, x, y):
     if get_point(mappoints, x-1, y)[3] not in ['A', 9] and not get_point(mappoints, x-1, y)[2]: 
         # print(' ↑', get_point(mappoints, x-1, y))
         set_point_flag(mappoints, x-1, y, True)
         check_near(mappoints, x-1, y)

     if get_point(mappoints, x+1, y)[3] not in ['A', 9] and not get_point(mappoints, x+1, y)[2]: 
         # print(' ↓', get_point(mappoints, x+1, y))
         set_point_flag(mappoints, x+1, y, True)
         check_near(mappoints, x+1, y)

     if get_point(mappoints, x, y-1)[3] not in ['A', 9] and not get_point(mappoints, x, y-1)[2]: 
         # print(' ←', get_point(mappoints, x, y-1))
         set_point_flag(mappoints, x, y-1, True)
         check_near(mappoints,  x, y-1)

     if get_point(mappoints, x, y+1)[3] not in ['A', 9] and not get_point(mappoints, x, y+1)[2]: 
         # print(' →', get_point(mappoints, x, y+1))
         set_point_flag(mappoints, x, y+1, True)
         check_near(mappoints, x, y+1)
  
@timer3
def part_2(mappoints):
    """ for each lowerpoints qualify the adjacent points """   
    basins_size = []
    for point in [lwrpts for lwrpts in mappoints if lwrpts[2]]:
        # set all points flag to False
        basinpoints = [(pts[0], pts[1], False, pts[3]) for pts in mappoints]
        check_near(basinpoints, point[0], point[1])
        basinpoints = [(pts[0], pts[1]) for pts in basinpoints if pts[2]]
        #print(basinpoints)
        basins_size.append(len(basinpoints))
    return reduce(lambda x,y:x*y,sorted(basins_size)[-3:])
    
    
if __name__ == '__main__':
    year, day = 2021, 9
    puzzle    = Puzzle(year, day)
    source = 'txt'
    
    pz_data = load_data(f'AoC-{str(year)[2:]} {source} files/Aoc_{year}_{day:02d}.{source}')   
    if pz_data == None: sys.exit()
    
    """ add a 'A'' border around the heightmap in input """
    # # print(pz_data)
    pz_data = ['A'*len(pz_data[0])] + pz_data + ['A'*len(pz_data[0])]
    pz_data = [['A']+[heightpoint for heightpoint in heightline]+['A'] for heightline in pz_data] 
    pz_data = pandas.DataFrame(pz_data)
    # print(pz_data)
    
    print()
    result_1, points = part_1(pz_data)    
    if source == 'tst':
        print_map(points)
    
    if source == 'tst':
        print_map(points, erase = 9)
    result_2 = part_2(points)    
          
    print(f'{chr(10)+"—"*50+chr(10)}my solutions for "{puzzle.title}" on {source} are: "'\
          f'{chr(10)}   part1: {result_1}{chr(10)}   part2: {result_2}')    
    
