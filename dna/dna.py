import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) < 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return

    # TODO: Read database file into a variable
    data = []
    filename, sequence_file = sys.argv[1], sys.argv[2]
    with open(filename) as file:
        reader = csv.DictReader(file)
        # comprehension --> data = [{k: v for k, v in row.items()} for row in reader]
        for row in reader:
            row_dict = {}
            for k, v in row.items():
                row_dict[k] = v
            data.append(row_dict)

    # TODO: Read DNA sequence file into a variable
    with open(sequence_file) as file:
        sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    str_counts = {}  #  Short Tandem Repeats -> str

    for STR in data[0]:
        if STR != "name":
            str_counts[STR] = longest_match(sequence, STR)

    # TODO: Check database for matching profiles
    for person in data:
        # comprehension --> person_counts = {STR: int(person[STR]) for STR in person if STR != "name"}
        person_counts = {}
        for STR in person:
            if STR != "name":
                person_counts[STR] = int(person[STR])

        if person_counts == str_counts:
            print(person["name"])
            return
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
