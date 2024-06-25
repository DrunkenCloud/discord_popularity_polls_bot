import random
import csv

def find_similar_char(char_list, target_popularity, tolerance=1000):
    """
    Find a character in the list whose popularity is within the given tolerance of the target popularity.
    """
    similar_chars = [char for char in char_list if abs(char[1] - target_popularity) <= tolerance]
    if not similar_chars:
        return None
    return random.choice(similar_chars)

def select_two_characters(char_list, tolerance=10):
    """
    Select a character randomly and find another character whose popularity is within the tolerance range.
    """
    if len(char_list) < 2:
        raise ValueError("The list must contain at least two characters.")

    # Randomly select a character
    selected_char = random.choice(char_list)
    char_list_without_selected = [char for char in char_list if char != selected_char]

    # Find another character with popularity close to the selected character's popularity
    similar_char = find_similar_char(char_list_without_selected, selected_char[1], tolerance)

    # If no similar character is found within the tolerance, adjust the tolerance or handle as needed
    while similar_char is None:
        tolerance += 5  # Increase tolerance and try again
        similar_char = find_similar_char(char_list_without_selected, selected_char[1], tolerance)
    
    return selected_char, similar_char

def read_and_sort_csv(file_path):
    char_list = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            char_list.append([row[1], int(row[2]), row[3]])
    char_list.sort(key=lambda x: x[1])
    return char_list

if __name__ == '__main__':
    char_list = read_and_sort_csv('test_male.csv')
    print(char_list)
    selected_char, similar_char = select_two_characters(char_list, tolerance=10)
    print(f"Selected Character: {selected_char}")
    print(f"Similar Character: {similar_char}")
