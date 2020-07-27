#!/usr/bin/python3

import os
from colorama import init, Fore, Back, Style
import shutil
import unrar

init(autoreset=True)

# TODO make global variables loaded from a file with movie dir and torrents dir
movies_dir = "/home/user/data2"

# set dir to torrents directory
os.chdir("/home/user/data2/torrents")
# list dirs/files in torrents directory
listing = os.listdir(".")
# list to hold dirs
dirs = []
# list to hold files
files = []

print("\n")


def print_list():
    for entry in listing:
        if entry[len(entry) - 4] == ".":
            print("\t" + Fore.RED + str(listing.index(entry) + 1) + ": " + entry)
            files.append(entry)
        else:
            print("\t" + str(listing.index(entry) + 1) + ": " + entry)
            dirs.append(entry)
    print("\n")


def make_movie_dir(name):
    print("new movie dir name is: " + name)
    try:
        path = os.path.join(movies_dir, name)
        os.mkdir(path)
    except FileExistsError:
        print("directory already exists")


def copy_movie(file, name):
    print(movies_dir + name)
    shutil.copy2(file, movies_dir + "/" + name)
    print("file copied and renamed")


print_list()

while True:
    selection = input(Fore.CYAN + "Choose file/directory from the list, type list to see the list, or 'q' to "
                                  "quit: ").lower()

    if selection == "list":
        print_list()
        print("\n")
    elif selection == 'q':
        print(Back.RED + "\n<---------- quitting! ---------->\n")
        break
    else:
        print("\nYou Chose: " + listing[int(selection) - 1] + "\n")
        choice = input("Is that correct? yes/no:  ").lower()
        if choice == 'yes':
            # do routine to create new directory, copy file, rename file
            print("\nPlease type the new movie and directory name: ")
            new_name = input()
            print("You entered: " + new_name)
            # TODO verify this is the correct choice before proceeding

            # if name in dir list cd into dir and extract

            # in name in files list, move etc
            make_movie_dir(new_name)

            # copy movie to new dir
            # temp file name for development
            old_file = "pizza.mkv"
            copy_movie(old_file, new_name)

        elif choice == 'no':
            print("chose again")
        else:
            print("Please type 'yes' or 'no'\n")

# TODO multithread/process this


    # if file
    # ask to rename, search movies dir for dir that already has name
    # if dir not found, create dir
    # copy file to new dir, ask to delete when done
    # if dir
    # chdir
    # search for files rars etc
    # if find movie file already present
    # ask if correct
    # rename
    # check and create dir in movies dir
    # copy file
    # ask to delete
    # if rar found
    # unrar, ask to verify
    # when unrar done, print success or not
    # search for file to rename
    # ask to rename
    # search movies for dir with this name
    # create dir if not present
    # copy file
    # ask to delete

# print("\n\n")
# print("Directories: ")
# print(dirs)
# print("\n")
# print("Files: ")
# print(files)

# Search dirs for mkv, avi, mp4
# if found, ask if this is what you are looking for


# rename file to user entered NAME

# mkdir in /home/user/data/movies/NAME

# copy file to /home/user/data/movies/NAME
