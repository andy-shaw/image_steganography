from PIL import Image
import string

end_of_message = '%!~'
input_text = open('input.txt').readlines()
input_text.extend([end_of_message])

def _log(x, message=''):
    if message != '': message += ':'
    open('debug.txt', 'a').write(message + x + '\n')

def retrieve_message(image_name):
    import compress
    from pprint import pprint

    im = Image.open(image_name)
    l,w = im.size

    binary_string = ''

    #for each pixel retrieve the bit
    for x in range(l):
        for y in range(w):
            r,g,b = im.getpixel((x,y))

            if r%2 == 1:
                binary_string += '1'
            else:
                binary_string += '0'

            if g%2 == 1:
                binary_string += '1'
            else:
                binary_string += '0'

            if b%2 == 1:
                binary_string += '1'
            else:
                binary_string += '0'


    #encoding is in the first 800 bits and contains all of compress.POSSIBLE_CHARACTERS
    header = binary_string[:800]

    binary_string = binary_string[800:]

    # each byte of header contains the encoding for the character
    # in order of compress.POSSIBLE_CHARACTERS
    temp = []
    i = 0
    for ch in compress.POSSIBLE_CHARACTERS:
        temp.append((header[i:i+8], ch))
        i += 8

    # sorted binary puts them in order of encoding
    # creating list so that source_encoding meets the compress encoding parameter reqs
    source_encoding = []
    for x,y in sorted(temp):
        source_encoding.append(y)

    compress.create_encoding(source_list=source_encoding)

    #truncate string to message
    #from end of string, go left until end_of_message is encountered

    #get binary of end of message
    bin_end_of_message = compress.compress(end_of_message)
    i = binary_string.find(bin_end_of_message)
    binary_string = binary_string[:i]


    return compress.decompress(binary_string)

def shred_message(image_name):
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

def receive(image_name, filename=None):
    message = retrieve_message(image_name)
    shred_message(image_name)

    if filename:
        open(filename, 'w').write(message)
    return message

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', help='Image to extract message from', required=True)
    parser.add_argument('-o', '--output', help='Output file', required=False)
    args = vars(parser.parse_args())

    if args['output']:
        filename = args['output']
        receive(args['image'], filename)
    else:
        filename = None
        print receive(args['image'], filename)