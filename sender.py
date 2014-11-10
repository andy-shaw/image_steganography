from pprint import pprint
from PIL import Image
import string
import binascii

input_file = 'input.txt'
end_of_message = '%!~'
stats = True
input_text = open(input_file).readlines()

h2b = {
    '0' : '0000',
    '1' : '0001',
    '2' : '0010',
    '3' : '0011',
    '4' : '0100',
    '5' : '0101',
    '6' : '0110',
    '7' : '0111',
    '8' : '1000',
    '9' : '1001',
    'a' : '1010',
    'b' : '1011',
    'c' : '1100',
    'd' : '1101',
    'e' : '1110',
    'f' : '1111',
}

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

    # place encoding at the head of the string
    temp = ''
    for ch in compress.encoding:
        #use existing tool to convert encoding to hex string
        temp += binascii.hexlify(ch)

    header = ''
    for ch in temp:
        #convert hex string to binary
        header += h2b[ch]

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
    put_message(message, image_name)

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    
    if len(args) <= 0:
        print 'USAGE: python sender.py <image_name>'
        exit()

    # send(image_name=args[0], message='TEST')
    send(image_name=args[0], message=''.join(open('input.txt').readlines()))