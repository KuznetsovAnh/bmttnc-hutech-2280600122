from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi
import sys
import requests

class MyApp(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("./ui/caesar.ui", self)

        self.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.txt_plain_text.toPlainText(),
            "key": self.txt_key.text()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.txt_cipher_text.setText(data["encrypted_message"])
                self._show_message("Encrypted Successfully")
            else:
                self._show_message("Error while calling API")
        except requests.exceptions.RequestException as e:
            self._show_message(f"Request failed: {e}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.txt_cipher_text.toPlainText(),
            "key": self.txt_key.text()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.txt_plain_text.setText(data["decrypted_message"])
                self._show_message("Decrypted Successfully")
            else:
                self._show_message("Error while calling API")
        except requests.exceptions.RequestException as e:
            self._show_message(f"Request failed: {e}")

    def _show_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
