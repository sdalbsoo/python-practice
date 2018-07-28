import re
from abc import abstractmethod
from bs4 import BeautifulSoup

import requests

import constants


class SubtitleParser():
    def __init__(self):
        self.meaning_words = DictParser()  # meaning_words가 DictParser를 가진다.
        with open(constants.PATH_STOPWORDS, "r") as f:
            self.stopwords = set(f.read().splitlines())

    def remove_tag(self, text):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', text)
        return clean_text
        # regex = f"<{tag}>(.*?)</{tag}>"
        # matches = re.finditer(regex, text, re.MULTILINE)
        # match = list(matches)[0]
        # assert len(match.groups()) == 1
        # return match.groups()[0]

    @abstractmethod
    def extract_sentences(self):
        pass

    @abstractmethod
    def extract_word(self):
        pass


class SrtParser(SubtitleParser):
    def __init__(self, srt_path):
        super(SrtParser, self).__init__()
        with open(srt_path, 'r') as f:
            replace_words = [
                ',', '.', '!', '?'
            ]
            content = f.read()
            for replace_word in replace_words:
                content.replace(replace_word, '')
            self.lines = content.lower().splitlines()

    def extract_sentences(self):
        sentences = []
        for line in self.lines:
            if line.isdigit():
                continue
            if '-->' in line:
                continue
            if len(line) == 0:
                continue
            line = self.remove_tag(line)
            sentences.append(line)
        return sentences

    def extract_words(self, sentences):
        words = {}
        for sentence in sentences:
            for word in sentence.split(' '):
                if word not in self.stopwords:
                    words[word] = words.get(word, 0) + 1
        return words


class SmiParser(SubtitleParser):
    def __init__(self):
        pass

    def extract_sentences(self):
        pass

    def extract_words(self):
        pass


class DictParser():
    def searchdict(extracted_words):
        meaning_words = {}
        for i, word in enumerate(extracted_words):
            daum_url = 'http://alldic.daum.net/search.do?q={}'
            search_url = daum_url.format(word)
            temp = []
            response = requests.get(search_url)
            source = response.text
            soup = BeautifulSoup(source, 'lxml')
            parsed = soup.find_all('span', class_='txt_search', limit=3)
            for j in range(3):
                try:
                    if parsed[j].string is None:
                        continue
                    temp.append(parsed[j].string)
                except IndexError:
                    continue
            meaning_words[word] = meaning_words.get(word, temp)
        return meaning_words

    def remove_tag(text):
        cleaner = re.compile('<.*?>')
        clean_text = re.sub(cleaner, '', text)
        return clean_text


def main():
    srt_path = "../data/srt/lionking.srt"
    srt = SrtParser(srt_path)
    sentences = srt.extract_sentences()
    extracted_words = srt.extract_words(sentences)
    print(extracted_words)
    meanings = DictParser.searchdict(extracted_words)
    print(meanings)


if __name__ == '__main__':
    main()
