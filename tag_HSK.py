# When input a paragraph of Chinese sentence, output it with HSK level on each word

print("Input some Chinese text:")
text=input()
# text='一家人在吃饭。 儿子问：“爸爸，虫子能吃吗？” 爸爸说：“儿子， 妈妈做的饭菜好吃吗？” 儿子说：“很好吃！” 爸爸说：“那么，你好好吃饭。 吃饭的时候，不要说话。好吗？” 儿子说：“好的。”'
# text='在一个商店,他看到一只小猫,对不起,大家到了清华大学'
# print(text)
# ==============================

# !pip install wget termcolor jieba
import json
import termcolor
import jieba
import wget
from pathlib import Path
import shutil
import os.path


# check if the HSK files exist  
Path("./assets").mkdir(parents=True, exist_ok=True)
if not os.path.exists('assets/hsk-level-1.json'):
    wget.download('https://raw.githubusercontent.com/simon2016bht/TagHskWords/master/assets/hsk-level-1.json')
    shutil.move('./hsk-level-1.json', 'assets/hsk-level-1.json')
if not os.path.exists('assets/hsk-level-2.json'):
    wget.download('https://raw.githubusercontent.com/simon2016bht/TagHskWords/master/assets/hsk-level-2.json')
    shutil.move('./hsk-level-2.json', 'assets/hsk-level-2.json')
if not os.path.exists('assets/hsk-level-3.json'):
    wget.download('https://raw.githubusercontent.com/simon2016bht/TagHskWords/master/assets/hsk-level-3.json')
    shutil.move('./hsk-level-3.json', 'assets/hsk-level-3.json')




# load file contents into lists
with open('assets/hsk-level-1.json') as file:
    hsk1_data = json.load(file)
hsk1_words = []
for item in hsk1_data:
    hsk1_words.append(item['hanzi'])

with open('assets/hsk-level-2.json') as file:
    hsk2_data = json.load(file)
hsk2_words = []
for item in hsk2_data:
    hsk2_words.append(item['hanzi'])

with open('assets/hsk-level-3.json') as file:
    hsk3_data = json.load(file)
hsk3_words = []
for item in hsk3_data:
    hsk3_words.append(item['hanzi'])

# =================================

# tag words which is of HSK 1,2,3
tagged_words_hsk1=[]
tagged_words_hsk2=[]
tagged_words_hsk3=[]

# using jieba for word segmentation
for word in jieba.cut(text, cut_all=False):
    #cut word in small pieces
#     print(word,len(word))
    # for each word output from jieba, check the subset of it
    subset_of_word=[]
    if len(word) >= 4:
#         print(word,4)
        subset_of_word.append(word[0])
        subset_of_word.append(word[1])
        subset_of_word.append(word[2])
        subset_of_word.append(word[3])
        subset_of_word.append(word[0:2])
        subset_of_word.append(word[1:3])
        subset_of_word.append(word[2:4])
        subset_of_word.append(word[0:3])
        subset_of_word.append(word[1:4])
    elif len(word) >= 3:
#         print(word,3)
        subset_of_word.append(word[0])
        subset_of_word.append(word[1])
        subset_of_word.append(word[2])
        subset_of_word.append(word[0:2])
        subset_of_word.append(word[1:3])
    elif len(word)>=2:
#         print(word,2)
        subset_of_word.append(word[0])
        subset_of_word.append(word[1])

# check the word directly from jieba    
    if word in hsk1_words and word not in tagged_words_hsk1:
        tagged_words_hsk1.append(word)
    elif word in hsk2_words and word not in tagged_words_hsk2:
        tagged_words_hsk2.append(word)
    elif word in hsk3_words and word not in tagged_words_hsk3:
        tagged_words_hsk3.append(word)
    
    
# also check subset of the word 
    for i in subset_of_word:
#         print(i)
        if i in hsk1_words and i not in tagged_words_hsk1:
            tagged_words_hsk1.append(i)
        if i in hsk2_words and i not in tagged_words_hsk2:
            tagged_words_hsk2.append(i)
        if i in hsk3_words and i not in tagged_words_hsk3:
            tagged_words_hsk3.append(i)
# print("=======================")
# print("HSK1:",tagged_words_hsk1)
# print("HSK2:",tagged_words_hsk2)
# print("HSK3:",tagged_words_hsk3)

# ====================================


# Create list of flags for each HSK level

# initialize flag as list of 0
hsk1_flag=[0]*len(text)
hsk2_flag=[0]*len(text)
hsk3_flag=[0]*len(text)


## flag a slice of list according to the length of the HSK word
def tag(flag_list_name,starting_position, length, hsk_level):
    for i in range(length):
        flag_list_name[starting_position+i]=hsk_level
        None

# going through the text
for cursor_position in enumerate(text):
    # test word from one syllable to 4 syllables, flag of longer word will override short word in the same level
    window=text[cursor_position[0]:cursor_position[0]+4]
    # check if the word size is as expected; avoid out of range problems at the end of the text
    if len(window) != 4:
        None
    elif window in tagged_words_hsk1:
        tag(hsk1_flag,cursor_position[0],4,1)
    elif window in tagged_words_hsk2:
        tag(hsk2_flag,cursor_position[0],4,2)
    elif window in tagged_words_hsk3:
        tag(hsk3_flag,cursor_position[0],4,3)
        
    window=text[cursor_position[0]:cursor_position[0]+3]        
    if len(window) != 3:
        None    
    elif window in tagged_words_hsk1:
#         print(window) 
        tag(hsk1_flag,cursor_position[0],3,1)
    elif window in tagged_words_hsk2:
        tag(hsk2_flag,cursor_position[0],3,2)
    elif window in tagged_words_hsk3:
        tag(hsk3_flag,cursor_position[0],3,3)

    window=text[cursor_position[0]:cursor_position[0]+2]
    if len(window) != 2:
        None
    elif window in tagged_words_hsk1:
#         print(window) 
        tag(hsk1_flag,cursor_position[0],2,1)
    elif window in tagged_words_hsk2:
        tag(hsk2_flag,cursor_position[0],2,2)
    elif window in tagged_words_hsk3:
        tag(hsk3_flag,cursor_position[0],2,3)

    window=text[cursor_position[0]:cursor_position[0]+1]    
    if window in tagged_words_hsk1:
        tag(hsk1_flag,cursor_position[0],1,1)
    elif window in tagged_words_hsk2:
        tag(hsk2_flag,cursor_position[0],1,2)
    elif window in tagged_words_hsk3:
        tag(hsk3_flag,cursor_position[0],1,3)


# # check tagging result for each HSK level
# for i in enumerate(text):
#     print(i[0],text[i[0]],hsk1_flag[i[0]], hsk2_flag[i[0]], hsk3_flag[i[0]])


# ======================================

## combine flags and assign font color and background color to each character
# Available text colors: red, green, yellow, blue, magenta, cyan, white.
HSK1_color = 'red'
HSK2_color = 'green'
HSK3_color = 'yellow'

combined_flag = []
for i in enumerate(text):
    d = {'character':text[i[0]],'font_color':None, 'bg_color':None}
    combined_flag.append(d)

for (cursor_position,character) in enumerate(text):
#     print(cursor_position, character,hsk1_flag[cursor_position])
    if hsk1_flag[cursor_position] != 0:
        combined_flag[cursor_position]['font_color'] = HSK1_color
    # for higher HSK level word, first check if it is already tagged. If so, using background color.
    if hsk2_flag[cursor_position] != 0:
        if combined_flag[cursor_position]['font_color'] == None:
            combined_flag[cursor_position]['font_color'] = HSK2_color
        elif combined_flag[cursor_position]['bg_color'] == None:
            combined_flag[cursor_position]['bg_color'] = 'on_' + HSK2_color

    if hsk3_flag[cursor_position] != 0:
        if combined_flag[cursor_position]['font_color'] == None:
            combined_flag[cursor_position]['font_color'] = HSK3_color
        elif combined_flag[cursor_position]['bg_color'] == None:
            combined_flag[cursor_position]['bg_color'] = 'on_' + HSK3_color
    
# =======================================


# output text according to the combined flag
print("Colored text (red for HSK1, green for HSK2, yellow for HSK3):\n---")
for i in enumerate(text):
#     print(i,combined_flag[i[0]]['font_color'], combined_flag[i[0]]['bg_color'])
    colored_word = termcolor.colored(i[1], color=combined_flag[i[0]]['font_color'], on_color=combined_flag[i[0]]['bg_color'])
    print(colored_word, end="")
print("\n---")
print('HSK3 words:', tagged_words_hsk3)
print('HSK2 words:', tagged_words_hsk2)
print('HSK1 words:', tagged_words_hsk1)

## END
