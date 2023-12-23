#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");
    double noOfLetters = count_letters(text);
    double noOfWords = count_words(text);
    double noOfSentences = count_sentences(text);

    double L = (noOfLetters / noOfWords) * 100;
    double S = (noOfSentences / noOfWords) * 100;

    int index = round((0.0588 * L) - (0.296 * S) - 15.8);

    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_sentences(string text)
{
    int pos = 0, sentences = 0;
    while (text[pos] != '\0')
    {
        if (text[pos] == '.' || text[pos] == '!' || text[pos] == '?')
        {
            sentences++;
        }
        pos++;
    }
    return sentences;
}

int count_words(string text)
{
    int pos = 0, words = 0;
    while (text[pos] != '\0')
    {
        if (isspace(text[pos]))
        {
            words++;
        }
        pos++;
    }
    return words + 1; // plus one for last word in text
}

int count_letters(string text)
{
    int pos = 0, letters = 0;
    while (text[pos] != '\0')
    {
        if (isalpha(text[pos]))
        {
            letters++;
        }
        pos++;
    }
    return letters;
}
