import re
import matplotlib.pyplot as plt

final_words = []
stopwords = []
regex = re.compile("([A-Z]\.)([A-Z]\.)+", re.IGNORECASE)

def process_word(cur_word):
    cur_word = cur_word.lower()
    if cur_word not in stopwords: # check if word is in stopword list
        if cur_word.endswith("sses"): #  Begin step 1a of porter stemmer
            cur_word = cur_word[:-2]
        if not (cur_word.endswith("ss") or cur_word.endswith("us")):
            if cur_word.endswith("ies") or cur_word.endswith("ied"):
                if len(cur_word) > 4:
                    cur_word = cur_word[:-2]
                else:
                    cur_word = cur_word[:-1]
            if len(cur_word) >= 2 and cur_word[len(cur_word)-1] == 's' and cur_word[len(cur_word)-2] not in ('a', 'e', 'i', 'o', 'u'):
                cur_word = cur_word[:-1]
            # end of step 1a for porter stemmer
            # start of step 1b for porter stemmer
        elif cur_word.endswith("eedly") and len(cur_word) > 6:
            cur_word = cur_word[:-3]
        elif cur_word.endswith("eed") and len(cur_word) > 4:
            cur_word = cur_word[:-1]
        elif cur_word.endswith("ingly") and len(cur_word) > 6 and any(char in ('a', 'e', 'i', 'o', 'u') for char in cur_word[0: len(cur_word)-6]):
            cur_word = cur_word[:-5]
            if cur_word.endswith("at") or cur_word.endswith("bl") or cur_word.endswith("iz"):
                cur_word += 'e'
            elif not (cur_word.endswith('ll') or cur_word.endswith('ss') or cur_word.endswith('zz')) and (cur_word[len(cur_word)-1] == cur_word[len(cur_word)-2]):
                cur_word = cur_word[:-1]
            elif not (cur_word.endswith('ll') or cur_word.endswith('ss') or cur_word.endswith('zz')) and len(cur_word) <= 3:
                cur_word += 'e'
        elif cur_word.endswith("edly") and len(cur_word) > 5 and any(char in ('a', 'e', 'i', 'o', 'u') for char in cur_word[0: len(cur_word)-5]):
            cur_word = cur_word[:-4]
            if cur_word.endswith("at") or cur_word.endswith("bl") or cur_word.endswith("iz"):
                cur_word += 'e'
            elif not (cur_word.endswith('ll') or cur_word.endswith('ss') or cur_word.endswith('zz')) and (cur_word[len(cur_word)-1] == cur_word[len(cur_word)-2]):
                cur_word = cur_word[:-1]
            elif not (cur_word.endswith('ll') or cur_word.endswith('ss') or cur_word.endswith('zz')) and len(cur_word) <= 3:
                cur += 'e'
        elif cur_word.endswith("ing") and len(cur_word) > 4 and any(char in ('a', 'e', 'i', 'o', 'u') for char in cur_word[0: len(cur_word)-4]):
            cur_word = cur_word[:-3]
            if cur_word.endswith("at") or cur_word.endswith("bl") or cur_word.endswith("iz"):
                cur_word += 'e'
            elif not (cur_word.endswith('ll') or cur_word.endswith('ss') or cur_word.endswith('zz')) and (cur_word[len(cur_word)-1] == cur_word[len(cur_word)-2]):
                cur_word = cur_word[:-1]
            elif not (cur_word.endswith('ll') or cur_word.endswith('ss') or cur_word.endswith('zz')) and len(cur_word) <= 3:
                cur_word += 'e'
        elif cur_word.endswith("ed") and len(cur_word) > 3 and any(char in ('a', 'e', 'i', 'o', 'u') for char in cur_word[0: len(cur_word)-3]):
            cur_word = cur_word[:-2]
            if cur_word.endswith("at") or cur_word.endswith("bl") or cur_word.endswith("iz"):
                cur_word += 'e'
            elif not (cur_word.endswith('ll') or cur_word.endswith('ss') or cur_word.endswith('zz')) and (cur_word[len(cur_word)-1] == cur_word[len(cur_word)-2]):
                cur_word = cur_word[:-1]
            elif not (cur_word.endswith('ll') or cur_word.endswith('ss') or cur_word.endswith('zz')) and len(cur_word) <= 3:
                cur_word += 'e'
        final_words.append(cur_word)


# add all stop words to stopword list
with open('stopwords.txt') as file: # open the spot words text file
    for line in file:
        if line != "":
            stopwords.append(line.strip())
    file.close()

# have user input name of the file they want tokenized
filename = input("Enter the file you want to be tokenized: ")

with open(filename,'r') as file:
    for line in file:
        for word in line.split(): # go through file line by line
            cur_word = ""
            found = regex.search(word)
            if found:
                abbrev = found.group(0)
                list = word.split(abbrev)
                if list[0] == "" and list[1] == "":
                    cur_word = abbrev.replace('.', '')
                    process_word(cur_word)
                else:
                    if list[0] != "" or list[1] != "":
                        cur_word = abbrev.replace('.', '')
                        process_word(cur_word)
            else:
                for char in word:
                    if char.isalnum():
                        cur_word += char
                    else:
                        if cur_word != "":
                            process_word(cur_word)
                            cur_word = ""
                if cur_word != "":
                    process_word(cur_word)

final_file = open("tokenized.txt", "w")
for word in final_words:
    final_file.write(word + '\n')
final_file.close()

histogram = {}
total_words = 0
unique_words = 0
total_list = [0]
unique_list = [0]

for word in final_words:
    total_words += 1
    total_list.append(total_words)
    if word in histogram:
        histogram[word] += 1
        unique_list.append(unique_words)
    else:
        histogram[word] = 1
        unique_words += 1
        unique_list.append(unique_words)

sorted_words = sorted(histogram, key = histogram.get, reverse = True)
sorted_words = sorted_words[:200]

freq_file = open("terms.txt", "w")
for key in sorted_words:
    freq_file.write(key + ': ' + str(histogram[key]) + '\n')
freq_file.close()

plt.plot(total_list, unique_list)
plt.title("Tokenization Project")
plt.ylabel("Vocabulary size")
plt.xlabel("Total words")
plt.show()
