#!/usr/bin/env python2.7

# Copyright 2012, Ed Campbell
# All rights reserved.

# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:

# Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.

# Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
import string

import PySide
from PySide.QtGui import QApplication, QMainWindow, QMessageBox

from ui_cipher import Ui_MainWindow


ENCODE = 0
DECODE = 1


class Caesar(object):
    def __init__(self, offset=0):
        self.offset = offset

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        if isinstance(offset, basestring):
            self._offset = string.ascii_lowercase.index(offset.lower())
        else:
            self._offset = offset

    def decode(self, cipher):
        return self.transform(cipher, DECODE)
    
    def encode(self, cipher):
        return self.transform(cipher, ENCODE)

    def transform(self, text, direction):
        if direction == ENCODE:
            offset = self.offset
        elif direction == DECODE:
            offset = -self.offset
        else:
            raise ValueError('Unknown direction {!r}'.format(direction))

        res = ''
        for letter in text:
            if letter in string.ascii_letters:
                index = (string.ascii_lowercase.index(letter.lower()) +
                         offset) % len(string.ascii_lowercase)
                replacement = string.ascii_lowercase[index]
                if letter.isupper():
                    replacement = replacement.upper()
            else:
                replacement = letter
            res += replacement
        return res


class Vigenere(object):
    def __init__(self, keyword):
        self.keyword = keyword

    def decode(self, cipher):
        return self.transform(cipher, DECODE)
    
    def encode(self, cipher):
        return self.transform(cipher, ENCODE)

    def transform(self, cipher, direction):
        keyword_index = 0
        plaintext = ''
        for letter in cipher:
            plaintext +=  Caesar(self.keyword[keyword_index]).transform(letter,
                direction)
            # If ascii letter then move along the keyword.
            if letter in string.ascii_letters:
                keyword_index = (keyword_index + 1) % len(self.keyword)
        return plaintext


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.decode_pushButton.setEnabled(False)
        self.encode_pushButton.setEnabled(False)

        self.action_About.triggered.connect(self.about)
        self.decode_pushButton.clicked.connect(self.decode)
        self.encode_pushButton.clicked.connect(self.encode)
        self.keyword_lineEdit.textChanged.connect(self.updateActions)
        self.plain_textEdit.textChanged.connect(self.updateActions)
        self.cipher_textEdit.textChanged.connect(self.updateActions)

    def about(self):
        """Popup a box with about message."""
        QMessageBox.about(self, 'About cipher',
                          '''<b> Cipher </b>
                          <p>Copyright &copy; 2012 Ed Campbell.</p>
                          <p>Vigenere encoder/decoder.</p>''')

    def decode(self):
        keyword = self.keyword_lineEdit.text()
        ciphertext = self.cipher_textEdit.toPlainText()
        self.plain_textEdit.setPlainText(Vigenere(keyword).decode(ciphertext))

    def encode(self):
        keyword = self.keyword_lineEdit.text()
        plaintext = self.plain_textEdit.toPlainText()
        self.cipher_textEdit.setPlainText(Vigenere(keyword).encode(plaintext))

    def updateActions(self):
        if self.keyword_lineEdit.text():
            self.decode_pushButton.setEnabled(bool(self.cipher_textEdit.toPlainText()))
            self.encode_pushButton.setEnabled(bool(self.plain_textEdit.toPlainText()))
        else:
            self.decode_pushButton.setEnabled(False)
            self.encode_pushButton.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()

