// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 2048 * 2;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    unsigned int hash_value = hash(word);
    node *node = table[hash_value];
    while (node != NULL)
    {
        if (strcasecmp(node->word, word) == 0)
        {
            return true;
        }
        node = node->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int hash_value = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash_value += (int) (tolower(word[i]));
    }

    return hash_value % N;
}

// Loads dictionary into memory, returning true if successful, else false
unsigned int word_count = 0;
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }
        strcpy(new_node->word, word);
        unsigned int hash_value = hash(word);
        new_node->next = table[hash_value];
        table[hash_value] = new_node;
        word_count++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
