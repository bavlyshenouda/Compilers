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
    for key, values in gramMap.items():
        while(True):
            countDic = {}
            mx = {"key" : "", "count" : 0}
            for term in values:
                if term == "epsilon":
                    continue
                elif term[0] in countDic.keys():
                    countDic[term[0]] = countDic[term[0]] + 1
                else :
                    countDic[term[0]] = 1
                if(mx["count"] < countDic[term[0]]):
                    mx['key'] = term[0]
                    mx['count'] = countDic[term[0]]
            if mx['count'] <= 1:
                resultGram[key] = values
                break
            newValues = []
            dashValues = []
            for term in values:
                if term[0] == mx['key'] and len(term) > 1:
                    dashValues.append(term[1:])
                elif term[0] != mx['key']:
                    newValues.append(term)
            newValues.append(mx['key']+key+'\'')
            resultGram[key] = newValues
            key = key+'\''
            values = dashValues
    print(resultGram.items())
    output_file = open('task_4_2_result.txt', "w+")
    for key, value in resultGram.items():
        output_file.write(key + ' : ')
        output_file.write(' | '.join(value))           
        output_file.write('\n')

    