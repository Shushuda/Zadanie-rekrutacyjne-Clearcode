import sys
import unittest
import io
import argparse
from unittest.mock import mock_open, patch
import zadanie


class TestZadanie(unittest.TestCase):

    def test_convert_file_type(self):
        """
        Test that the file conversion results in a StringIO file object
        """
        testargv = ['one', 'two']

        data = """id,name,surname
1,Adam,Kowalski
2,Seth,McFarlane"""

        with patch.object(sys, 'argv', testargv):
            with patch('builtins.open', mock_open(read_data=data)) as m:
                result = zadanie.convert_file('foo')

        self.assertIs(type(result), io.StringIO)

    def test_convert_file_contents(self):
        """
        Test that the file conversion doesn't change the data of the file and successfully copies it all
        """
        testargv = ['one', 'two']

        data = """id,name,surname
1,Adam,Kowalski
2,Seth,McFarlane"""

        expected = io.StringIO("""id,name,surname
1,Adam,Kowalski
2,Seth,McFarlane""")

        with patch.object(sys, 'argv', testargv):
            with patch('builtins.open', mock_open(read_data=data)) as m:
                result = zadanie.convert_file('foo')

        self.assertEqual(result.getvalue(), expected.getvalue())


if __name__ == '__main__':
    unittest.main()
