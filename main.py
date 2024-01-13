import requests
import re
from bs4 import BeautifulSoup
from collections import Counter

page = "Microsoft"
section = "History"
url = 'https://en.wikipedia.org/w/api.php'

params = {
            'action': 'parse',
            'page': page,
            'format': 'json',
            'prop':'sections',
            'redirects':''
        }

response = requests.get(url, params)
data = response.json()
sectionIndex = 0
for sec in data['parse']['sections']:
    if sec['line'] == section:
        sectionIndex = sec['index']

params = {
            'action': 'parse',
            'page': page,
            'format': 'json',
            'prop':'text',
            'section': sectionIndex,
            'redirects':''
        }

response = requests.get(url, params)
data = response.json()
raw_html = data['parse']['text']['*']
soup = BeautifulSoup(raw_html,'html.parser')

wordlist = []
for items in soup.select("span.mw-headline, p, figcaption"):
    content = items.text
    words = re.sub("[^\w]", " ",  content).split()
    wordlist += words

word_count = {}
for word in wordlist:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1
c = Counter(word_count)
top = c.most_common(10)
print(top)

