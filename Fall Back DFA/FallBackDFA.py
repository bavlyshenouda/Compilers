import argparse
from DFA import DFA
from stack import StackClass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--dfa-file', action="store", help="path of file to take as input to construct DFA", nargs="?", metavar="dfa_file")
    parser.add_argument('--input-file', action="store", help="path of file to take as input to test strings in on DFA", nargs="?", metavar="input_file")
    
    args = parser.parse_args()
    output_file = open('task_3_1_result.txt', "w+")
    dfa = DFA(args.dfa_file)
    with open(args.input_file, "r") as file:
        for line in file:
            line = line.strip()
            r = 0
            l = 0
            stk = StackClass()
            while r<len(line):
                currentState = dfa.start_state
                stk.push(dfa.start_state)
                while l < len(line):
                    for trans in dfa.transitions:
                        if(trans["from"] == currentState and trans["opperand"] == line[l]):
                            stk.push(trans["to"])
                            currentState = trans["to"]
                            break
                    l = l + 1
                lastState = ""
                print(stk)
                while (not (stk.isEmpty() or stk.peek() in dfa.final_state)):
                    lastState = stk.pop()
                    l = l - 1
                if(not stk.isEmpty()):
                    #if a final state is found
                    lastState = stk.peek()
                else :
                    l = len(line)
                expr = dfa.expMap[lastState]
                out = dfa.OutputMap[expr]
                output_file.write(line[r:l] + ", " + out+"\n")
                print(line[r:l] + ", " + out)
                r = l 
                print("r = "+ str(r))
                print("l = "+ str(l))
                if(stk.isEmpty()):
                    break
                stk.items.clear()
                