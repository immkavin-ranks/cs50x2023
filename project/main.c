#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    srand(time(NULL));

    int max_number = 100;
    int min_number = 1;

    int play_again = 1;

    int player_best = -1;

    while (play_again)
    {
        int player_guess;
        int attempts = 0;

        int random_secret_number = (rand() % (max_number - min_number + 1)) + min_number;

        printf("\n| GUESS THE NUMBER |\n");
        printf("\nMaximum Limit: 10 attempts\n");
        printf("Guess the number (between 1 and 100) or enter 0 to exit: ");

        while (1) {
            while (scanf("%d", &player_guess) != 1 || (player_guess != 0 && (player_guess < 1 || player_guess > 100))) {
                while (getchar() != '\n');
                printf("Invalid guess. Please enter a number between 1 and 100, or enter 0 to exit: ");
            }

            if (player_guess == 0) {
                play_again = 0;
                break;
            }

            if (player_guess != 0) {
                attempts++;
            }

            if (player_guess == random_secret_number && attempts < 10) {
                printf("Congratulations! You guessed the correct number in %d attempts.\n", attempts);
                if (player_best == -1 || attempts < player_best) {
                    player_best = attempts;
                    printf("New Achievement! Your best: %d attempts.\n", player_best);
                }
                break;
            } else if (player_guess < random_secret_number && attempts < 10) {
                printf("Too low. Try guessing a higher number: ");
            } else if (player_guess > random_secret_number && attempts < 10) {
                printf("Too high. Try guessing a lower number: ");
            }

            if (attempts >= 10) {
                printf("Game Over! You have exceeded the maximum number of attempts.\n");
                break;
            }
        }

        if (play_again == 1 && attempts < 10) {
            printf("Do you want to play again? (1 for Yes, 0 for No): ");
            scanf("%d", &play_again);
            while (getchar() != '\n');
            printf("\n");
        }
    }

    if (player_best != -1) {
        printf("Your best: %d attempts\n", player_best);
    } else {
        printf("No attempts made. Thank you for playing!\n");
    }

    //system("pause");

    return 0;
}
