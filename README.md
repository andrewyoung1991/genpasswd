# genpasswd.py

genpasswd is a minimal python script for generating and retrieving secure passwords from a master password and an *arbitrary key*.

### usage

genpasswd ships with a simple commandline interface `genpasswd`.

#### getting started

to get started with genpasswd run `genpasswd --new_master`. the password entered here will be the main entrance point into the `genpasswd` commandline interface from here on. if you ever want to change the master password (which is ill advised, as changing this will alter the way passwords are generated/retrieved in the future, making it virtually impossible to retrieve an old password *unless you change the master password back*), simply run `genpasswd --new_master` again.

#### generating and retrieving passwords

now that the master password is set up generating a new password will simply require a key. the key should be easy to remember, perhaps named after the account password you are creating. here i will generate a password for my github account by running `genpasswd andrewyoung1991@github.com`, this will copy an incredible password to your clipboard. if i logout of my github account i can simply run `genpasswd andrewyoung1991@github.com` again and paste the results in to log back in securely.

#### additional arguments

a few additional arguments are available throught the commandline interface. simply run `genpasswd --help` for more options.
