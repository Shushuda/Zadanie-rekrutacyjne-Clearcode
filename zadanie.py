import argparse
import sys
import io
import csv


# function for merging data of two file objects into a single list of dicts
# accepts two StringIO arguments (as requested in exercise's description)
def merge(persons_file, visits_file):

    # converts the StringIOs into DictReader objects containing OrderedDict objects with formatting done by csv module
    persons_reader = csv.DictReader(persons_file)
    visits_reader = csv.DictReader(visits_file)

    # exception handling whether the CSV files are accepted by the script
    # the acceptable data format is provided in the exercise's description
    # the validity of the CSV files is checked by comparing their headers with the correct values
    if persons_reader.fieldnames != ['id', 'name', 'surname'] or \
            visits_reader.fieldnames != ['id', 'person_id', 'site']:
        print("Fieldnames error: One or more of the provided CSV files contain incorrect data. "
              "Check the headers and try again.")
        sys.exit()

    # helper list objects containing above readers' data
    # stores the OrderedDict objects in lists to make them iterable
    # (DictReader can be "iterated" only once, as it behaves like a reader object)
    persons = [row for row in persons_reader]
    visits = [row for row in visits_reader]

    output = []

    # iterates over the above lists of OrderedDicts to create output dicts with keys specified in the exercise's
    # description and counts the amount of visits per each person
    # at the end of the outer for loop, the created dict is appended to the output list
    for person in persons:
        visits_num = 0

        for visit in visits:
            if person["id"] == visit["person_id"]:
                visits_num += 1

        dictionary = {
            "id": person["id"],
            "name": person["name"],
            "surname": person["surname"],
            "visits": visits_num
        }

        output.append(dictionary)

    # return the list of dicts
    return output


# helper function for converting provided files to StringIO objects (as requested in exercise's description)
def convert_file(given_file):
    with open(given_file, 'r', newline='') as opened_file:
        stringIO_file = io.StringIO(opened_file.read())
    return stringIO_file


# helper function for file exception handling
# created for code clarity, reducing redundancy of code and ease of unit testing
# exception handling for passing command line arguments to the script
# informs the user of the cause of error and exits the script
# exception handling for: wrong number of provided files (requires two), wrong filenames
def file_exceptions(used_funct, given_file):
    try:
        result = used_funct(given_file)
    except FileNotFoundError as e:
        print(e, ". Provide correct filenames with filename extensions.")
        sys.exit()
    return result


# helper function for parsing sys.args into easy to use variables
# informs the user which arguments are needed for the script to work
# provides -h descriptions of the script
def argument_parser():
    parser = argparse.ArgumentParser(description="Merge two CSV files' data into a list of dictionaries.")
    parser.add_argument('file_one')
    parser.add_argument('file_two')

    arguments = parser.parse_args()

    return arguments


# main entry point of the script
# runs all the above functions to provide an end result in sys.stdout
def main(args):
    persons_f = file_exceptions(convert_file, args.file_one)
    visits_f = file_exceptions(convert_file, args.file_two)

    print(merge(persons_f, visits_f))


# executed when the script is run from the command line
# needed for unittests to work properly
if __name__ == '__main__':
    arg = argument_parser()
    main(arg)

