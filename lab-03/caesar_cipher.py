import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow

def caesar_encrypt_local(text, key):
    try:
        k = int(str(key).strip()) % 26
    except Exception:
        k = 0
    out = []
    for ch in text:
        if 'a' <= ch <= 'z':
            out.append(chr((ord(ch)-97 + k) % 26 + 97))
        elif 'A' <= ch <= 'Z':
            out.append(chr((ord(ch)-65 + k) % 26 + 65))
        else:
            out.append(ch)
    return ''.join(out)

def caesar_decrypt_local(text, key):
    try:
        k = int(str(key).strip()) % 26
    except Exception:
        k = 0
    return caesar_encrypt_local(text, -k)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối các nút bấm với hàm xử lý
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def show_message(self, title, text, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.txt_plain_text.toPlainText(),
            "key": self.ui.txt_key.toPlainText()
        }

        try:
            response = requests.post(url, json=payload, timeout=3)
            response.raise_for_status()
            data = response.json()
            cipher = data.get("encrypted_message", "")
            self.ui.txt_cipher_text.setText(cipher)
            self.show_message("Thành công", "Đã mã hóa dữ liệu thành công!")
        except Exception as e:
            # fallback local và in lỗi để debug
            print("Encrypt API failed:", repr(e))
            cipher = caesar_encrypt_local(payload["plain_text"], payload["key"])
            self.ui.txt_cipher_text.setText(cipher)
            self.show_message("Lưu ý", "Đã mã hóa cục bộ (server không phản hồi).")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.txt_cipher_text.toPlainText(),
            "key": self.ui.txt_key.toPlainText()
        }

        try:
            response = requests.post(url, json=payload, timeout=3)
            response.raise_for_status()
            data = response.json()
            plain = data.get("decrypted_message", "")
            self.ui.txt_plain_text.setText(plain)
            self.show_message("Thành công", "Đã giải mã dữ liệu thành công!")
        except Exception as e:
            print("Decrypt API failed:", repr(e))
            plain = caesar_decrypt_local(payload["cipher_text"], payload["key"])
            self.ui.txt_plain_text.setText(plain)
            self.show_message("Lưu ý", "Đã giải mã cục bộ (server không phản hồi).")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())