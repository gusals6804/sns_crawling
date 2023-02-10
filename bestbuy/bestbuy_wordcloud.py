from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import nltk
import re
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

pos_list = ['RB']
pos_name = 'RB_all_words'
top_count = 100

# nltk package download
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

# read data
text_df = pd.read_csv('./best_buy_result/best_buy_washtower.csv', encoding='cp949')

# Review
# text = text_df['Review']
# text = list(text)
# print(text)

# Review_title + Review
text = []
for i in range(len(text_df)):
    text.append(str(text_df['Review_title'][i]) + str(text_df['Review'][i]))
print(text)

# data preprocessing
pos_words = []
for i in range(len(text)):
    # Eliminate unnecessary symbols
    text[i] = re.sub(r'[^\w\d\s]', '', text[i])  # each sentence
    # change lower case
    text[i] = text[i].lower()

    # Word tokenization
    word_tokens = nltk.word_tokenize(text[i])
    # POS tagging
    tokens_pos = nltk.pos_tag(word_tokens)
    for word, pos in tokens_pos:
        if pos in pos_list:
            pos_words.append(word)
            print(word, pos)
print(pos_words, 'pos_words')

# Lemmatization
wlem = nltk.WordNetLemmatizer()
lemmatized_words = []
for word in pos_words:
    new_word = wlem.lemmatize(word)
    lemmatized_words.append(new_word)
print(lemmatized_words, 'lemmatized_words')

# Stopwords removal(1)
stopwords_list = stopwords.words('english')  # nltk stopwords
# print('stopwords: ', stopwords_list)
unique_NN_words = set(lemmatized_words)
final_NN_words = lemmatized_words

for word in unique_NN_words:
    if word in stopwords_list:
        while word in final_NN_words:
            final_NN_words.remove(word)
print(final_NN_words, 'final_NN_words1')

# Stopwords removal(2)
# Define stopwords
# 너무 많아지면 txt 파일로 만들기
# customized_stopwords = ['washer', 'dryer', 'machine', 'washtower', 'laundry', 'product', 'lg', 'washerdryer', 'buy',
#                         'it', 'i', 'unit', 'really', 'also', 'much', 'absolutely', 'best', 'thus', 'im', 'else', 'dont',
#                         'instead', 'sometimes', 'still', 'even', 'usually', 'maybe', 'away', 'le', 'fpr', 'never',
#                         'unfortunately', 'dont', 'far', 'yet', 'bit', 'reluctantly', 'noisy', 'itabsolutely', 'recently',
#                         'probably', 'initially', 'ago', 'ever', 'otherwise', 'however', 'therefore', 'rather', 'barely',
#                         'user', 'need', 'lint', 'intermittently', 'dryer', 'absolutely', 'around', 'towerrellay',
#                         'especially', 'well', 'didnt', 'definitely', 'mainly', 'pretty', 'completely', 'occasionally',
#                         'mostly', 'dryerabsolutely', 'relatively', 'back', 'already', 'extremely', 'actually', 'totally',
#                         'apparently', 'importantly', 'nearly', 'towerreally', 'literally', 'along', 'alone', 'isnt', 'side', 'weve',
#                         'washtowerabsolutely', 'lateri', 'ironically', 'noisyvery', 'anyway', 'cloth', 'anyway', 'incorrectly', 'loudly', 'greattruly']
#
# unique_NN_words1 = set(final_NN_words)
# for word in unique_NN_words1:
#     if word in customized_stopwords:
#         while word in final_NN_words:
#             final_NN_words.remove(word)
# print(final_NN_words, 'final_NN_words2')


# top_count word save
counts = Counter(final_NN_words)
top_count = len(final_NN_words)
tags = counts.most_common(top_count)
print(tags)
print(len(final_NN_words))

counts = []
words = []
ratio_list = []
for word, count in tags:
    words.append(word)
    counts.append(count)
    ratio_list.append(round((count/len(final_NN_words))*100, 2))

count_dict = {
    "word": words,
    "count": counts,
    "ratio": ratio_list
}

word_count_df = pd.DataFrame(count_dict)
word_count_df.to_csv('./best_buy_result/word_count_%s.csv' % pos_name)

# WordCloud
FONT_PATH = 'C:/Windows/Fonts/malgun.ttf'

# noun_text = ''
# for word in final_NN_words:
#     noun_text = noun_text + ' ' + word
# wordcloud = WordCloud(max_font_size=60,  width=400, height=400, relative_scaling=.5, font_path=FONT_PATH).generate(noun_text) # generate() 는 하나의 string value를 입력 받음
wc = WordCloud(font_path=FONT_PATH, max_font_size=150,  width=1000, height=1000, relative_scaling=.5,)
cloud = wc.generate_from_frequencies(dict(tags))

# WordCloud plt
plt.figure()
plt.imshow(cloud, interpolation='bilinear')
plt.axis("off"), plt.xticks([]), plt.yticks([])
plt.tight_layout()
plt.savefig('./best_buy_result/%s' % pos_name)
plt.show()