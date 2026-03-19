from collections import defaultdict
import pymorphy2
import re


morph = pymorphy2.MorphAnalyzer()
WORD_RE = re.compile(r"[а-яА-Яa-zA-Z]+")


class TextAnalyzer:
    def __init__(self):
        self.global_count = defaultdict(int)
        self.line_counts = defaultdict(dict)

    def normalize(self, word: str) -> str:
        return morph.parse(word)[0].normal_form

    def process_line(self, line: str, line_index: int):
        words = WORD_RE.findall(line.lower())

        local_counter = defaultdict(int)

        for word in words:
            lemma = self.normalize(word)
            local_counter[lemma] += 1

        for lemma, count in local_counter.items():
            self.global_count[lemma] += count
            self.line_counts[lemma][line_index] = count