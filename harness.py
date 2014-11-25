import sender, receiver
import string

image_file = 'images\\source.png'

try:
    message = open('input.txt').readlines()
except:
    print 'Unable to open input.txt'
    exit()

try:
    pic = open(image_file)
except:
    print 'Unable to open picture'
    exit()

print 'Input text from "input.txt"'
print 'Input image from "images/source.png"'

sender.stats = True

#clean input of unicode only characters
for i in range(len(message)):
    ch = 0
    while ch < len(message[i]):
        if message[i][ch] not in string.printable:
            message[i] = message[i][:ch] + message[i][ch+1:]
        ch += 1

sender.send(image_file, ''.join(message))

print '\nMessage placed, now retrieving\n'

text = receiver.receive(image_file)



if len(text) > 500:
    print 'Message Excerpt:\n' + '-'*45
    print text[:500]
else:
    print 'Message:\n' + '-'*45
    print text
print '-'*45
print 'Message Correctly Transferred:', text==''.join(message)