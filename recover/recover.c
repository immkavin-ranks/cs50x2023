#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    char *rawfile;
    if (argc == 2)
    {
        rawfile = argv[1];
    }
    else
    {
        printf("Usage: ./recover [forensic image]");
        return 1;
    }

    FILE *file = fopen(rawfile, "r");
    if (file == NULL)
    {
        printf("Could not open file %s.\n", rawfile);
        return 1;
    }
    unsigned char buffer[BLOCK_SIZE];
    int file_number = 0;
    FILE *out_file = NULL;
    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (out_file != NULL)
            {
                fclose(out_file);
            }

            char filename[8]; // Ex. "001.jpg\0" -> 8 characters
            sprintf(filename, "%03i.jpg", file_number);
            out_file = fopen(filename, "w");
            file_number++;
        }
        if (out_file != NULL)
        {
            fwrite(buffer, sizeof(char), BLOCK_SIZE, out_file);
        }
    }
    if (out_file != NULL)
    {
        fclose(out_file);
    }
    fclose(file);
}
