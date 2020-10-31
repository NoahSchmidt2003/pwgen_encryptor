import random
import string
from os import stat, remove

import pyAesCrypt
from pyAesCrypt import decryptStream

letterslow = string.ascii_lowercase
lettersupper = string.ascii_uppercase
puctation = string.punctuation
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
numbers2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
operators = [1, 2, 3, 4]


class pwgen:
    def __init__(self, numberslol, askuser):
        self.n = numberslol
        self.a = askuser
        self.list = []
        self.password = None
        if self.a == "y":
            self.attr = 3
        else:
            self.attr = 2

    def generator(self):
        global letter
        for i in range(self.n):
            randomly = operators[random.randint(0, self.attr)]
            if randomly == 1:
                letter = random.choice(letterslow)
            elif randomly == 2:
                letter = random.choice(lettersupper)
            elif randomly == 3:
                letter = numbers2[random.randint(0, 8)]
                letter = str(letter)
            elif randomly == 4:
                letter = random.choice(puctation)

            self.list.append(letter)
        self.password = ''.join(map(str, self.list))
        print(self.list)
        print(self.password)
        print("Das ist dein sicheres Passwort")

    def showpw(self):
        passwords = self.password
        return passwords


class encryptor:
    def __init__(self, file, pws):
        self.f = file
        self.p = pws
        endung = ".aes"
        self.fileaes = "".join((self.f, endung))
        self.bufferSize = 64 * 1024
        self.encFileSize = stat(self.f).st_size

    def encryptor(self):
        with open(self.f, "rb") as fIn:
            with open(self.fileaes, "wb") as fOut:
                pyAesCrypt.encryptStream(fIn, fOut, self.p, self.bufferSize)
                print("Deine Datei wurde erfolgreich verschluesselt du findest sie unter", self.fileaes, "wieder")

    def decryptor(self):
        with open(self.f, "rb") as fIn:
            try:
                with open("dataout.txt", "wb") as fOut:
                    decryptStream(fIn, fOut, self.p, self.bufferSize, self.encFileSize)
                    print("Deine Datei wurde erfolgreich entschuesselt du findest sie unter data.out wieder")
            except ValueError:
                print("Error die Datei konnte nicht entschuesselt werden")
                remove("dataout.txt")


if __name__ == "__main__":
    while True:
        print("Wilkommen zum En/decryptor und PW Gen 2.0")
        ask2 = input("Moechtest du ein PW generieren oder eine Datei verschluesseln oder entschluesseln pw/data\n:")
        if ask2 == "pw":
            numbers = int(input("Wie viele Zeichen soll dein zufaellig generiertes Passwort haben\n"))
            ask = input("Moechtest du auch solche Zeichen generieren /()+#  y/n\n:")
            pw = pwgen(numbers, ask)
            pw.generator()
        elif ask2 == "data":
            ask3 = input("Moechtest du eine Datei verschluessseln (encrypt) oder entschluesseln (decrypt)\n:")
            if ask3 == "encrypt":
                filename = input("Wie heisst deine Datei?\n:")
                ask = input("Moechtest du ein zufaellig generiertes Passwort haben y/n\n:")
                if ask == "y":
                    numbers = random.randint(15, 90)
                    pw2 = pwgen(numbers, ask)
                    pw2.generator()
                    password = pw2.showpw()
                else:
                    password = input(
                        "Wie lautet dein Masterpasswort\nAchtung schreibe dir dieses Passwort unbedingt auf einen "
                        "Zettel\n:")
                encrypt = encryptor(filename, password)
                encrypt.encryptor()
            elif ask3 == "decrypt":
                filename = input("Wie heisst deine Datei?\n:")
                password = input("Wie lautet dein Masterpasswort\n:")
                encrypt = encryptor(filename, password)
                encrypt.decryptor()
