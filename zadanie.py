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


# exception handling for passing command line arguments to the script
# informs the user of the cause of error and exits the script
# exception handling for: wrong number of provided files (requires two), wrong filenames
try:
    persons_f = convert_file(sys.argv[1])
    visits_f = convert_file(sys.argv[2])
except IndexError:
    print("Error: Too few files provided. Provide exactly two files.")
    sys.exit()
except FileNotFoundError as e:
    print(e, ". Provide correct filenames with filename extensions.")
    sys.exit()


print(merge(persons_f, visits_f))

