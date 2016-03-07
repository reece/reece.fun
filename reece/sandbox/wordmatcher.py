"""class that's useful for playing with anagrams, crosswords, and other word games

wget -nd http://iweb.dl.sourceforge.net/project/wordlist/speller/2016.01.19/hunspell-en_US-2016.01.19.zip
unzip hunspell-en_US-2016.01.19.zip
unmunch en_US.dic en_US.aff | perl -ne 'print unless m/\d|^[A-Z]|\x27s$|^[A-Z]+s?$|^\w$/' | sort -u | gzip >|words.txt.gz

"""

import collections
import gzip
import itertools
import re

class WordKey(str):
    """class representing a canonicalized form ("key") of the letters of a
    word and providing operations on these keys that are useful for
    anagrams and crosswords.

    For a given word w, a universe U of words, and a word u ∈ U, there
    are three comparisons relevant for anagrams and crosswords:

    * w is an anagram of u if WordKey(w) == WordKey(u) (and w ≠ u)
    * w is spellable with u if WordKey(w) <= WordKey(u) (and w ≠ u)

    """

    def __new__(cls, s):
        return str.__new__(cls, "".join(sorted(s)))

    def spellable_with(w, u):
        "`w.spellable_with(u)` is True if a word with key w can be spelled with letters in key u"
        if w == u:
            return True
        if any(l not in u for l in w):
            return False
        uc = collections.Counter(u)
        wc = collections.Counter(w)
        return all(wc[l] <= uc[l] for l in wc)



class WordMatcher(object):
    def __init__(self, fn):
        words = [line.decode("UTF-8").strip() for line in gzip.open(fn)]
        key_word = [(WordKey(w), w) for w in words]
        key_word.sort(key=lambda e: e[0])
        self._key_wordlist_map = {k: list(we[1] for we in kwi)
                                  for k, kwi in itertools.groupby(key_word, key=lambda e: e[0])}

    def find_anagrams(self, s):
        s_wk = WordKey(s)
        try:
            return [w for w in self._key_wordlist_map[s_wk] if w != s]
        except KeyError:
            return []

    def find_subwords(self, s):
        "given a set of letters, return a list of words that can be made from it"
        s_wk = WordKey(s)
        subkeys = [k for k in self._key_wordlist_map.keys() if k.spellable_with(s_wk)]
        return (w
                for w in itertools.chain.from_iterable(self._key_wordlist_map[k] for k in subkeys)
                if w != s)

    def find_subwords_for_pattern(self, letters, pattern, min_length=3, must_use=""):
        pletters = "".join(re.findall('\w', pattern))
        return (w
                for w in self.find_subwords(letters + pletters)
                if (len(w) >= min_length and
                    re.search(pattern, w) and
                    (not must_use or all(l in w for l in must_use))))


    def find_options(self, letters, patterns, min_length=3, must_use=""):
        for p in patterns:
            yield (p, list(wm.find_subwords_for_pattern(letters=letters, pattern=p, min_length=min_length, must_use=must_use)))

if __name__ == "__main__":
    wm = WordMatcher("words.txt.gz")
