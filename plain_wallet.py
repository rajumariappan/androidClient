import configparser
import os
import base58
import bitcoin_asymmetric_encrypt


class PlainWallet(object):
    """An encapsulated wallet for notary stuff.
    """
    def __init__(self):
        self.file_name = 'notarywallet.data'
        self.section_name = 'NotaryWallet'
        self.private_key_hex = None
        self.private_key_wif = None
        self.private_key = None
        self.public_key=None
        self.public_address=None

    def sign(self, message):
        return bitcoin_asymmetric_encrypt.sign(self.get_private_key_wif(),message)


    def verify(self, message, signature):
        return bitcoin_asymmetric_encrypt.verify(signature,message,self.get_bitcoin_address())

    def get_private_key(self):
        return self.private_key

    def get_public_key(self):
        return bitcoin_asymmetric_encrypt.private_key_to_public_key(self.private_key_wif)

    def get_public_key_hex(self):
        return self.public_key.encode("hex")

    def get_bitcoin_address(self):
        return self.public_address

    def get_private_key_wif(self):
        return self.private_key_wif

    def wallet_exists(self):
        if os.path.exists(self.file_name) and os.path.isfile(self.file_name):
            return True
        else:
            return False

    def instance(self):
        if not self.wallet_exists():
            self.create_new_wallet()
        self.private_key_hex = self.read_private_key()
        self.private_key_wif = base58.base58_check_encode(0x80, self.private_key_hex.decode("hex"))
        self.public_key=bitcoin_asymmetric_encrypt.private_key_to_public_key(self.private_key_wif)
        self.public_address = bitcoin_asymmetric_encrypt.public_key_to_address(self.public_key)

    def create_new_wallet(self):
        private_key = os.urandom(32)
        private_hex = private_key.encode("hex")

        config = configparser.ConfigParser()
        config.add_section(self.section_name)
        config.set(self.section_name, 'private_key',  private_hex)

        with open(self.file_name, 'w') as configfile:
            config.write(configfile)

    def read_private_key(self):
        if self.wallet_exists():
            config = configparser.ConfigParser()
            config.read(self.file_name)
            if config.has_option(self.section_name, 'private_key'):
                private_hex = config.get(self.section_name, 'private_key')
                return private_hex
            else:
                raise ValueError('Private key does not exist!')
        else:
            raise ValueError('Wallet does not exist!')

    def generate_encrypted_private_key(self):
        private_key = os.urandom(32)
        private_hex = private_key.encode("hex")
        encrypted_hex = self.encrypt_to_hex(private_hex)
        return encrypted_hex

    def encrypt_to_hex(self, plaintext):
        return plaintext

    def decrypt_from_hex(self, ciphertext):
        return ciphertext
