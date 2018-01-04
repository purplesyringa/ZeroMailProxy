# ZeroMailProxy

A fast, lightweight server for [ZeroMail](https://github.com/HelloZeroNet/ZeroMail), written in Python.

## Installation and usage

Linux:
```bash
$ git clone https://github.com/imachug/ZeroMailProxy
$ cd ZeroMailProxy
$ sudo python pop.py # Run local POP3 server
$ sudo python smtp.py # Run local SMTP server
```

Windows:
```
> git clone https://github.com/imachug/ZeroMailProxy
> cd ZeroMailProxy
> python pop.py # Run local POP3 server
> python smtp.py # Run local SMTP server
```

## Local servers

POP3 server is finished. To make it work, configure your mail clinet to use `localhost:110` with login `local` and password `local`.

## Example for Windows Mail client

1. Run POP3 server
2. Run Windows Mail  
![Windows Mail](images/winmail/1.png)  
3. Press *Accounts* and then *+ Add account*
4. Scroll to very bottom and choose *Advanced setup*  
![Advanced setup](images/winmail/2.png)  
5. Choose *Internet email*  
![Internet email](images/winmail/3.png)  
6. Set:  
![1](images/winmail/4.png)  
    - *Email address* to `<yourzeroid>@zeroid.bit`
    - *User name* to `local`
    - *Password* to `local`
    - *Account name* to anything you want  
![2](images/winmail/5.png)  
    - *Send your messages using this name* to `local`
    - *Incoming email server* to `localhost`
    - *Account type* to `POP3`
    - *Outgoing (SMTP) email server* to `localhost`  
![3](images/winmail/6.png)  
    - Uncheck *Require SSL for incoming email*
    - Uncheck *Require SSL for outgoing email*
7. Press *Sign in*
8. Press *Done*  
![Done](images/winmail/7.png)
9. Wait until your mail is synchronized

## Example for ThunderBird

1. Run POP3 server
2. Run SMTP server
3. Open ThunderBird  
![ThunderBird](images/thunderbird/1.png)  
4. Open *Menu* -> *Options* -> *Account Settings*  
![ThunderBird](images/thunderbird/2.png)  
5. Press *Account Actions* -> *Add Mail Account...*  
![ThunderBird](images/thunderbird/3.png)  
6. Set *Your name* to anything you want, *Email address* to `<yourzeroid>@zeroid.bit`, *Password* to `local` and press `Continue`  
![ThunderBird](images/thunderbird/4.png)  
7. ThunderBird will try to configure everything manually - stop that by pressing *Manual config*
8. Set:
    - *Incoming* to `POP3 | localhost | 110 | None | Normal password`
    - *Outgoing* to `SMTP | localhost | 587 | None | Normal password`
    - *Username* to `local | local`  
![ThunderBird](images/thunderbird/5.png)  
9. Press *Re-test* and then *Done*
10. Accept warning  
![ThunderBird](images/thunderbird/6.png)  
11. Close menu and press *Get messages*

## Command-line client

*Coming soon*
