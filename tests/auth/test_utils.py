import string
from django.test import TestCase
from djplus.auth.utils import generate_random_string


class GenerateRandomStringTest(TestCase):
    def test_length(self):
        s = generate_random_string(length=6)
        self.assertEqual(len(s), 6)

        s = generate_random_string(length=12)
        self.assertEqual(len(s), 12)

    def test_raise_when_length_is_negative(self):
        expected_error = "Length can't contain negative values"
        with self.assertRaisesMessage(ValueError, expected_error):
            generate_random_string(length=-1)

        with self.assertRaisesMessage(ValueError, expected_error):
            generate_random_string(length=-6)

    def test_lowercase(self):
        s = generate_random_string(lowercase=True)
        self.assertTrue(any(map(str.islower, s)))

        s = generate_random_string(lowercase=False)
        self.assertFalse(any(map(str.islower, s)))

    def test_uppercase(self):
        s = generate_random_string(uppercase=True)
        self.assertTrue(any(map(str.isupper, s)))

        s = generate_random_string(uppercase=False)
        self.assertFalse(any(map(str.isupper, s)))

    def test_number(self):
        s = generate_random_string(number=True)
        self.assertTrue(any(map(str.isdigit, s)))

        s = generate_random_string(number=False)
        self.assertFalse(any(map(str.isdigit, s)))
        
    def test_symbol(self):
        s = generate_random_string(symbol=True)
        self.assertTrue(any(char in s for char in string.punctuation))

        s = generate_random_string(symbol=False)
        self.assertFalse(any(char in s for char in string.punctuation))

    def test_a_example(self):
        s = generate_random_string(length=4, lowercase=True, uppercase=True, number=True, symbol=True)
        self.assertTrue(any(map(str.islower, s)))
        self.assertTrue(any(map(str.isupper, s)))
        self.assertTrue(any(map(str.isdigit, s)))
        self.assertTrue(any(char in s for char in string.punctuation))

    def test_raise_when_the_amount_of_length_is_not_enough_to_generate(self):
        expected_error = "With the given arguments, the `length` value must be at least %(length)d"

        with self.assertRaisesMessage(ValueError, expected_error % {"length": 1}):
            generate_random_string(length=0, lowercase=False, uppercase=False, number=True, symbol=False)

        with self.assertRaisesMessage(ValueError, expected_error % {"length": 2}):
            generate_random_string(length=1, lowercase=True, uppercase=True, number=False, symbol=False)

        with self.assertRaisesMessage(ValueError, expected_error % {"length": 3}):
            generate_random_string(length=0, lowercase=True, uppercase=False, number=True, symbol=True)

        with self.assertRaisesMessage(ValueError, expected_error % {"length": 4}):
            generate_random_string(length=3, lowercase=True, uppercase=True, number=True, symbol=True)

    def test_raise_when_all_of_the_arguments_are_false(self):
        expected_error = "At least one of these arguments must be True. {lowercase, uppercase, number, symbol}"
        with self.assertRaisesMessage(ValueError, expected_error):
            generate_random_string(lowercase=False, uppercase=False, number=False, symbol=False)
