import zipfile

ZFile = zipfile.ZipFile('CrackMe.zip')
Verbose = 5
with open('dictionary.txt', 'rb') as PWords:
    for index, line in enumerate(PWords):
        try:
            pwd = line.strip(b'\n')
            pwd = pwd.strip(b'\r')
            ZFile.extractall(pwd=pwd)
        except RuntimeError:
            if index % Verbose == 0:
                print('{}. Password: {} is not a match.'.format(index + 1, pwd))
        else:
            print('{}. Found the password: "{}"'.format(index + 1, bytes.decode(pwd)))
            break

ZFile.close()