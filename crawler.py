from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sys
# stop word
stopWords = []
segments = ''
with open('stop_words.txt', 'r', encoding='UTF-8') as file:
    for data in file.readlines():
        data = data.strip()
        stopWords.append(data)
argument = sys.argv
print("start to crawler")
#0~50

all_paper = "https://arxiv.org/search/?searchtype=all&query="+argument[1]+"&abstracts=show&size=50&order=&start=0"
html = urlopen(all_paper).read()
soup = BeautifulSoup(html,"html.parser")
target_link = soup.find_all('p','list-title is-inline-block')
target_title = soup.find_all('p','title is-5 mathjax')
target_abstract = soup.find_all('p','abstract-full has-text-grey-dark mathjax')
target_author = soup.find_all('p','authors')
target_text = str()
target_abstract_link = []
for index in range(0,50):
    one_author = target_author[index]
    one_title = target_title[index]
    one_link = target_link[index]
    
    temp_url = ''
    temp_a = one_link('a')[0]
    target_text += temp_a['href']+'\n'
    target_abstract_link.append(temp_a['href'])
    
    temp_title = ''
    one_title.text
    temp_b = one_title.text.lstrip()
    temp_b = temp_b.rstrip()
    target_text += temp_b+'\n'
    
    temp_authors = ''
    for all_authors in one_author.find_all('a'):
        temp_authors = temp_authors+str(all_authors.text)+';'
    target_text +=temp_authors+'\n'

# need add
count = dict()
for index in range(0,50):
    paper_abstract = target_abstract_link[index]
    html_abs = urlopen(paper_abstract).read()
    soup_abs = BeautifulSoup(html_abs,"html.parser")
    get_abstract = soup_abs.find_all('blockquote','abstract mathjax')
    get_abstract = str(get_abstract[0])
    get_abstract = BeautifulSoup(get_abstract,'html.parser')
    get_abstract = get_abstract.find('blockquote', class_='abstract mathjax')
    get_abstract.span.extract()
    temp_abstract = get_abstract.text.lstrip()
    temp_abstract = temp_abstract.rstrip()
    temp_abstract = temp_abstract.lower()
    # delete the Symbol 
    new_str = re.sub('[;~!@#$%^&*><.?]','',temp_abstract)
    abstract_split = new_str.split()
    for word in abstract_split:
        if word in stopWords:
            pass
        elif(word in count):
            count[word] += 1
        else:
            count[word] = 1
print("finish 0~50")
#51~100
all_paper = "https://arxiv.org/search/?searchtype=all&query="+argument[1]+"&abstracts=show&size=50&order=&start=50"
html = urlopen(all_paper).read()
soup = BeautifulSoup(html,"html.parser")
target_link = soup.find_all('p','list-title is-inline-block')
target_title = soup.find_all('p','title is-5 mathjax')
target_abstract = soup.find_all('p','abstract-full has-text-grey-dark mathjax')
target_author = soup.find_all('p','authors')
target_abstract_link = []
for index in range(0,50):
    one_author = target_author[index]
    one_title = target_title[index]
    one_link = target_link[index]
    
    temp_url = ''
    temp_a = one_link('a')[0]
    target_text += temp_a['href']+'\n'
    target_abstract_link.append(temp_a['href'])
    
    temp_title = ''
    one_title.text
    temp_b = one_title.text.lstrip()
    temp_b = temp_b.rstrip()
    target_text += temp_b+'\n'
    
    temp_authors = ''
    for all_authors in one_author.find_all('a'):
        temp_authors = temp_authors+str(all_authors.text)+';'
    target_text +=temp_authors+'\n'

# need add
for index in range(0,50):
    paper_abstract = target_abstract_link[index]
    html_abs = urlopen(paper_abstract).read()
    soup_abs = BeautifulSoup(html_abs,"html.parser")
    get_abstract = soup_abs.find_all('blockquote','abstract mathjax')
    get_abstract = str(get_abstract[0])
    get_abstract = BeautifulSoup(get_abstract,'html.parser')
    get_abstract = get_abstract.find('blockquote', class_='abstract mathjax')
    get_abstract.span.extract()
    temp_abstract = get_abstract.text.lstrip()
    temp_abstract = temp_abstract.rstrip()
    temp_abstract = temp_abstract.lower()
    # delete the Symbol 
    new_str = re.sub('[;~!@#$%^&*><.?]','',temp_abstract)
    abstract_split = new_str.split()
    for word in abstract_split:
        if word in stopWords:
            pass
        elif(word in count):
            count[word] += 1
        else:
            count[word] = 1
print("finish 51~100")
sorted_count = [(wd, count[wd]) for wd in sorted(count, key=count.get, reverse=True)]
#writing data for paper info
target_text = target_text.encode(encoding="utf-8")
with open("paper_info.txt",'wb') as f:
    f.write(target_text)

#writing data for frequent word
with open("frequent_word.txt",'wb') as f:
    for index in range(0,50):
        temp_0 = sorted_count[index][0].encode(encoding="utf-8")
        temp_1 = str(sorted_count[index][1]).encode(encoding="utf-8")
        f.write(temp_0+b' '+temp_1+b'\n')
print("done")
