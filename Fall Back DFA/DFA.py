import argparse

class DFA:

    def __init__(self, file):
        with open(file, "r") as file:
            idx = 1
            lines = file.read()
            lines= lines.split('\n')
            for line in lines:
                if(idx == 1):
                    #states
                    line = line.replace(' ','')
                    temp = line.split(',')
                    map(str.strip, temp)
                    self.states = temp 
                if(idx == 2):
                    #alphabet
                    line = line.replace(' ','')
                    temp = line.split(',')
                    map(str.strip, temp)
                    self.alphabet = temp
                if(idx == 3):
                    #start state
                    self.start_state = line
                if(idx == 4):
                    #final state
                    line = line.replace(' ','')
                    temp = line.split(',')
                    map(str.strip, temp)
                    self.final_state = temp
                if(idx == 5):
                    #transitions
                    line = line.replace(' ', '')
                    temp = line.split('),(')
                    map(str.strip, temp)
                    self.transitions = []
                    for trans in  temp:
                        #print(trans)
                        trans = trans.replace('(', '')
                        trans = trans.replace(')', '')
                        seperated = trans.split(',')
                        self.transitions.append({'from' : seperated[0],'opperand': seperated[1], 'to' : seperated[2]}) 
                if(idx == 6):
                    #state->expresion
                    line = line.replace(' ', '')
                    temp = line.split('),(')
                    self.expMap = {}
                    for ex in temp:
                        ex = ex.replace('(', '')
                        ex = ex.replace(')', '')
                        seperated = ex.split(',')
                        self.expMap[seperated[0]] = seperated[1] 
                if(idx == 7):
                    #expression->output
                    temp = line.split('), (')
                    self.OutputMap = {}
                    for ex in temp:
                        ex = ex.replace('(', '')
                        ex = ex.replace(')', '')
                        seperated = ex.split(', ')
                        self.OutputMap[seperated[0]] = seperated[1]      
                idx = idx+1
                     

        
    
      
