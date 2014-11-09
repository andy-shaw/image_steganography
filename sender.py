from pprint import pprint
from PIL import Image

input_file = 'input.txt'
end_of_message = '%!~'
stats = True
input_text = open(input_file).readlines()
input_text.extend([end_of_message])

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

    if stats:
        print 'Compressed', len(text + end_of_message) * 8, 'bits to', len(binary_string)
        print 'Compression ratio is', round(100*(1 - len(binary_string)/float(len(text + end_of_message)*8)), 5), '%'
        print 'Need', len(binary_string)/3, 'pixels to send the message' 



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