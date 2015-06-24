import os
import unittest
from genpasswd import genpasswd


class PasswordFunctionTestCase(unittest.TestCase):
    def setUp(self):
        # lets patch the master file path
        genpasswd.PASSWORD_FILE = "/tmp/.testmastpass"
        self.master_pass = "testMaster123"
        self.salt = genpasswd.generate_master(self.master_pass)

    def tearDown(self):
        if os.path.exists(genpasswd.PASSWORD_FILE):
            os.remove(genpasswd.PASSWORD_FILE)

    def test_master_file(self):
        self.assertTrue(os.path.exists(genpasswd.PASSWORD_FILE))
        self.assertEqual(self.salt, genpasswd.get_salt()[-1])

    def test_change_master_password(self):
        salt = genpasswd.generate_master("newTestPasswd123", force=True)
        self.assertNotEqual(self.salt, salt)
        self.assertEqual(salt, genpasswd.get_salt()[-1])

    def test_oneway_password_lock(self):
        oneway = genpasswd.OneWayPassword("mygmailaccount", length=8)
        self.assertEqual(oneway.length, 8)
        self.assertEqual(oneway.keyphrase, "mygmailaccount")
        alg, salt = genpasswd.get_salt()
        self.assertEqual(alg, oneway.alg)
        self.assertEqual(salt, oneway.salt)
        passwd = oneway.lock()
        self.assertEqual(len(passwd), 8)

