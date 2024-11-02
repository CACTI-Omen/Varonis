import subprocess
import time
import string
import argparse
import os
from statistics import mean


def ensure_executable(vault_path):
    """Ensure that the vault.o file is executable. Set executable permissions if not."""
    if not os.access(vault_path, os.X_OK):
        try:
            subprocess.run(['chmod', '+x', vault_path], check=True)
            print(f"Set executable permissions on {vault_path}")
        except subprocess.CalledProcessError:
            print(f"Failed to set executable permissions on {vault_path}")
            exit(1)


def test_password(vault_path, password_attempt, attempts=5):
    """Run the vault.o program multiple times with a password attempt, return average execution time and output."""
    timings = []
    for _ in range(attempts):
        start_time = time.time()
        try:
            # Execute the vault program with the password attempt
            result = subprocess.run([vault_path, password_attempt], capture_output=True, text=True, timeout=1)
            elapsed_time = time.time() - start_time
            output = result.stdout.strip()  # Capture output like "Wrong password" or "SUCCESS!"
            success = "SUCCESS!" in output
            timings.append(elapsed_time)
            if success:
                return mean(timings), output, success
        except subprocess.TimeoutExpired:
            # If the process times out, it means the password is incorrect
            timings.append(time.time() - start_time)
            return mean(timings), "Timeout", False

    return mean(timings), "Wrong password", False


def timing_attack(vault_path):
    password = ''
    alphabet = string.ascii_lowercase  # Possible characters in the password
    position = 0

    # Log each password attempt and its result
    with open("password_attempts.log", "w") as log_file:
        while True:
            timings = []
            for char in alphabet:
                attempt = password + char
                elapsed_time, output, success = test_password(vault_path, attempt, attempts=5)
                log_file.write(f"Attempt: {attempt} - Output: {output} - Time: {elapsed_time:.5f}s\n")

                if success:
                    print(f"Password found: {attempt}")
                    log_file.write(f"\nPassword found: {attempt}")
                    return attempt

                timings.append((elapsed_time, char))
                print(f"Attempt: {attempt} - Output: {output} - Time: {elapsed_time:.5f}s")

            # Sort timings to find the longest one, which likely corresponds to a correct character
            timings.sort(reverse=True, key=lambda x: x[0])
            best_guess = timings[0][1]

            # Append the best guess to the password and move to the next character
            password += best_guess
            position += 1
            print(f"Best guess at position {position}: '{best_guess}' - Current password attempt: '{password}'")


def main():
    parser = argparse.ArgumentParser(description="Timing attack brute-force for vault.o.")
    parser.add_argument('-f', '--file', required=True, help="Path to the vault.o file")
    args = parser.parse_args()

    # Ensure the file is executable before running the attack
    ensure_executable(args.file)

    # Run the timing attack with the provided file path
    timing_attack(args.file)


if __name__ == "__main__":
    main()
