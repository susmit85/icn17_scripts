import numpy as np
import argparse
import random


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', help='file to downsample', type=str, required=True)
    parser.add_argument('-p', '--percentage', help='percentage to downsample', type=float, required=True)
    parser.add_argument('-o', '--output',  help='output file', type=str, required=False)
    args = parser.parse_args()

    filename = args.filename
    percentage = args.percentage
    output_file = args.output if args.output is not None else filename+str(percentage)

    num_lines = sum(1 for line in open(filename, 'r'))
    sample_arr_size = int(num_lines*percentage/100)


    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    random_choice = random.sample(lines, sample_arr_size)

    with open(output_file, 'w') as w:
        w.write(''.join(sorted(random_choice, key=lambda random_choice: int(random_choice.split('\t')[0]))))
#        print('\n'.join(random_choice))
        

