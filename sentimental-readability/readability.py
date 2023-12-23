# TODO
from cs50 import get_string


def main():
    text = get_string("Text: ")
    no_of_letters = count_letters(text)
    no_of_words = count_words(text)
    no_of_sentences = count_sentences(text)

    l = (no_of_letters / no_of_words) * 100
    s = (no_of_sentences / no_of_words) * 100

    index = round((0.0588 * l) - (0.296 * s) - 15.8)

    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


def count_sentences(text):
    sentences = 0
    for char in text:
        if char in [".", "!", "?"]:
            sentences += 1

    return sentences


def count_words(text):
    words = 0
    for char in text:
        if char.isspace():
            words += 1

    return words + 1


def count_letters(text):
    letters = 0
    for char in text:
        if char.isalpha():
            letters += 1

    return letters


if __name__ == "__main__":
    main()
