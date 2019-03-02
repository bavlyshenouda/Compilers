import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?", metavar="file")
    
    args = parser.parse_args()
    gramMap = {}
    resultGram = {}
    with open(args.file, "r") as file:
        lines = file.read()
        lines = lines.split('\n')
    for line in lines:
        line = line.replace(' ','')
        gram = line.split(':')
        gramMap[gram[0]] = gram[1].split('|')
    #print(gramMap)
    for key, values in gramMap.items():
        alpha = []
        beta = []
        for subKey, subValues in resultGram.items():
            if subKey == key:
                break
            else :
                newValues = []
                for exp in values:
                    if exp[0] == subKey :
                        for x in subValues:
                            newValues.append(x + exp[1:])
                    else :
                        newValues.append(exp)
                values = newValues
        for value in values:
            if value[0] == key:
                alpha.append(value[1:])
            else :
                beta.append(value)
        if len(alpha)>0:
            newBeta = []
            for b in beta:
                newBeta.append(' '.join(b+key)+'\'')
            resultGram[key] = newBeta
            newAlpha = []
            for a in alpha:
                newAlpha.append(' '.join(a + key)+'\'')
            newAlpha.append('epsilon')
            resultGram[key+'\''] = newAlpha
        else :
            newVals = []
            for v in values:
                newVals.append(' '.join(v))
            values = newVals
            resultGram[key] = values
    output_file = open('task_4_1_result.txt', "w+")
    for key, value in resultGram.items():
        output_file.write(key + ' : ')
        output_file.write(' | '.join(value))           
        output_file.write('\n')