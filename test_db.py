import unittest
import os
import sqlite3
import database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Use a temporary test database
        database.DB_NAME = 'test_vocab.db'
        if os.path.exists('test_vocab.db'):
            os.remove('test_vocab.db')
        
        # Monkeypatch database.sqlite3.connect to use test_vocab.db
        self.original_connect = sqlite3.connect
        database.sqlite3.connect = lambda name: self.original_connect('test_vocab.db')
        database.init_db()

    def tearDown(self):
        # Cleanup
        if os.path.exists('test_vocab.db'):
            os.remove('test_vocab.db')
        database.sqlite3.connect = self.original_connect

    def test_add_and_get_words(self):
        user_id = 12345
        database.add_word(user_id, "Apfel", "Apple")
        database.add_word(user_id, "Hund", "Dog")
        
        words = database.get_words(user_id)
        self.assertEqual(len(words), 2)
        self.assertIn(("Apfel", "Apple"), words)
        self.assertIn(("Hund", "Dog"), words)

    def test_get_random_word(self):
        user_id = 12345
        database.add_word(user_id, "Katze", "Cat")
        
        word_data = database.get_random_word(user_id)
        self.assertIsNotNone(word_data)
        self.assertEqual(word_data[0], "Katze")
        self.assertEqual(word_data[1], "Cat")

    def test_empty_words(self):
        user_id = 999
        words = database.get_words(user_id)
        self.assertEqual(len(words), 0)
        
        word_data = database.get_random_word(user_id)
        self.assertIsNone(word_data)

if __name__ == '__main__':
    unittest.main()
