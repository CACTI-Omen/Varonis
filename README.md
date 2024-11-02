# # Timing Attack Script for `vault.o`

This Python script performs a timing attack on the `vault.o` binary by attempting a password one character at a time and measuring the response time. The goal is to guess the password based on timing discrepancies.

## Prerequisites

- Python 3.7 or later
- Ensure `vault.o` is available in the same directory as the script or specify its path with the `-f` flag.
- Ensure `vault.o` has execute permissions. The script will attempt to set executable permissions if they are missing.

## Installation

1. **Clone or download the repository.**

2. **Ensure appropriate permissions**

3. **Execute**
   python3 timing_varonis.py -f /path/to/vault.o

