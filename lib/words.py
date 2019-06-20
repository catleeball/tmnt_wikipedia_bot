import pronouncing
import urllib

from lib.constants import BANNED
from num2words import num2words as n2w


def isTMNT(title: str):
    """Checks if a Wikipedia page title has the same stress pattern as TMNT.

    >>> isTMNT('Teenage Mutant Ninja Turtles')
    True

    >>> isTMNT('Single Payer Health Insurance')
    True

    >>> isTMNT('Romeo, Romeo, wherefore art thou, Romeo?')
    False
    """
    TMNT_STRESSES = (
        "12101010",
        "10101010",
    )

    for phrase in BANNED:
        if phrase in title.lower():
            return False

    title = cleanStr(title)
    title_stresses = getTitleStresses(title)

    if not title_stresses:
        return False

    if len(title_stresses) != 8:
        return False

    return title_stresses in TMNT_STRESSES


def getTitleStresses(title: str):
    """Takes a wikipedia title and gets the combined stresses of all words.

    >>> getTitleStresses('Teenage Mutant Ninja Turtles')
    '12101010'

    Args:
        title: String, title of a wikipedia page.
    Returns:
        String, stresses of each syllable as 0, 1, and 2s.
    """
    title_words = title.split()
    title_stresses = ""
    while title_words:
        if len(title_stresses) > 8:
            return None
        word = title_words.pop(0)
        word_stresses = getWordStresses(word)
        # If word was a long number, it may have been parsed into several words.
        if isinstance(word_stresses, list):
            title_words = word_stresses + title_words
        else:
            title_stresses += getWordStresses(word)

    return title_stresses


def getWordStresses(word: str):
    word = numbersToWords(word)
    if " " in word:
        return word.split()
    try:
        phones = pronouncing.phones_for_word(word)
        stresses = pronouncing.stresses(phones[0])
    except IndexError:
        # Hacky way of discarding candidate title
        return "1111111111"
    return stresses


def numbersToWords(word):
    ordinal_number_endings = ("nd", "rd", "st", "th")
    if word.isdigit():
        if len(word) == 4:
            try:
                word = n2w(word, to="year")
            except Exception:
                # Hacky way of discarding candidate title
                return "1111111111"
        else:
            try:
                word = n2w(word)
            except Exception:
                # Hacky way of discarding candidate title
                return "1111111111"
    if word[:-2].isdigit() and word[-2:] in ordinal_number_endings:
        word = word[-2:]
        try:
            word = n2w(word, to="ordinal")
        except Exception:
            # Hacky way of discarding candidate title
            return "1111111111"

    return word


def cleanStr(s: str):
    """Remove characters that the pronouncing dictionary doesn't like.

    This isn't very efficient, but it's readable at least. :-)

    >>> cleanStr('fooBar123')
    'fooBar123'

    >>> cleanStr('Hello ([world])')
    'Hello world'

    >>> cleanStr('{hello-world}')
    'hello world'

    Args:
        s: String to be stripped of offending characters
    Returns:
        String without offending characters
    """
    DEL_CHARS = ["(", ")", "[", "]", "{", "}", ",", ":", ";", "."]
    SWAP_CHARS = [("-", " ")]

    for char in DEL_CHARS:
        s = s.replace(char, "")

    for char, replacement in SWAP_CHARS:
        s = s.replace(char, replacement)

    return s


def getWikiUrl(title: str):
    title = title.replace(" ", "_")
    title = urllib.parse.quote_plus(title)
    return "https://en.wikipedia.org/wiki/" + title
