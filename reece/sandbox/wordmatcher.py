"""class that's useful for playing with anagrams, crosswords, and other word games

wget -nd http://iweb.dl.sourceforge.net/project/wordlist/speller/2016.01.19/hunspell-en_US-2016.01.19.zip
unzip hunspell-en_US-2016.01.19.zip
unmunch en_US.dic en_US.aff | perl -ne 'print unless m/\d|^[A-Z]|\x27|^[A-Z]+s?$|^\w$/' | sort -u | gzip >|words.txt.gz

"""

import collections
import gzip
import itertools
import re


def _sdiff(s1, s2):
    """return symmetric diff of strings s1 and s2, as a tuple of (letters
    unique to s1, letters common to both, letters unique to s2.

    s1 and s2 must be strings with letters in sorted order

    """

    if s1 == s2:
        return ('', s1, '')

    i1 = i2 = 0
    u1 = u2 = i = ""

    while i1 < len(s1) and i2 < len(s2):
        if s1[i1] == s2[i2]:
            i += s1[i1]
            i1 += 1
            i2 += 1
        elif s1[i1] <= s2[i2]:
            u1 += s1[i1]
            i1 += 1
        elif s2[i2] <= s1[i1]:
            u2 += s2[i2]
            i2 += 1
        else:
            assert False, "Shouldn't be here"

    u1 += s1[i1:]
    u2 += s2[i2:]

    return (u1, i, u2)


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


    def diff(w, u):
        """returns a tuple of three strings, representing letters unique to w,
        common to both, and unique to u"""
        assert isinstance(w, WordKey) and isinstance(u, WordKey), "expected two WordKey instances"
        return _sdiff(w, u)


class WordMatcher(object):
    alphabet = "abcdefghijklmnopqrstuvwxyz"

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
                for w in itertools.chain.from_iterable(self._key_wordlist_map[k] for k in subkeys))

    # consider returning flat structure like {blanks, word}
    # return in desc length order?
    def find_subwords_for_pattern(self, tiles, pattern):
        t_letters = tiles.replace('_', '')
        n_blanks = len(tiles) - len(t_letters)
        p_letters = "".join(re.findall('\w', pattern))
        avail_letters = t_letters + p_letters
        al_wk = WordKey(avail_letters)
        returned = set()

        wkeys = sorted(self._key_wordlist_map.keys(), key = lambda e: len(e), reverse = True)

        blank_key_pairs = [(b, k)
                           for k, b in ((k, k.diff(al_wk)[0]) for k in wkeys)
                           if len(b) <= n_blanks]
        blank_key_pairs.sort(key=lambda bk: (len(bk[0]), bk[0]))

        for b, bk_i in itertools.groupby(blank_key_pairs, key=lambda bk: (len(bk[0]), bk[0])):
            words = [w
                     for w in itertools.chain.from_iterable(self._key_wordlist_map[bk[1]] for bk in bk_i)
                     if re.search(pattern, w)]
            new_words = set(words) - returned
            if len(new_words) > 0:
                returned.update(new_words)
                yield {'blanks': b, 'words': sorted(new_words, key=len, reverse=True)}

    def find_options(self, tiles, patterns, min_length=2, must_use=""):
        for p in patterns:
            yield (p, list(self.find_subwords_for_pattern(
                tiles=tiles, pattern=p)))

if __name__ == "__main__":
    wm = WordMatcher("reece/sandbox/_data/wordlists/words.txt.gz")
