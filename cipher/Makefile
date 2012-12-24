all: ui_cipher.py

ui_cipher.py : cipher.ui
	pyside-uic cipher.ui  > ui_cipher.py

clean:
	rm -f ui_cipher.py *.pyc
