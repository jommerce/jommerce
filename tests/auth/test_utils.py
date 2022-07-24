import string
from django.test import TestCase
from djplus.auth.utils import generate_random_string


class GenerateRandomStringTests(TestCase):
    def test_string_length(self):
        s = generate_random_string(length=6)
        self.assertEqual(len(s), 6)
        s = generate_random_string(length=12)
        self.assertEqual(len(s), 12)

    def test_generate_at_least_one_lowercase_character(self):
        s = generate_random_string(lowercase=True)
        self.assertTrue(any(map(str.islower, s)))

    def test_generate_without_lowercase_characters(self):
        s = generate_random_string(lowercase=False)
        self.assertFalse(any(map(str.islower, s)))

    def test_generate_at_least_one_uppercase_character(self):
        s = generate_random_string(uppercase=True)
        self.assertTrue(any(map(str.isupper, s)))

    def test_generate_without_uppercase_characters(self):
        s = generate_random_string(uppercase=False)
        self.assertFalse(any(map(str.isupper, s)))

    def test_generate_at_least_one_digit_character(self):
        s = generate_random_string(digit=True)
        self.assertTrue(any(map(str.isdigit, s)))

    def test_generate_without_digit_characters(self):
        s = generate_random_string(digit=False)
        self.assertFalse(any(map(str.isdigit, s)))
        
    def test_generate_at_least_one_special_character(self):
        s = generate_random_string(symbol=True)
        self.assertTrue(any(char in s for char in string.punctuation))

    def test_generate_without_special_characters(self):
        s = generate_random_string(symbol=False)
        self.assertFalse(any(char in s for char in string.punctuation))

    def test_a_string_of_length_4_that_includes_letters_and_numbers_and_special_characters(self):
        s = generate_random_string(length=4, lowercase=True, uppercase=True, digit=True, symbol=True)
        self.assertTrue(any(map(str.islower, s)))
        self.assertTrue(any(map(str.isupper, s)))
        self.assertTrue(any(map(str.isdigit, s)))
        self.assertTrue(any(char in s for char in string.punctuation))

    def test_raise_when_length_is_negative(self):
        expected_error = "Length can't contain negative values"
        with self.assertRaisesMessage(ValueError, expected_error):
            generate_random_string(length=-1)
        with self.assertRaisesMessage(ValueError, expected_error):
            generate_random_string(length=-6)

    def test_error_not_enough_length_to_generate(self):
        expected_error = "With the given arguments, the `length` value must be at least %(length)d"
        with self.assertRaisesMessage(ValueError, expected_error % {"length": 1}):
            generate_random_string(length=0, lowercase=False, uppercase=False, digit=True, symbol=False)
        with self.assertRaisesMessage(ValueError, expected_error % {"length": 2}):
            generate_random_string(length=1, lowercase=True, uppercase=True, digit=False, symbol=False)
        with self.assertRaisesMessage(ValueError, expected_error % {"length": 3}):
            generate_random_string(length=0, lowercase=True, uppercase=False, digit=True, symbol=True)
        with self.assertRaisesMessage(ValueError, expected_error % {"length": 4}):
            generate_random_string(length=3, lowercase=True, uppercase=True, digit=True, symbol=True)

    def test_raise_when_all_of_the_arguments_are_false(self):
        expected_error = "At least one of these arguments must be True. {lowercase, uppercase, digit, symbol}"
        with self.assertRaisesMessage(ValueError, expected_error):
            generate_random_string(lowercase=False, uppercase=False, digit=False, symbol=False)
