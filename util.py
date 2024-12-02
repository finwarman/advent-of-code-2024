import os
import sys
from pathlib import Path

def get_input_data(default_file='input.txt', env_var='INPUT_FILE'):
    """
    Retrieve input data from a default file, env var filename, or stdin.
    :param default_file: The default input file to read.
    :param env_var: The environment variable to check for the file path.
    :return: Content of the input as a string.
    """

    # Check for STDIN
    if not sys.stdin.isatty():
        return sys.stdin.read()

    # Resolve the default file relative to the importing script's directory
    script_dir = Path(sys.modules['__main__'].__file__).resolve().parent
    default_file_path = script_dir / default_file

    # Read from file (INPUT_FILE env var or resolved default file path)
    input_file = os.getenv(env_var, str(default_file_path))
    print("[#aoc] input file:", input_file)
    with open(input_file, 'r', encoding='UTF-8') as file:
        return file.read()
