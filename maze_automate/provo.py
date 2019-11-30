'''Reads the input file of the cleaned provo dataset csv'''
import csv
item_to_info = {}
with open("provo.csv", 'r') as tsv:
    f = csv.reader(tsv, delimiter=",", quotechar='"')
    for row in f:
        if row[0] == "Text_ID":
            continue
        if row[0] in item_to_info:  # text_id already seen
            if row[1] in item_to_info[row[0]][0]: #sentence_id already seen, skipping
                continue
            item_to_info[row[0]][0].append(row[1])  # condition generated as sentence_id
            item_to_info[row[0]][1].append(row[5].strip())  # add sentence to the list
            item_to_info[row[0]][2].append([i for i in range(len(row[5].strip().split()))])
        else:
            item_to_info[row[0]] = [[row[1]], [row[5].strip()]]  # new item num, add a new entry
            item_to_info[row[0]].append([[i for i in range(len(row[5].strip().split()))]])
'''Deals with sentences with semicolons in them, that would mess up the parsing'''
for info in item_to_info.values():
    for i in range(len(info[1])):
        for j in range(len(info[1][i])):
            if info[1][i][j] == ';':
                info[1][i] = info[1][i][:j] + ':' + info[1][i][j+1:]
                print(info[1][i])

'''Saves results to a file in semicolon delimited format, basically same as the original input'''
with open("provo_input.txt", 'w') as f:
    for key in item_to_info:
        for i in range(len(item_to_info[key][1])):
            f.write('"'+item_to_info[key][0][i]+'";')
            f.write(''+key+';')
            f.write(''+item_to_info[key][1][i]+';')
            f.write(''+" ".join([str(id) for id in item_to_info[key][2][i]])+'\n')