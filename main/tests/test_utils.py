from django.test import TestCase
from main.utils import chunk_generator


class TestUtils(TestCase):
    def test_chunk_generator_list(self):
        lst = list(range(9))
        result = list(chunk_generator(lst, 3))
        self.assertEqual(3, len(result))
        self.assertEqual([[0, 1, 2], [3, 4, 5], [6, 7, 8]], result)

    def test_chunk_generator_tuple(self):
        seq = tuple(range(9))
        first_chunk = next(chunk_generator(seq, 3))
        self.assertEqual(3, len(first_chunk))
        self.assertEqual((0, 1, 2), first_chunk)
