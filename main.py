import random

# For whatever reason, I'm having venv problems.  Whatever.
try:
    import pandas as pd
except ImportError:
    from pip._internal import main as pip
    pip(['install', 'pandas'])
    import pandas as pd

def insert_string(string: str, index: int, value: str) -> str:
    return string[:index] + value + string[index:len(string)]


def insert_operations(numbers: str,
                      add: bool = True,
                      subtract: bool = True,
                      multiply: bool = True,
                      divide: bool = True,
                      parentheses: bool = True) -> str:

    if add:
        idx = random.randint(1,len(numbers)-1)
        numbers = insert_string(numbers, idx, '+')
    if subtract:
        idx = random.randint(1,len(numbers)-1)
        while not numbers[idx].isdigit() and numbers[idx+1].isdigit():
            idx = random.randint(1, len(numbers) - 1)
        numbers = insert_string(numbers, idx, '-')
    if multiply:
        idx = random.randint(1,len(numbers)-1)
        while not numbers[idx].isdigit() and numbers[idx+1].isdigit():
            idx = random.randint(1, len(numbers) - 1)
        numbers = insert_string(numbers, idx, '*')
    if divide:
        idx = random.randint(1,len(numbers)-1)
        while not numbers[idx].isdigit() and numbers[idx+1].isdigit():
            idx = random.randint(1, len(numbers) - 1)
        numbers = insert_string(numbers, idx, '/')
    if parentheses:
        idx1 = len(numbers)-1
        while idx1 == len(numbers) - 1 or not numbers[idx1+1].isdigit():
            idx1 = random.randint(0,len(numbers)-1)

        numbers = insert_string(numbers, idx1, '(')
        idx2 = random.randint(idx1 + 2, len(numbers))
        while not numbers[idx2-1].isdigit():
            idx2 = random.randint(idx1 + 2, len(numbers))
        numbers = insert_string(numbers, idx2, ')')
    return numbers


def find_digit_sequences(s):
    result = []
    start_index = None
    for i, char in enumerate(s):
        if char.isdigit():
            if start_index is None:
                start_index = i  # mark the start of a sequence
        else:
            if start_index is not None:
                result.append([start_index, i - start_index])  # add the sequence
                start_index = None  # reset for the next sequence
    if start_index is not None:  # Handle case where string ends with digits
        result.append([start_index, len(s) - start_index])
    return result

# Example usage:
s = "abc123xyz4567abc89"
sequences = find_digit_sequences(s) #[[3, 3], [9, 4], [15, 2]]


def perform_actions(string: str) -> float:

    return eval(string)


def insert_multi_if_needed(string: str) -> str:
    idx = string.find("(")
    if string[idx-1].isdigit():
        string = insert_string(string, idx, "*")
    idx = string.find(")")
    try:
        if string[idx+1].isdigit():
            string = insert_string(string, idx+1, "*")
    except IndexError:
        pass
    return string


#Example
data = []
for i in range(100000):
    puzzle = insert_operations('123456789')
    puzzle_ = insert_multi_if_needed((puzzle))
    try:
        result = perform_actions(puzzle_)
        if result > 0:
            if result.is_integer():
                data.append([puzzle, int(result), 'int'])
            else:
                data.append([puzzle, result, 'float'])
    except (SyntaxError, ZeroDivisionError):
        pass


df = pd.DataFrame(columns=['string', 'result', 'type'], data = data)
df = df[df['type']=='int'][['string', 'result']]
df.sort_values(by='result', inplace=True)
print(df.head(15))