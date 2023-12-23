# TODO
from cs50 import get_float


def main():
    change_owed = get_float("Change owed: ")
    while change_owed < 0.01:
        change_owed = get_float("Change owed: ")

    change_owed = change_owed * 100

    quarters = calculate_quarters(change_owed)
    change_owed %= 25
    dimes = calculate_dimes(change_owed)
    change_owed %= 10
    nickels = calculate_nickels(change_owed)
    change_owed %= 5
    pennies = calculate_pennies(change_owed)
    change_owed %= 1

    min_coins = quarters + dimes + nickels + pennies

    print(int(min_coins))


def calculate_quarters(cents):
    if cents >= 25:
        return cents // 25

    return 0


def calculate_dimes(cents):
    if cents >= 10:
        return cents // 10

    return 0


def calculate_nickels(cents):
    if cents >= 5:
        return cents // 5

    return 0


def calculate_pennies(cents):
    if cents >= 1:
        return cents

    return 0


if __name__ == "__main__":
    main()
