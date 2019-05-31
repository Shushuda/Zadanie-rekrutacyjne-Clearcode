import unittest
import io
from contextlib import redirect_stdout
from unittest.mock import mock_open, patch
import zadanie


# helper function to avoid redundancy of code and preserve code clarity
# redirects stdout prints to a variable as a string
def helper_redirect_stdout(tested_func, *args):
    f = io.StringIO()
    with redirect_stdout(f):
        tested_func(*args)
    return f.getvalue()


class TestZadanie(unittest.TestCase):

    def test_convert_file_type(self):
        """
        Test that the file conversion results in a StringIO file object
        """

        data = """id,name,surname
1,Adam,Kowalski
2,Seth,McFarlane"""

        with patch('builtins.open', mock_open(read_data=data)):
            result = zadanie.convert_file('foo')

        self.assertIs(type(result), io.StringIO)

    def test_convert_file_contents(self):
        """
        Test that the file conversion doesn't change the data of the file and successfully copies it all
        """

        data = """id,name,surname
1,Adam,Kowalski
2,Seth,McFarlane"""

        expected = io.StringIO("""id,name,surname
1,Adam,Kowalski
2,Seth,McFarlane""")

        with patch('builtins.open', mock_open(read_data=data)):
            result = zadanie.convert_file('foo')

        self.assertEqual(result.getvalue(), expected.getvalue())

    def test_file_exceptions_wrong_filename(self):
        """
        Test whether the script correctly reacts to a nonexistent file or typos in the filename.
        """

        fake_filename = "foo"

        expected = "[Errno 2] No such file or directory: 'foo' . Provide correct filenames with filename extensions."

        with self.assertRaises(SystemExit) as cm:
            result = helper_redirect_stdout(zadanie.file_exceptions, zadanie.convert_file, fake_filename)

            self.assertEqual(expected, result)
            self.assertEqual(cm.exception.code, 0)

    def test_argument_parser_two_arguments(self):
        """
        Test that the argument parser function accepts exactly two arguments.
        """

        fake_args = ['one', 'two']

        expected = {'file_one': 'one', 'file_two': 'two'}

        result = zadanie.argument_parser(fake_args)

        self.assertEqual(vars(result), expected)

    def test_argument_parser_one_argument(self):
        """
        Test that the argument parser function reacts properly to too few arguments - one.
        """

        fake_args = ['one']

        with self.assertRaises(SystemExit) as cm:
            zadanie.argument_parser(fake_args)

            self.assertEqual(cm.exception.code, 0)

    def test_argument_parser_one_argument(self):
        """
        Test that the argument parser function reacts properly to too few arguments - zero.
        """

        fake_args = []

        with self.assertRaises(SystemExit) as cm:
            zadanie.argument_parser(fake_args)

            self.assertEqual(cm.exception.code, 0)

    def test_merge_wrong_persons_CSV(self):
        """
        Test that the merge function rejects a persons CSV file with the header of wrong format.
        Correct format is specified in -h of the script.
        """

        wrong_persons_file = io.StringIO("""id,surname,test_name
1,Adam,Kowalski
2,Seth,McFarlane""")

        correct_visits_file = io.StringIO("""id,person_id,site
1,2,test.pl
2,2,test.com""")

        expected = "Fieldnames error: One or more of the provided CSV files contain incorrect data. " \
                   "Check the headers and try again."

        with self.assertRaises(SystemExit) as cm:
            result = helper_redirect_stdout(zadanie.merge, wrong_persons_file, correct_visits_file)

            self.assertEqual(expected, result)
            self.assertEqual(cm.exception.code, 0)

    def test_merge_wrong_visits_CSV(self):
        """
        Test that the merge function rejects a visits CSV file with the header of wrong format.
        Correct format is specified in -h of the script.
        """

        correct_persons_file = io.StringIO("""id,name,surname
1,Adam,Kowalski
2,Seth,McFarlane""")

        wrong_visits_file = io.StringIO("""id,test_wrong,hello_there_fellow_programmers
1,2,test.pl
2,2,test.com""")

        expected = "Fieldnames error: One or more of the provided CSV files contain incorrect data. " \
                   "Check the headers and try again."

        with self.assertRaises(SystemExit) as cm:
            result = helper_redirect_stdout(zadanie.merge, correct_persons_file, wrong_visits_file)

            self.assertEqual(expected, result)
            self.assertEqual(cm.exception.code, 0)

    def test_merge_correct_CSV_files(self):
        """
        Test that the merge function accepts correct CSV files and produces a correct list of dicts.
        Correct format is specified in -h of the script.
        """

        correct_persons_file = io.StringIO("""id,name,surname
1,Adam,Kowalski
2,Seth,McFarlane""")

        correct_visits_file = io.StringIO("""id,person_id,site
1,2,test.pl
2,2,test.com""")

        expected = [
            {
                "id": '1',
                "name": "Adam",
                "surname": "Kowalski",
                "visits": 0
            },
            {
                "id": '2',
                "name": "Seth",
                "surname": "McFarlane",
                "visits": 2
            }
        ]

        result = zadanie.merge(correct_persons_file, correct_visits_file)

        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main(exit=False)
