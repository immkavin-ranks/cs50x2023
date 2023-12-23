#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int n; // population size
    do
    {
        n = get_int("Start size: ");
    }
    while (n < 9);

    // TODO: Prompt for end size
    int end_size;
    do
    {
        end_size = get_int("End size: ");
    }
    while (end_size < n);

    // TODO: Calculate number of years until we reach threshold
    int years = 0;
    while (n < end_size)
    {
        n = n + (n / 3) - (n / 4);
        years++;
    }

    // TODO: Print number of years
    printf("Years: %i\n", years);
}
