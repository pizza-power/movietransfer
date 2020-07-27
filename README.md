# movietransfer

Problem: 

I download movies and the file names are not as I want them. They also sometimes needed to be unrar'd. And they also needed to be renamed. I generally used the linux command line to do this, but it got cumbersome. I then made a bash script to automate/ease parts of it, but that was not optimal. 

Solution: 

This script (when finished) creates an ini file on first run containing variables for the final movie directory, and the initial torrents directory. These dirs will be loaded when the script is run in the future. 

The torrent dir is listed, and the user can select a file or directory. If the user selects a movie file, the corect final dir is created, and the file is copied there and renamed. 

If the user selects a dir containing rar files, the rar is unrar'd and then copied and renamed

TODO: 

Create a Transfer class to use in Multiprocessing
Multiprocessing would come in handy when unraring is occuring
Input validation/invalid characters in dir names
More error catching needed
