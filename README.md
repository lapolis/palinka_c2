# palinka_c2 v0.1
Why am I doing this? Cause I recently started using CobaltStrike for red team operations but I still define as "magic" most of the things that it does behind the scene. So, this is my way to understand things through blood and pain.  
I decided to start this things after I read a tweet by [0xBoku](https://twitter.com/0xBoku) saying he/they was/were developing a small C2 for initial access and, right after that, I saw this amazing [article/guide](https://0xrick.github.io/misc/c2/) by [Ahmed Hesham](https://twitter.com/ahm3d_h3sham); so at that point I tought to just borrow the code from [0xRick](https://github.com/0xRick/c2) and focus on the implant side.. But things got out of hand.. And here I am, presenting the umpteenth C2 which will slowly die while dependencies will break and functionality will get obsolete.  
### General boring stuff
The terminal based main menu presents 4 tabs in which you can find all the most commond functionalities of a C2 server. To navigate between tabs you can use:
```
# to go left
Ctrl+w
# to go right
Ctrl+e
```

 
# Setup
### The usual "installation"
```
gig clone https://github.com/lapolis/palinka_c2.git
cd ./palinka_c2
pip install -r ./requirements.txt
```
### Getting certs ready (for HTTPS listener)
#### Self signed cert
```
openssl req -x509 -newkey rsa:4096 -nodes -out /<palinka_c2 home folder>/certs/cert.pem -keyout /<palinka_c2 home folder>/certs/key.pem -days 365
```
#### Legit cert
```
sudo certbot --manual --preferred-challenges dns certonly -d www.<domain> -d <domain>
```
The copy the cert file and private key to the `certs` folder.
```
mkdir /<palinka_c2 home folder>/certs
sudo cp /etc/letsencrypt/live/<DOMAIN>/fullchain.pem /<palinka_c2 home folder>/certs/cert.pem
sudo cp /etc/letsencrypt/live/<DOMAIN>/privkey.pem /<palinka_c2 home folder>/certs/key.pem
sudo chown $USER: /<palinka_c2 home folder>/certs/*
```
___

# Changelog
### v0.3
Well, from now on, it just works.
Added functionalities:
- Some fixes here and there
- Users can choose between HTTP and HTTPS
- Listener nice info preview
- Auto generate powershell implant
- Agents use listener enc key only for init, then switch to agent key
- Can encrypt DB
- Added few args
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
- Powershell crypto module from [ctigeek](https://gist.github.com/ctigeek/2a56648b923d198a6e60) which is actually the same as 0xRick's one
- Stash module created and improved
### v0.0
Very basic stuff:
- Accepting requests
