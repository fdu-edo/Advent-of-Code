from aocd.models import Puzzle
import pandas
sep = '\n   '

def get_data(datafile):
    with open(datafile, encoding='utf-8', mode = "r") as input_file:
            return input_file.read().strip().split('\n')

makebin = lambda b_list: ''.join([str(x) for x in b_list])
makeint = lambda b_list: int(makebin(b_list),2)   

# most common bit for each column
def get_most(data):
    return [1 if 2*one-len(data) >= 0 else 0 for one in list(data.sum(axis=0))]

# least common bit for each column
def get_least(data):
    return [1 if 2*one-len(data) < 0 else 0 for one in list(data.sum(axis=0))]
          
# reduce dataframe
def reduce_data(data, get_commons):
    # iterate on the dataframe columns left→right
    for col in range(data.shape[1]):
        if data.shape[0] > 1:
           # get the significant bit for the current column
           commons  = get_commons(data)
           # remove the row not containing the significant bit in the current column
           data = data[data[col] == commons[col]]
    return data.mode().iloc[0].to_list()
    
def part_1(data):
    gamma   = get_most(data)
    epsilon = get_least(data)
    return makeint(gamma) * makeint(epsilon)

def part_2(data):
    oxygen = reduce_data(data, get_most)   
    dioxyd = reduce_data(data, get_least)
    return makeint(oxygen) * makeint(dioxyd)
    
if __name__ == '__main__':
    year, day   = 2021, 3
    puzzle = Puzzle(year, day)
    source = 'web' # web, txt, tst
   
    if source == 'web': pz_data = puzzle.input_data.strip().split('\n')
    else: pz_data = get_data(f'Aoc_{year}_{day:02d}.{source}')
    
    pz_data = [[bit for bit in diagline] for diagline in pz_data] 
    pz_data = pandas.DataFrame(pz_data).astype(int)
     
    result_1 = part_1(pz_data)
    result_2 = part_2(pz_data)
        
    print(f'my solutions for "{puzzle.title}" on {source} are: {sep}part1: {result_1}{sep}part2: {result_2}')    
    
