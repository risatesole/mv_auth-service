import hashlib
import secrets
import hmac

def hasher(phrase: str) -> str:
    salt = secrets.token_bytes(16)
    iterations = 310_000

    dk = hashlib.pbkdf2_hmac(
        'sha256',
        phrase.encode('utf-8'),
        salt,
        iterations
    )

    return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"

def hashverifier(password: str, stored: str) -> bool:
    algo, iterations, salt_hex, hash_hex = stored.split('$')
    iterations = int(iterations)
    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(hash_hex)

    dk = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations
    )

    return hmac.compare_digest(dk, expected)


if __name__ == "__main__":
    password = "supersecret"

    print("Password hashing demo (stdlib only)")
    print("-" * 40)

    stored = hasher(password)

    print("Original password:")
    print(password)
    print()

    print("Stored representation:")
    print(stored)
    print()

    print("Verifying correct password...")
    if hashverifier(password, stored):
        print("Correct password accepted")
    else:
        print("Correct password rejected (this should not happen)")
    print()

    print("Verifying wrong password...")
    if hashverifier("wrong", stored):
        print("Wrong password accepted (this is BAD)")
    else:
        print("Wrong password rejected")
    print()

    print("Summary:")
    print("• Password was salted")
    print("• Hash was derived using PBKDF2-HMAC-SHA256")
    print("• Comparison was done in constant time")
    print()
    print("OK")
