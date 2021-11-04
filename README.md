# palinka_c2 v0.1
Why am I doing this? Cause I recently started usign CobaltStrike for red team operations but I still define as "magic" most of the things that it does. So, this is my way to understand things.
I decided to start this things after I saw this [article](https://0xrick.github.io/misc/c2/), so yeah, thanks 0xRick!

## Changelog
### v0.1
Added listener functionalities:
- Store commands
- Store command/output history
- Store encryption key for each listener
- Doawnload/Upload file function
- Crypto module brutally copied from [0xRick](https://github.com/0xRick/)'s own [c2](https://github.com/0xRick/c2/blob/master/core/encryption.py)
- Powershell module from [ctigeek](https://gist.github.com/ctigeek/2a56648b923d198a6e60) which is actually the same as 0xRick's one
- Stash module created and improved
### v0.0
Very basic stuff:
- Accepting requests
