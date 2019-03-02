from copy import deepcopy
import argparse
#to form Stack Class
class StackClass:

    def __init__(self, itemlist=[]):
        self.items = itemlist

    def isEmpty(self):
        if self.items == []:
            return True
        else:
            return False

    def peek(self):
        return self.items[-1:][0]

    def pop(self):
        return self.items.pop()

    def push(self, item):
        self.items.append(item)
        return 0

class HelperClass:

    
    def concatEpsAdder(self, rgex):
        #add concationation .
        st = StackClass()
        rgex = rgex.replace("ε", " ")
        for e in rgex:
            if(st.isEmpty()):
                st.push(e)
            elif e in "0123456789qwertyuiopasdfghjklzxcvbnm ":
                if not st.peek() in "|(" :
                    st.push('.')
                st.push(e)
            elif e in "+*?|)" :
                st.push(e)   
            elif e == '(':
                if not st.peek() in "|(" :
                    st.push('.')
                st.push(e)
        result = ""
        while(not st.isEmpty()) :
            result = st.pop() + result
        return result
    
    def getPostFix(self, rgex):
        postfix=""
        stk = StackClass()
        prec={
            '(': 1,
            '*': 2,
            '?': 2,
            '+': 2,
            '.': 3,
            '|': 4, 
        }
        for e in rgex:
            #If the incoming symbols is an operand, print it.
            if e in "0123456789qwertyuiopasdfghjklzxcvbnm ":
                postfix+=e
            #If the incoming symbol is a left parenthesis, push it on the stack.    
            elif e == '(':
                stk.push(e)
            #If the incoming symbol is a right parenthesis: 
            # discard the right parenthesis, pop and print the stack symbols until you see a left parenthesis. Pop the left parenthesis and discard it.
            elif e == ')':
                while (stk.peek()!='('): 
                    postfix+=stk.pop()
                stk.pop()
            #If the incoming symbol is an operator and the stack is empty or contains a left parenthesis on top, push the incoming operator onto the stack.
            elif (e in "|+*?.^" and (stk.isEmpty() or stk.peek() == '(')):
                stk.push(e)
            #If the incoming symbol is an operator and has either higher precedence than the operator on the top of the stack, 
            #or has the same precedence as the operator on the top of the stack and is right associative -- push it on the stack.
            elif (e in "|+*?.^" and prec[e]<prec[stk.peek()]):
                stk.push(e)
            #If the incoming symbol is an operator and has either lower precedence than the operator on the top of the stack, 
            #or has the same precedence as the operator on the top of the stack and is left associative -- continue to pop the stack until this is not true. Then, push the incoming operator.
            elif (e in "|+*?.^" and prec[e]>=prec[stk.peek()]):
                while(not stk.isEmpty() and prec[e]>=prec[stk.peek()] and stk.peek() != '('):
                    postfix+=stk.pop()
                stk.push(e)
        #At the end of the expression, pop and print all operators on the stack.
        while(not stk.isEmpty()):
            postfix+=stk.pop()
        return postfix

    def NFAGen(self, postfix):
        stk = StackClass()
        for e in postfix:
            if e in "0123456789qwertyuiopasdfghjklzxcvbnm ":
                newNFA = NFA(opperand = e)
                stk.push(newNFA)
            elif e == "*":
                nfa = stk.pop()
                nfa = nfa.Kleene()
                stk.push(nfa)
            elif e == "+":
                nfa = stk.pop()
                nfa = nfa.plus()
                stk.push(nfa)
            elif e == "?":
                nfa = stk.pop()
                nfa = nfa.questionMark()
                stk.push(nfa)
            elif e == ".":
                snd = stk.pop()
                fst = stk.pop()
                nfa = fst.concat(snd)
                stk.push(nfa)
            elif e == "|":
                snd = stk.pop()
                fst = stk.pop()
                nfa = fst.union(snd)
                stk.push(nfa)
            else:
                print("error "+e)
        if len(stk.items)>1:
            print("More than one NFA left in stack")
        return stk.pop()

class NFA:
    counter = 0

    def __init__(self, opperand):
        self.intial_state = 'q'+ str(NFA.counter)
        NFA.counter = NFA.counter+1
        self.final_state = 'q'+ str(NFA.counter)
        NFA.counter = NFA.counter+1
        self.transitions = [{'from':self.intial_state, 'opperand': opperand, 'to': self.final_state}]
        self.states = [self.intial_state, self.final_state]
        self.alphabet = [opperand]
        
    
    def concat(self, newNFA):
        transitionsWithStart = []
        for trans in newNFA.transitions:
            if trans["from"] == newNFA.intial_state:
                transitionsWithStart.append(trans)
        for trans in transitionsWithStart:
            trans["from"] = self.final_state
            self.transitions.append(trans)
            newNFA.transitions.remove(trans)
        newNFA.states.remove(newNFA.intial_state)
        self.transitions.extend(newNFA.transitions)
        self.states.extend(newNFA.states)
        self.final_state = newNFA.final_state
        for e in newNFA.alphabet:
            if not e in self.alphabet:
                self.alphabet.append(e)
        return self
    

    def union(self, newNFA):
        newStart = 'q'+str(NFA.counter)
        NFA.counter = NFA.counter +1
        newFinal = 'q'+str(NFA.counter)
        NFA.counter = NFA.counter +1
        self.transitions.append({"from" : newStart, 'opperand' : " ", "to": self.intial_state})
        newNFA.transitions.append({"from" : newStart, 'opperand' : " ", "to": newNFA.intial_state})
        self.transitions.append({"from" : self.final_state, 'opperand' : " ", "to": newFinal})
        newNFA.transitions.append({"from" : newNFA.final_state, 'opperand' : " ", "to": newFinal})
        self.transitions.extend(newNFA.transitions)
        self.states.extend(newNFA.states)
        self.states.append(newStart)
        self.states.append(newFinal)
        self.intial_state = newStart
        self.final_state = newFinal
        for e in newNFA.alphabet:
            if not e in self.alphabet:
                self.alphabet.append(e)
        return self
    
    def Kleene(self):
        newStart = 'q'+ str(NFA.counter)
        NFA.counter = NFA.counter +1
        newFinal = 'q'+str(NFA.counter)
        NFA.counter = NFA.counter +1
        self.transitions.append({"from" : self.final_state, 'opperand' : " ", "to": self.intial_state})
        self.transitions.append({"from" : newStart, 'opperand' : " ", "to": self.intial_state })
        self.transitions.append({"from" : newStart, 'opperand' : " ", "to": newFinal })
        self.transitions.append({"from" : self.final_state, 'opperand' : " ", "to": newFinal })
        self.intial_state = newStart
        self.final_state = newFinal
        self.states.append(newStart)
        self.states.append(newFinal)
        return self

    
    def plus(self):
        #slef.self*
        newNFA = deepcopy(self)
        newNFA = newNFA.Kleene()
        self = self.concat(newNFA)
        return self

    def questionMark(self):
        #self|eps
        newNFA = NFA(opperand = " ")
        self = self.union(newNFA)
        return self

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")
    args = parser.parse_args()
    output_file = open('task_2_result.txt', "w+")
    with open(args.file, "r") as file:
            for line in file:
                re = line
                helper = HelperClass()
                re = helper.concatEpsAdder(re)
                postfix = helper.getPostFix(rgex = re)
                print(re)
                nfa = helper.NFAGen(postfix)
                for e in nfa.states:
                    output_file.write(e+", ")
                output_file.write("\n")
                for e in nfa.alphabet:
                    output_file.write(e+", ")
                output_file.write("\n")
                output_file.write(nfa.intial_state+"\n")
                output_file.write(nfa.final_state+"\n")
                for e in nfa.transitions:
                    output_file.write("("+e["from"]+", "+ e["opperand"]+", ["+e["to"]+"]), ")
    
