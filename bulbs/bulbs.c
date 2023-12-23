#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

struct binaryStruct
{
    int byte[BITS_IN_BYTE];
} s;

int main(void)
{
    // TODO
    string message = get_string("Message: ");
    int pos = 0;
    while (message[pos] != '\0')
    {
        int ascii = (int) message[pos];
        struct s;
        for (int i = 0; i < BITS_IN_BYTE; i++)
        {
            s.byte[i] = 0;
        }
        int bits = BITS_IN_BYTE - 1;
        while (ascii > 0)
        {
            s.byte[bits] = ascii % 2;
            bits--;
            ascii /= 2;
        }

        for (int i = 0; i < BITS_IN_BYTE; i++)
        {
            print_bulb(s.byte[i]);
        }
        printf("\n");

        pos++;
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
