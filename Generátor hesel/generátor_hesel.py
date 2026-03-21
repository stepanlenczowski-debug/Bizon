import random
import string

print("----- GENERÁTOR HESEL -----")

# vstupy od uživatele
count = int(input("Kolik hesel chceš vygenerovat?: "))
length = int(input("Zadej délku hesla: "))
use_numbers = input("Chceš použít čísla? (y/n): ").lower()
use_symbols = input("Chceš použít symboly? (y/n): ").lower()

# základ znaků
characters = string.ascii_letters

if use_numbers == "y":
    characters += string.digits

if use_symbols == "y":
    characters += "!@#$%^&*()_+-="


def check_password_strength(password):
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in "!@#$%^&*()_+-=" for c in password)

    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if has_lower and has_upper:
        score += 1
    if has_digit:
        score += 1
    if has_symbol:
        score += 1

    if score <= 2:
        return "SLABÉ"
    elif score <= 4:
        return "STŘEDNÍ"
    else:
        return "SILNÉ"


for i in range(count):
    password = ""

    for j in range(length):
        password += random.choice(characters)

    strength = check_password_strength(password)
    print(f"{i + 1}. heslo: {password} | Síla: {strength}")
