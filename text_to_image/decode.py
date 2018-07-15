#!/usr/bin/env python3
from os import path
import sys
import argparse
import logging

from PIL import Image


from text_to_image.utilities import check_filename
from text_to_image.utilities import color_to_index


def decode(image_path):
    """
    Decode an image by converting pixel values back to characters.
    :param str image_path: Path to a png image file.
    :return str: Decoded text.
    """
    pixel_width = 8
    if not path.isfile(image_path):
        raise FileExistsError("Image file {0} does not exist. Cannot decode a nonexistent image".format(image_path))
    img = Image.open(image_path)
    decoded_text = ""
    build_char = [0] * 3
    index = 0
    for row in range(0, img.size[0] // pixel_width):
        for col in range(0, img.size[1] // pixel_width):
            pixel_value = img.getpixel((row * pixel_width, col * pixel_width))
            if pixel_value != (0, 0, 0):  # ignore 0 (NULL) values
                build_char[index] = pixel_value
                if index == 2:
                    # Build up the integer by combining three colors
                    decoded_text += decode_pixel(
                        color_to_index[build_char[0]] |
                        (color_to_index[build_char[1]] << 2) |
                        (color_to_index[build_char[2]] << 4))
                    index = 0
                else:
                    index += 1
    return decoded_text + "=="


def decode_pixel(pixel):
    if pixel < 0 or pixel > 63:
        raise ValueError("Number out of base64 range!")

    if pixel < 26:
        return chr(pixel + ord('A'))
    if pixel < 52:
        return chr(pixel - 26 + ord('a'))
    if pixel < 62:
        return chr(pixel - 52 + ord('0'))
    if pixel == 62:
        return '+'
    if pixel == 63:
        return '/'


def decode_to_file(image_path, file_path):
    """
    Take an encoded png image and produce a text file with the decoded text.
    :param str image_path: Path to a png image with encoded text to be extracted.
    :param str file_path: Path to file where decoded text will be stored. Should be a plain text file '.txt'.
    :return str: Path to output text file.
    """
    if not path.isfile(image_path):
        raise FileExistsError("Image file {0} does not exist. Cannot decode a nonexistent image".format(image_path))
    if image_path[-4:].lower() != ".png":
        raise TypeError("Image {0} must be a png image file with a '.png' file extension".format(image_path))
    file_path = check_filename(file_path)

    decoded_text = decode(image_path)
    with open(file_path, "w") as f:
        f.write(decoded_text)
    return file_path


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Decode text from an image and output to console to a text file.")
    parser.add_argument("image_path", action="store", help="Filename/path for the input image with the encoded text.",
                        type=str)
    parser.add_argument("-f", "--file", action="store", help="Path to text file where decoded text should be stored.",
                        type=str)
    args = parser.parse_args()

    if args.file is None:
        print(decode(args.image_path))
    else:
        output_file = decode_to_file(args.image_path, args.file)
        logging.info("File '{0}' has been created with the decoded text".format(output_file))
