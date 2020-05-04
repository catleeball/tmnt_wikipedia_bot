import unittest
import lib.words as words


class IsTMNTTest(unittest.TestCase):
    def test_valid_string_returns_true(self):
        """
        A string in trochaic tetrameter passed into isTMNT()
        should return True
        """
        test_string = "Teenage Mutant Ninja Turtles"
        self.assertTrue(words.isTMNT(test_string))

    def test_invalid_string_returns_false(self):
        """
        A string not in trochaic tetrameter passed into isTMNT()
        should return False
        """
        test_string = "Romeo, Romeo, wherefore art thou, Romeo?"
        self.assertFalse(words.isTMNT(test_string))

    def test_banned_word_in_valid_string_returns_false(self):
        """
        A string in trochaic tetrameter passed into isTMNT()
        that contains a banned word should return False
        """
        test_string = "Teenage Mutant Nazi Turtles"
        self.assertFalse(words.isTMNT(test_string))


class ContainsBannedTest(unittest.TestCase):
    def test_banned_word_in_string(self):
        """
        If the string contains a banned word, containsBanned()
        should return True
        """
        test_string = "Teenage Mutant Nazi Turtles"
        self.assertTrue(words.containsBanned(test_string))

    def test_not_banned_word_in_string(self):
        """
        Nothing in this string is on the banned words or phrases
        lists so containsBanned() should return False
        """
        test_string = "Teenage Mutant Ninja Turtles"
        self.assertFalse(words.containsBanned(test_string))

    def test_banned_phrase_in_string(self):
        """
        Rugby Player is on the banned phrases list so
        containsBanned() should return True
        """
        test_string = "Teenage Mutant Rugby Player"
        self.assertTrue(words.containsBanned(test_string))


class GetTitleStressesTest(unittest.TestCase):
    def test_valid_title_stresses(self):
        """
        getTitleStresses() should return a string value of '12101010'
        for 'Teenage Mutant Ninja Turtles'
        """
        test_title = "Teenage Mutant Ninja Turtles"
        self.assertEqual(words.getTitleStresses(test_title), "12101010")

    def test_title_stresses_for_long_title(self):
        """
        getTitleStresses() should return None if the title has
        too many syllables
        """
        test_title = "Teenage Mutant Ninja Turtle Dinosaurs"
        self.assertIsNone(words.getTitleStresses(test_title))


class GetWordStressesTest(unittest.TestCase):
    def test_get_word_stresses_output(self):
        """
        getWordStresses() should output a string containing the digits
        0, 1 and/or 2. Turtles should return '10'.
        """
        test_word = "Turtles"
        self.assertEqual(words.getWordStresses(test_word), "10")

    def test_get_word_stresses_index_error(self):
        """
        """
        pass

    def test_get_word_stresses_pronunciation_override(self):
        """
        For a word on the Pronunciation Override list, return the
        corresponding override value, instead of the pronouncing
        output.
        """
        test_word = "U.S."
        self.assertEqual(words.getWordStresses(test_word), "10")


class NumbersToWordsTest(unittest.TestCase):
    def test_numbers_to_words_with_word_ninth(self):
        """
        Passing '9th' to numbersToWords() should return 'ninth'
        """
        test_string = "9th"
        self.assertEqual(words.numbersToWords(test_string), "ninth")

    def test_numbers_to_words_with_digit(self):
        """
        Passing 18 to numbersToWords() should return 'eighteen'
        """
        test_string = "18"
        self.assertEqual(words.numbersToWords(test_string), "eighteen")

    def test_numbers_to_words_with_year(self):
        """
        Passing a year-like number should return a year-like string
        """
        test_string = "2019"
        self.assertEqual(words.numbersToWords(test_string), "twenty nineteen")

    def test_numbers_to_words_with_string(self):
        """
        Passing something that isn't a number should return the
        original word
        """
        test_string = "turtle"
        self.assertEqual(words.numbersToWords(test_string), "turtle")


class CleanStrTest(unittest.TestCase):
    def test_testcleanstr_with_valid_string(self):
        """
        Some strings require no modification. If so, return the
        original string with no changes.
        """
        test_string = "fooBar123"
        self.assertEqual(words.cleanStr(test_string), "fooBar123")

    def test_testcleanstr_with_deletable_characters(self):
        """
        Some strings require characters to be removed entirely,
        such as brackets.
        """
        test_string = "Hello ([world])"
        self.assertEqual(words.cleanStr(test_string), "Hello world")

    def test_testcleanstr_with_swappable_characters(self):
        """
        Some strings require characters to be swapped out,
        such as dashes, which we replace with strings.
        """
        test_string = "hello-world"
        self.assertEqual(words.cleanStr(test_string), "hello world")


class GetWikiTest(unittest.TestCase):
    def test_getwiki_with_one_word(self):
        """
        getWikiURL should return a full English Wikipedia URL
        for a single word
        """
        test_string = "Turtle"
        expected_output = "https://en.wikipedia.org/wiki/Turtle"
        self.assertEqual(words.getWikiUrl(test_string), expected_output)

    def test_getwiki_with_multiple_words(self):
        """
        getWikiURL should return a full English Wikipedia URL
        for multiple words, with underscores replacing spaces
        """
        test_string = "Teenage Mutant Ninja Turtles"
        expected_output = "https://en.wikipedia.org/wiki/Teenage_Mutant_Ninja_Turtles"
        self.assertEqual(words.getWikiUrl(test_string), expected_output)


class AddPaddingTest(unittest.TestCase):
    def test_addpadding_doesnt_change_four_word_title(self):
        """
        If a title only has 4 words, then addPadding() has nothing
        to do and should simply return the original title
        """
        test_string = "Teenage Mutant Ninja Turtles"
        self.assertEqual(words.addPadding(test_string), "Teenage Mutant Ninja Turtles")

    def test_addpadding_adds_padding(self):
        """
        If a title only has 3 words, then addPadding() needs
        to add a space to push the 3rd word into the '4th'.
        """
        test_string = "Microsoft Transaction Server"
        self.assertEqual(words.addPadding(test_string), "Microsoft  Transaction Server")

    def test_addpadding_adds_padding_2(self):
        """
        If a title only has 2 words, then addPadding() needs
        to add multiple spaces to push the 2nd word into the '4th'.
        """
        test_string = "Two Words"
        self.assertEqual(words.addPadding(test_string), "  Two  Words")

    def test_addpadding_with_single_eight_syllable_word(self):
        """
        For a single 8-syllable word, the original word should simply
        be returned as-is.
        """
        test_string = "OneWordString"
        self.assertEqual(words.addPadding(test_string), "OneWordString")
