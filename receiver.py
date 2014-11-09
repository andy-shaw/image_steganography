from PIL import Image

end_of_message = '%!~'
input_text = open('input.txt').readlines()
input_text.extend([end_of_message])


def retrieve_message(image_name):
    import compress
    compress.create_encoding(compress.create_encoding_source(input_text))
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

def receive(image_name):
    message = retrieve_message(image_name)
    shred_message(image_name)

    return message

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    
    if len(args) <= 0:
        print 'USAGE: python receiver.py <image_name>'
        exit()

    print receive(args[0])