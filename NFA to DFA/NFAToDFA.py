import argparse
from NFA import NFA

def getClosure(transitions, start, Result):
    next = []
    for s in start:
        for t in transitions:
            if t["from"] == s and t['opperand'] == " " and not(t["to"] in Result):
                next.append(t["to"])
                Result.append(t["to"]) 
    if len(next)>0:
        return  getClosure(transitions, next, Result)
    return Result
     
if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")
    args = parser.parse_args()
    nfa = NFA(args.file)
    #get DFA start state
    start = getClosure(nfa.transitions, [nfa.start_state], [nfa.start_state])
    nfa.alphabet.remove(" ")
    table = {"states" : []}
    for a in nfa.alphabet:
        table[a] = []
    currentState = start
    nextState = []
    done = []
    toBeDone = [start]
    cont = True
    while(len(toBeDone)>0):
        currentState = toBeDone.pop()
        done.append(currentState)
        table["states"].append(currentState)
        for a in nfa.alphabet:
            nextState = []
            for s in currentState: 
                for t in nfa.transitions:
                    if t["from"] == s and t['opperand'] == a:
                        nextState.append(t['to'])
            if(len(nextState)>0):       
                nextState = getClosure(nfa.transitions, nextState, nextState)
                table[a].append(nextState)
                if(not nextState in done and not nextState in toBeDone):
                    toBeDone.append(nextState)
            else:
                table[a].append(["DEAD"])
            done.append(currentState)    
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    idx = 0
    rename = {}
    transitions = []
    acceptStates = []
    for state in table["states"]:
        if(''.join(state) == "DEAD"):
            rename[''.join(state)] = "DEAD"
        else :
            rename[''.join(state)] = letters[idx]
        idx = idx + 1
        for s in state:
            if s in nfa.final_state and not state in acceptStates:
                acceptStates.append(rename[''.join(state)])
    idx = 0
    for state in table["states"]:
        for a in nfa.alphabet:
            transitions.append({"from": rename[''.join(state)], "opperand": a, "to": rename[''.join(table[a][idx])]})
        idx = idx + 1
    output_file = open('task_2_2_result.txt', "w+")
    output_file.write(','.join(rename.values()))
    output_file.write("\n")
    output_file.write(','.join(nfa.alphabet))
    output_file.write("\n")
    output_file.write(rename[''.join(start)])
    output_file.write("\n")
    output_file.write(','.join(acceptStates))
    output_file.write("\n")
    transitionToString = '('+transitions[0]['from']+' ,'+transitions[0]['opperand']+' ,'+transitions[0]['to']+')'
    transitions.remove(transitions[0])
    for t in transitions:
        transitionToString = transitionToString + ', ('+t['from']+' ,'+t['opperand']+' ,'+t['to']+')'   
    output_file.write(transitionToString)