import time
import unittest
from datetime import datetime, timedelta

from atumm.extensions.services.tokenizer.paseto_tokenizer import PasetoTokenizer
from atumm.extensions.services.tokenizer.exceptions import ExpiredTokenException,\
    DecodeTokenException


class TestPasetoTokenizer(unittest.TestCase):
    def setUp(self):
        self.secret_key = "test_secret_key"
        self.expire_period = 1
        self.tokenizer = PasetoTokenizer(self.secret_key, self.expire_period)

    def test_encode(self):
        payload = {"sub": "test@example.com", "user_id": 123}
        token = self.tokenizer.encode(payload)
        self.assertIsInstance(token, str)

    def test_decode_valid_token(self):
        payload = {"sub": "test@example.com", "user_id": 123}
        token = self.tokenizer.encode(payload)
        decoded_payload = self.tokenizer.decode(token)
        self.assertEqual(decoded_payload["sub"], payload["sub"])
        self.assertEqual(decoded_payload["user_id"], payload["user_id"])

    def test_decode_invalid_token(self):
        invalid_token = "invalid.token.string"
        with self.assertRaises(DecodeTokenException):
            self.tokenizer.decode(invalid_token)

    def test_decode_expired_token(self):
        payload = {"sub": "test@example.com", "user_id": 123}
        token = self.tokenizer.encode(payload)
        # Wait for the token to expire
        time.sleep(2)
        with self.assertRaises(ExpiredTokenException):
            self.tokenizer.decode(token)


if __name__ == "__main__":
    unittest.main()
