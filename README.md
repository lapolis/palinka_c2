# palinka_c2 v0.1
Why am I doing this? Cause I recently started using CobaltStrike for red team operations but I still define as "magic" most of the things that it does behind the scene. So, this is my way to understand things through blood and pain.  
I decided to start this things after I read a tweet by [0xBoku](https://twitter.com/0xBoku) saying he was developing a small C2 for initial access and, right after that, I saw this amazing [article/guide](https://0xrick.github.io/misc/c2/) by [Ahmed Hesham](https://twitter.com/ahm3d_h3sham); so at that point I thought to just *"borrow"* the code from [0xRick](https://github.com/0xRick/c2) and focus on the implant side.. But things got out of hand.. And here I am, presenting the umpteenth C2 which will slowly die while dependencies will break and functionality will get obsolete.  
  
This tool has been developed and tested on Linux but it **should** be multi platform, let me know if you find out :)
### General boring stuff
When the option `-j` is used, all the others are ignored. This function is used to just_decrypt a project so you will have sqlite3 DB nicely decrypted for you on disk.  
If you use `-p` DO NOT pass the password in the command line, you will be prompted for password.  
The use of password (encrypted DB) is not mandatory, so you can just run palinka C2 with `-f <project name>` only.  
If you want to keep all the debug logs from Flask (Requests log) used the flag `-d` and you will have a nice `./debug.log` file.

```
usage: palinka_c2.py [-h] [-f FILE_NAME] [-d] [-p] [-j JUST_DECRYPT]

Welcome to palinka_c2

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_NAME, --file_name FILE_NAME
                        This name will be used to create the DB with all the logs and information. Letters, numbers and . _ only.
  -d, --debug           Activate debugging. Everything will be saved in the file ./debug.log.
  -p, --password        Encrypt DB with password. Password will be asked later.
  -j JUST_DECRYPT, --just_decrypt JUST_DECRYPT
                        Just decrypt the DB file and save on disk.
```
The project name / file name will be used to create a Sqlite3 DB that will hold all the information about listeners, encryption keys, agents, commands and so on. The structure is is very simple (so far), easy to explore with sqlitebrowser. 
The terminal based main menu presents 4 tabs in which you can find all very basic functionalities of a C2 server.  
To navigate between tabs you can use `a` to go left and `d` to go right (ever played cod?).  
All the tabs are very self explanatory so you go and have fun.  
When you will have some agents and you want to check the full list of sent commands with relevant responses just go on the `Overview` tab and choose the agent you want to query. At that point, just pretend you are using `less`. Well, almost.. Actually, not even close. You can just scroll up and down basically :).. You can use the arrows or `w` for up and `s` for down. To skip pages just use `PgUp` and `PgDn`. Once you are done with it just press `q` or `Esc`.  
# Starting Listeners
### HTTP/HTTPS
The HTTP/HTTPS listener consists on a Flask web app composed by the following endpoints:
```
# new beacon registration
/beacon/register
# Agent querying for tasks to execute (name is the agent name)
/tasks/<name>
# Agent submitting the result of the executed task (code is the task unique code)
/results/<code>
# Agent grabbing files to download (simply doing wget for now)
/download/<file>
```
This is NOT MEANT to be a very OPSEC setup. A malleable kinda profile will (maybe) follow sooner or later.
To create a new HTTP/HTTPS listener got to Listeners > New Listener and input the info following this syntax:
```
<HTTPS|HTTP> <listener name> <IP> <PORT>
```
At this point, if everything went well, you will find it in the "Show Listeners" menu.
# Setup
### The usual "installation"
```
git clone https://github.com/lapolis/palinka_c2.git
cd ./palinka_c2
pip install -r ./requirements.txt
```
### Getting certs ready (for HTTPS listener)
#### Self signed cert
```
mkdir ./certs
openssl req -x509 -newkey rsa:4096 -nodes -out ./certs/cert.pem -keyout ./certs/key.pem -days 365
```
#### Legit cert
```
sudo certbot --manual --preferred-challenges dns certonly -d www.<domain> -d <domain>
```
The copy the cert file and private key to the `certs` folder.
```
mkdir ./certs
sudo cp /etc/letsencrypt/live/<DOMAIN>/fullchain.pem ./certs/cert.pem
sudo cp /etc/letsencrypt/live/<DOMAIN>/privkey.pem ./certs/key.pem
sudo chown $USER: ./certs/*
```
___

# Change log
### v0.1.1
Implementations:
- Download function
- Upload function

Fixies:
- Fixed file upload error on file with space in the name

### v0.1.0
All the main functionalities are up and running.

Well, from now on, it just works.
Added functionalities:
- Some fixes here and there
- Users can choose between HTTP and HTTPS
- Listener nice info preview
- Auto generate powershell implant
- Agents use listener enc key only for init, then switch to agent key
- Can encrypt DB
- Added few args
### v0.0.2
Added functionalities:
- Interactive menu
- Tabbed menu (hopefully) like d4rk3r likes xD
- Listener menu w/ all functionalities
- User can create listeners
- Send commands to HTTPS listener
- Implemented ssl
- Ready to go?
### v0.0.1
Added functionalities:
- Store commands
- Store command/output history
- Store encryption key for each listener
- Download/Upload file function (Flask side)
- Crypto module brutally copied from [0xRick](https://github.com/0xRick/)'s own [c2](https://github.com/0xRick/c2/blob/master/core/encryption.py)
- Powershell crypto module from [ctigeek](https://gist.github.com/ctigeek/2a56648b923d198a6e60) which is actually the same as 0xRick's one
- Stash module created and improved
- Accepting requests
