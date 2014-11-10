import sender, receiver
import string

message = open('input.txt').readlines()

#clean input of unicode only characters
for i in range(len(message)):
    ch = 0
    while ch < len(message[i]):
        if message[i][ch] not in string.printable:
            message[i] = message[i][:ch] + message[i][ch+1:]
        ch += 1

sender.send('images\\source.png', ''.join(message))

print '\nMessage placed, now retrieving\n'

text = receiver.receive('images\\source.png')


print 'Message:\n' + '-'*45
if len(text) > 2000:
    print text[:2000]
else:
    print text
print '-'*45
print 'Message Correctly Transferred:', text==''.join(message)