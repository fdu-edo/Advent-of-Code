from aocd.models import Puzzle
import datetime

def save_data(datafile, data):
    with open(datafile, encoding='utf-8', mode = 'w') as output_file:
        for line in data: 
            output_file.write(line+'\n')
    
if __name__ == '__main__':
    today = datetime.datetime.now()
    year, day   = today.year, today.day
    puzzle = Puzzle(year, day)
   
    pz_data = puzzle.input_data.strip().split('\n')
    save_data(f'Aoc_{year}_{day:02d}.txt', pz_data)   


    # for i in [e for e in dir(puzzle) if e[0]!='_' and e!='input_data']:
    #     #print(i) 
    #     print(i, eval('puzzle.'+i))