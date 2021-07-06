import random
import zipfile
import string


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def ziplist(files):
    zipped = zipfile.ZipFile("./upload/output/output.zip", 'w')
    for i in files:
        zipped.write(i)
    zipped.close()