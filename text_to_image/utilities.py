#!/usr/bin/env python3
import math

def check_filename(filepath, extension=".txt"):
    """
    Take a path to a file and ensure the filename has the right extension, else add the extension.
    :param str filepath: The path to the file.
    :param str extension: Extension for the given file. If wrong extension in filepath then raise error.
    Extension must start with '.'.
    :return str: The filepath with the correct extension.
    """
    if extension[0] != ".":
        raise ValueError("Parameter 'extension'  must start with a period e.g. '.txt'.")
    file_extension = filepath[-(len(extension)):].lower()  # get last part of filename to check extension
    extension = extension.lower()
    if file_extension != extension:
        # remove any trailing slashes at end of filepath
        while filepath[-1] == "/" or filepath[-1] == "\\":
            filepath = filepath[0:-1]
        filepath += extension
    return filepath


index_to_color = {
    0 : (255, 0, 0),   # Red
    1 : (0, 255, 0),   # Green
    2 : (0, 0, 255),   # Blue
    3 : (255, 127, 0)  # Orange
    }

# Keep this in sync with index_to_color
color_to_index = {
    (255, 0, 0) : 0,   # Red
    (0, 255, 0) : 1,   # Green
    (0, 0, 255) : 2,   # Blue
    (255, 127, 0) : 3  # Orange
    }

def convert_char_to_tuple(char, limit=256):
    """
    Take a character and return an integer value while ensuring the values returned do not go above the limit.
    :param str char: A single character.
    :param int limit: An integer representing the largest value which will start requiring reducing char value.
    (default=256).
    :return int: A number between 1 (0=NULL) and the limit that represents the int value of the char.
    """
    
    if char == '=':
        # '=' doesn't fit in our 64 characters. Just ignore them and add them back when decoding
        return []
    b64 = char_to_int(char)
    return [
        index_to_color[b64 & 3],
        index_to_color[(b64 & (3 << 2)) >> 2],
        index_to_color[(b64 & (3 << 4)) >> 4]
    ]

    
def char_to_int(char):
    # Ascii doesn't map evenly with base64 character set
    # Lets make A-Za-Z map to 0-51, 0-9 map to 52-61,
    # '+' to 62, and '/' to 63
    if char >= 'A' and char <= 'Z':
        return ord(char) - ord('A')
    if char >= 'a' and char <= 'z':
        return ord(char) - ord('a') + 26
    if char >= '0' and char <= '9':
        return ord(char) - ord('0') + 52
    if char == '+':
        return 62
    if char == '/':
        return 63


def get_image_size(text_length):
    """
    Take the length of text to be encoded and get the width, height of the resulting image.
    Must account for a null terminator at the end of the image.
    Tries to get the best resolution so that width and height values are as close as possible.
    :param int text_length: The length of text to be encoded as an image.
    :return (int, int): width, height of the image.
    """

    if True:
        # Don't bother trying to find the best fit. I'd rather have squares with some black than some "optimized" 3x100 image
        min_length = text_length
        root = int(math.sqrt(min_length))
        if root * root >= min_length:
            return (root, root)
        if root * (root + 1) >= min_length:
            return (root, root + 1)
        return (root + 1, root + 1) # This is guaranteed to be larger than min_length


if __name__ == "__main__":
    pass
