#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long long int number = get_long_long("Number: ");
    long long int temp = number;
    int digit, i = 0, checksum = 0;
    int digits[16];

    while (number > 0)
    {
        digit = number % 10;
        if (i % 2 != 0)
        {
            digits[i] = digit * 2;
        }
        else
        {
            digits[i] = digit;
        }

        i++;
        number /= 10;
    }

    for (int j = 0; j < i; j++)
    {
        if (digits[j] % 10 != 0)
        {
            checksum += digits[j] % 10;
        }
        digits[j] /= 10;
        checksum += digits[j];
    }

    while (temp >= 100)
    {
        temp /= 10;
    }
    int two_digits = temp;
    int first_digit = two_digits / 10;

    if (checksum % 10 == 0)
    {
        // Check for AMEX card
        if ((i == 15) && (two_digits == 34 || two_digits == 37))
        {
            printf("AMEX\n");
        }
        // Check for MASTERCARD
        else if ((i == 16) && (two_digits >= 51 && two_digits <= 55))
        {
            printf("MASTERCARD\n");
        }
        // Check for VISA card
        else if ((i == 13 || i == 16) && (first_digit == 4))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
