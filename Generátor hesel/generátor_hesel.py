import secrets
import string

ERROR_MESSAGE = "Neplatná volba, zadej 'y' nebo 'n'."


def get_int(prompt: str, min_value: int = 1, max_value: int = 100) -> int:
    """Načte a validuje celé číslo ve specifikovaném rozsahu."""
    while True:
        user_input = input(prompt).strip()
        if not user_input.isdigit():
            print("Hodnota musí být celé číslo.")
            continue

        value = int(user_input)
        if value < min_value or value > max_value:
            print(f"Zadej číslo mezi {min_value} a {max_value}.")
            continue

        return value


def get_yes_no(prompt: str) -> bool:
    """Vrací True pro 'y', False pro 'n'."""
    while True:
        answer = input(prompt).strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False

        print(ERROR_MESSAGE)


def generate_password(length: int, use_numbers: bool, use_symbols: bool) -> str:
    """Vygeneruje bezpečné náhodné heslo podle nastavení."""
    characters = string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += "!@#$%^&*()_+-="

    # Sestavení hesla znak po znaku pro zajištění náhodnosti
    return "".join(secrets.choice(characters) for _ in range(length))


def main() -> None:
    print("----- GENERÁTOR HESEL -----")

    length = get_int("Zadej délku hesla (4-128): ", min_value=4, max_value=128)
    use_numbers = get_yes_no("Chceš použít čísla? (y/n): ")
    use_symbols = get_yes_no("Chceš použít symboly? (y/n): ")

    password = generate_password(length, use_numbers, use_symbols)

    print("\nVygenerované heslo:")
    print(password)


if __name__ == "__main__":
    main()

