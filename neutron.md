Installing Neutron Drive
========

First log into your google account. Then go to the following url in chrome and install neutron drive

https://chrome.google.com/webstore/detail/neutron-drive/lanjfnanlbolmgmnchmhfnicfefjgnff?hl=en-US

Next install secure shell in chrome

https://chrome.google.com/webstore/detail/secure-shell/pnhechapfaindjhompbnflcldabbghjo?hl=en-US

Now open secure shell and ssh into your server. For this class your username is student and your server is s#.2pi.nu and you'll get your password from the instructor.

Once in the shell, start by changing your password. 

```bash
passwd
```

You'll be prompted for a password twice. Then start neutron beam.

```bash
nbeam start
```

You'll be asked for your email address (use the same as you google account above) and a directory. Enter the following directory:

```bash
/home/student/
```

This is where your home directory. Now you need to connect neutron drive to neutron beam. Highlight the key and it will be put on the clipboard. Open neutron drive in chrome. Click the gear in the top right corner, then click "Neutron beam servers". Type in the same url above as you used to ssh into your server (s#.2pi.nu). Then paste the server key into the appropriate field. Hit save then close. You should now be able to click on the server name to the right and edit files on the server.
