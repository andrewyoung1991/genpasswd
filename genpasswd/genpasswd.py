#!/usr/bin/python
from __future__ import absolute_import

import os
from subprocess import call as check, Popen, PIPE
import pyperclip
import getpass
import stat as st
from hashlib import pbkdf2_hmac, sha1
from binascii import b2a_uu


USERHOME = os.environ.get("HOME")
PASSWORD_FILE = os.path.join(USERHOME, ".mastpass")


class OneWayPassword(object):
    def __init__(self, keyphrase, length=16):
        self.keyphrase = keyphrase
        self.length = length
        self.alg, self.salt = get_salt()

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.keyphrase)
    __str__ = __repr__

    def lock(self):
        passwd = pbkdf2_hmac(
            self.alg,
            bytes(self.keyphrase, "utf-8"),
            bytes(self.salt, "utf-8"),
            100000
        )
        return b2a_uu(passwd).decode("utf-8").strip(" \n")[:self.length]


def generate_master(password, encryption="sha256", force=False):
    """opens up the .mastpass file and adds encryption and salt
    """
    if not force and os.path.exists(PASSWORD_FILE):
        raise OSError("~/.mastpass file already exists!")
    salt = sha1(bytes(password, "utf-8")).hexdigest()
    with open(PASSWORD_FILE, "w") as master:
        master.write("{0}:{1}".format(encryption, salt))
    # this file is locked down to current user only
    os.chmod(PASSWORD_FILE, st.S_IRWXU)
    return salt


def confirm_credentials(password):
    check_salt = sha1(bytes(password, "utf-8")).hexdigest()
    _, salt = get_salt()
    return check_salt == salt


def get_salt():
    with open(PASSWORD_FILE, "r") as master:
        contents = master.read()
        alg, salt = contents.split(":")
    return alg, salt


def generate_password(keyphrase, length=16):
    return OneWayPassword(keyphrase, length)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog="genpasswd",
        description="genpasswd.py is a utility script for generating secure passwords based on a single password.",
        usage="genpasswd <keyphrase> [--length=16] [--encryption=sha256]",
        epilog="""
        based on a single password using an arbitrary keyphrase. the
        keyphrase itself should be something unique and easy to remember,
        as it is more or less a password (i.e. used to generate and
        retrieve passwords). for instance an email password might be most
        memorable if they keyphrase is the email address itself -> jon@doe.com
        """
    )
    parser.add_argument(
        "keyphrase",
        nargs='?', default=None,
        help="a keyphrase to generate and retrieve a password."
    )
    parser.add_argument(
        "-e", "--encryption",
        default="sha256",
        choices=("sha256", "sha1"),
        help="the prefered encryption method used when generating new passwords, defaults to sha256."
    )
    parser.add_argument(
        "-l", "--length",
        type=int, default=16,
        help="length of the password, defaults to 16 characters."
    )
    parser.add_argument(
        "-n", "--new_master",
        action="store_true",
        help=""
    )
    args = parser.parse_args()

    if not os.path.exists(PASSWORD_FILE):
        # ohh, this must be your first time ;)
        master_password = getpass.getpass("(Enter a master password): ")
        master_again = getpass.getpass("(Again): ")
        if master_password == master_again:
            generate_master(master_password, args.encryption)
        else:
            raise SystemExit("The passwords didn't match, exiting!")
    elif args.new_master:
        old = getpass.getpass("(Enter existing password): ")
        if not confirm_credentials(old):
            raise SystemExit("The password entered didn't match, exiting!")
        new_master = getpass.getpass("(Enter a new password): ")
        new_again = getpass.getpass("(Again): ")
        if new_master == new_again:
            generate_master(new_master, args.encryption, force=True)
        else:
            raise SystemExit("The passwords didn't match, exiting!")
    else:
        master_password = getpass.getpass("(Enter the master password): ")
        if not confirm_credentials(master_password):
            raise SystemExit("The password entered didn't match, exiting!")

    if args.keyphrase:
        passwd = generate_password(args.keyphrase, args.length)
        pyperclip.copy(passwd.lock())
        print("{0} -> copied to clipboard!".format(passwd))
    else:
        raise SystemExit("Nothing to generate, exiting!")
