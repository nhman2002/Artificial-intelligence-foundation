from MyAlgo import MyAlgo
import os

# Get the absolute path to the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = [os.path.join(script_dir, 'input', 'input_1.txt'),
              os.path.join(script_dir, 'input', 'input_2.txt'),
              os.path.join(script_dir, 'input', 'input_3.txt'),
              os.path.join(script_dir, 'input', 'input_4.txt'),
              os.path.join(script_dir, 'input', 'input_5.txt')]

OUTPUT_FILE = [os.path.join(script_dir, 'output', 'output1.txt'),
               os.path.join(script_dir, 'output', 'output2.txt'),
               os.path.join(script_dir, 'output', 'output3.txt'),
               os.path.join(script_dir, 'output', 'output4.txt'),
               os.path.join(script_dir, 'output', 'output5.txt')]

testcase_num = len(INPUT_FILE)

def main():
    for index in range(testcase_num):
        my_algo = MyAlgo()
        my_algo.read_file(input_file=INPUT_FILE[index])
        my_algo.pl_resolution()
        my_algo.write_file(output_file=OUTPUT_FILE[index])

if __name__ == '__main__':
    main()
