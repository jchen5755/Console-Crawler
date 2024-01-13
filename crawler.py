import requests
import re
from bs4 import BeautifulSoup
from collections import Counter

def countWords(wordlist):
    word_count = {}
    for word in wordlist:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return Counter(word_count)

def createWordList(soup, excludeWordsList):
    wordlist = []
    pattern = "|".join(excludeWordsList)
    for items in soup.select("span.mw-headline, p, figcaption"):
        content = items.text
        words = re.sub(pattern, " ",  content).split()
        wordlist += words
    return wordlist
        
def wikiApiJson(url, page = "Microsoft", section = None):
    params = {
        'action': 'parse',
        'page': page,
        'format': 'json',
        'redirects':''
    }
    
    if section:
        params['prop'] = 'text'
        params['section'] = section
    else:
        params['prop'] = 'sections'
    
    return requests.get(url, params).json()

def main():
    page = "Microsoft"
    section = "History"
    url = 'https://en.wikipedia.org/w/api.php'
    excludeWordsList = ["[^a-zA-Z0-9'-]"]
    wordsToPrint = 10
        
    wordsToPrintInput = input("Enter the number of words you wish to return (default: 10): ") 
    if (type(wordsToPrintInput) == type(wordsToPrint)):
        wordsToPrint = wordsToPrintInput
    
    excludeWordsInput = input("Enter the words you wish to exclude separated by space (default: none): ")
    excludeWordsList += re.sub("[^a-zA-Z0-9'-]", " ", excludeWordsInput).split()
    
    pageData = wikiApiJson(url, page)
    sectionIndex = 0
    for sec in pageData['parse']['sections']:
        if sec['line'] == section:
            sectionIndex = sec['index']
    
    sectionData = wikiApiJson(url, page, sectionIndex)
    sectionHtml = sectionData['parse']['text']['*']
    soup = BeautifulSoup(sectionHtml,'html.parser')
    
    wordlist = createWordList(soup, excludeWordsList)
    countedWordList = countWords(wordlist)
    print(countedWordList.most_common(wordsToPrint))
    input("Press Enter to close window.")
    
if __name__ == "__main__":
    main()