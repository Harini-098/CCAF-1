def is_prime(number: int) -> bool:
    """Return True if number is a prime, False otherwise.

    A prime is an integer greater than 1 with no positive divisors
    other than 1 and itself.
    """
    if number < 2:
        return False
    if number < 4:
        return True
    if number % 2 == 0:
        return False

    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2

    return True
