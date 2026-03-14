class CaesarCipher:

    def encrypt_text(self, text, key):
        result = ""

        for char in text:
            if char.isalpha():
                shift = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - shift + key) % 26 + shift)
            else:
                result += char

        return result


    def decrypt_text(self, text, key):
        return self.encrypt_text(text, -key)