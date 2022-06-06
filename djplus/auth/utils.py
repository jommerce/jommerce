import string
import secrets


def generate_random_string(length=6, lowercase=True, uppercase=True, number=True, symbol=True):
    if length < 0:
        raise ValueError("Length can't contain negative values")
    if not any((lowercase, uppercase, number, symbol)):
        raise ValueError("At least one of these arguments must be True. {lowercase, uppercase, number, symbol}")

    values = set()
    characters = ""
    if lowercase:
        values.add(secrets.choice(string.ascii_lowercase))
        characters += string.ascii_lowercase
    if uppercase:
        values.add(secrets.choice(string.ascii_uppercase))
        characters += string.ascii_uppercase
    if number:
        values.add(secrets.choice(string.digits))
        characters += string.digits
    if symbol:
        values.add(secrets.choice(string.punctuation))
        characters += string.punctuation

    try:
        indexes = secrets.SystemRandom().sample(range(length), len(values))
    except ValueError:
        raise ValueError(f"With the given arguments, the `length` value must be at least {len(values)}")

    s = [secrets.choice(characters) for _ in range(length)]
    for index, value in zip(indexes, values):
        s[index] = value
    return "".join(s)
