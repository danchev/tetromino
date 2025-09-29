# This script generates a Tetris input file of random length and random moves.
# Usage: import and call generate_random_tetris_input(filename, num_lines)
import random


def generate_random_tetris_input(filename, num_lines):
    piece_types = ["Q", "Z", "S", "T", "I", "L", "J"]
    width = random.randint(5, 150)  # Random width between 5 and 15
    with open(filename, "w") as f:
        for _ in range(num_lines):
            line = []
            for _ in range(width):
                piece = random.choice(piece_types)
                col = random.randint(0, width - 1)
                line.append(f"{piece}{col}")
            f.write(",".join(line) + "\n")


# Example usage:
# generate_random_tetris_input("tests/resources/random_input.txt", 500)

if __name__ == "__main__":
    generate_random_tetris_input("random_input.txt", 500)
