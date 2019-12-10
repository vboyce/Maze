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
            item_to_info[row[0]][1].append(row[5].strip().split(" "))  # add sentence to the list
            item_to_info[row[0]][2].append(row[5].strip())
        else:
            item_to_info[row[0]] = [[row[1]], [row[5].strip().split(" ")], [row[5].strip()]]  # new item num, add a new entry
        print(item_to_info[row[0]][2])

'''Reads the provo_log file and matches the positions with the words and the information'''
from helper_new import strip_punct
line = 0
id = 0
data = []
with open("provo_log2.txt", 'r') as log:
    for row in log:
        line += 1
        if line <= 3:
            continue
        if row[0] == '[':
            continue
        data.append(row.strip().split(" "))
line = 0
print(len(item_to_info))
item_to_freq = [[]]*(len(item_to_info) + 1)
item_to_surprisal = [[]]*(len(item_to_info) + 1)
print(item_to_freq)
ids = [str(i) for i in range(1, 56)]
for strid in sorted(ids):
    id = int(strid)
    item_to_freq[id] = [[] for i in range(len(item_to_info[str(id)][0]))]
    item_to_surprisal[id] = [[] for i in range(len(item_to_info[str(id)][0]))]
    # for each sentence set
    for j in range(100):
        # for each word index in sentence (up to 100, which should be more than any sentence length)
        for i in range(len(item_to_info[str(id)][0])):
            # for each sentence in sentence set
            if j >= len(item_to_info[str(id)][1][i]):
                continue
            (word, _, _, _) = strip_punct(item_to_info[str(id)][1][i][j])
            # print(id, j, i, word, data[line])
            if data[line][0] == word and len(data[line][1]) > 5:
                # data should be "word surprisal"
                item_to_surprisal[id][i].append(data[line][1])
                line += 1
            else:
                item_to_surprisal[id][i].append("")
        for i in range(len(item_to_info[str(id)][0])):
            # for each sentence in sentence set
            if j >= len(item_to_info[str(id)][1][i]):
                continue
            (word, _, _, _) = strip_punct(item_to_info[str(id)][1][i][j])
            # print(id, j, i, word, data[line])
            if data[line][0] == word and len(data[line][1]) <= 5:
                # data should be "word freq"
                item_to_freq[id][i].append(data[line][1])
                line += 1
            else:
                item_to_freq[id][i].append("")
    # print(item_to_freq[id])

'''Saves results to a file back to csv format'''
with open("provo_final2.csv", 'w') as f:
    writer = csv.writer(f)
    for sentence_set_id in range(1, len(item_to_info) + 1):
        for sentence_id in range(len(item_to_info[str(sentence_set_id)][1])):
            for word_id in range(len(item_to_info[str(sentence_set_id)][1][sentence_id])):
                row = []
                row.append(sentence_set_id)
                row.append(sentence_id + 1)
                row.append(word_id + 1)
                row.append(item_to_info[str(sentence_set_id)][1][sentence_id][word_id])
                row.append(item_to_info[str(sentence_set_id)][2][sentence_id])
                row.append(item_to_freq[sentence_set_id][sentence_id][word_id])
                row.append(item_to_surprisal[sentence_set_id][sentence_id][word_id])
                writer.writerow(row)
