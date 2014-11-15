from pprint import pprint
from PIL import Image
import string

input_file = 'input.txt'
end_of_message = '%!~'
stats = False
input_text = open(input_file).readlines()

def _log(x, message=''):
    if message != '': message += ':'
    open('debug.txt', 'a').write(message + x + '\n')

def clean_image(image_name):
    im = Image.open(image_name)

    #for every pixel clear the last bit of each RGB value
    #done by assuring the pixel values are even numbers
    l,w = im.size

    for x in range(l):
        for y in range(w):
            r,g,b = im.getpixel((x,y))
            #set the pixels to even numbers
            r = (r/2)*2
            g = (g/2)*2
            b = (b/2)*2
            
            im.putpixel((x,y), (r,g,b))

    im.save(image_name)

    im.close()

def compression_ratio(len_bin, len_full):
    return (1 - len_bin / float(len_full))

def determine_bit(color, index, binary_string):
    #if the index is out of the bounds of the string, color is unchanged
    if index >= len(binary_string):
        return color

    #the binary value in the string determines if the color is odd or even
    if binary_string[index] == '1':
        return color + 1
    return color

def put_message(text, image_name):
    import compress
    compress.create_encoding(compress.create_encoding_source(input_text))
    binary_string = compress.compress(text + end_of_message)

    # header will be binary encoding for each character
    # ie
    # spot 1 will be the first in compress.POSSIBLE_CHARACTERS
    # and binary based on encoding
    # NOTE: all characters will take up 8 bits, so it is absolute spacing -> needed to parse
    header = ''
    for ch in compress.POSSIBLE_CHARACTERS:
        header += compress.encoding[ch].rjust(8, '0')

    binary_string = header + binary_string

    if stats:
        print 'Placing encoding in image.'

    len_full = len(text + end_of_message) * 8
    len_bin = len(binary_string) - len(header)

    if stats:
        print 'Overhead of {0} bits required to send the encoding'.format(len(string.printable) * 8)
        print 'Compressed {0} bits to {1}'.format(len_full, len_bin)
        print 'Compression ratio is {0}%'.format(round(100 * compression_ratio(len_bin, len_full), 5))
        print 'Need {0} pixels to send {1} bits'.format(len(binary_string)/3, len(binary_string))

    #place binary in last position for each RGB value for each pixel
    #placement is linear

    i = 0 #index in binary of message
    im = Image.open(image_name)
    l,w = im.size
    if stats: print l * w, 'pixels are available for use'

    #check to make sure image can fit message
    if l * w < len(binary_string)/3 + 1:
        print 'Cannot send message in this image.  Need a larger image'
        im.close()
        exit()

    for x in range(l):
        for y in range(w):
            r,g,b = im.getpixel((x,y))

            r = determine_bit(r,i,binary_string)
            i += 1
            g = determine_bit(g,i,binary_string)
            i += 1
            b = determine_bit(b,i,binary_string)
            i += 1

            im.putpixel((x,y), (r,g,b))

    im.save(open(image_name, 'wb'))
    im.close()


def send(image_name, message):
    clean_image(image_name)
    put_message(text=message, image_name=image_name)

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', help='Image to extract message from', required=True)
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    parser.add_argument('-s', '--source', help='Source text file', required=True)
    args = vars(parser.parse_args())

    if args['verbose']: stats = True

    message = ''.join(open(args['source']).readlines())    
    send(args['image'], message)