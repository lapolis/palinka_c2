# palinka_c2 v0.2
Why am I doing this? Cause I recently started using CobaltStrike for red team operations but I still define as "magic" most of the things that it does. So, this is my way to understand things through blood and pain.  
I decided to start this things after I saw this [article](https://0xrick.github.io/misc/c2/), so yeah, thanks 0xRick! Also thanks for the crypto function! 

# Setup
### Getting certs ready (for HTTPS listener)
#### Self signed cert
```
openssl req -x509 -newkey rsa:4096 -nodes -out ./certs/cert.pem -keyout ./certs/key.pem -days 365
```
#### Legit cert
```
sudo certbot --manual --preferred-challenges dns certonly -d www.<domain> -d <domain>
```
The copy the cert file and private key to the `certs` folder.
```
sudo cp /etc/letsencrypt/live/<DOMAIN>/fullchain.pem /<palinka_c2 home folder>/certs/cert.pem
sudo cp /etc/letsencrypt/live/<DOMAIN>/privkey.pem /<palinka_c2 home folder>/certs/key.pem
sudo chown $USER: /<palinka_c2 home folder>/certs/*
```
___

# Changelog
### v0.2
Added functionalities:
- Interactive menu
- Tabbed menu (hopefully) like d4rk3r likes xD
- Listener menu w/ all functionalities
- User can create listeners
- Send commands to HTTPS listener
- Implemented ssl
- Ready to go?
### v0.1
Added functionalities:
- Store commands
- Store command/output history
- Store encryption key for each listener
- Download/Upload file function (Flask side)
- Crypto module brutally copied from [0xRick](https://github.com/0xRick/)'s own [c2](https://github.com/0xRick/c2/blob/master/core/encryption.py)
- Powershell module from [ctigeek](https://gist.github.com/ctigeek/2a56648b923d198a6e60) which is actually the same as 0xRick's one
- Stash module created and improved
### v0.0
Very basic stuff:
- Accepting requests
