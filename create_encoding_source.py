import urllib
import compress

columns = 6

RAW_PASTE_URL_BASE = 'http://pastebin.com/raw.php?i='
PASTE_PAGES = [
    'CJ5ipU7W',
    'd4YQ6cWe',
    'uVb63Rd7',
    'BX8z8EE6',
    '1qjnwhFM',
    'AsEWaqE2',
    'Vn4VJnHE',
    '9qTtWKz1',
    'vKpnWQcp',
    'V0vmV9Dr',
    'gq3FMFGZ',
    'n8Y43FCi',
    '8NpT2y9k',
    'psj1Efqp',
    'MDb3xkqA',
    'vcQebtbC',
    'X32Av0Vd',
    '4tkKysWC'
]


if __name__ == '__main__':
    #read in a pastebin pages
    lines = []
    i = 0
    for page in PASTE_PAGES:
        i += 1
        print 'fetching {0} of {1} pages'.format(i, len(PASTE_PAGES))
        lines.extend(urllib.urlopen(RAW_PASTE_URL_BASE + page))

    ordering = compress.create_encoding_source(lines)

    i = 0
    f = open('encoding_source.txt', 'w')
    for ch in ordering:
        f.write(repr(ch) + ',')
        if i % columns == 0:
            f.write('\n')
        i += 1
    f.close()