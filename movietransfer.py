#!/usr/bin/python3

import configparser
import os
from colorama import init, Fore, Back, Style
import shutil
from unrar import rarfile

init(autoreset=True)


def print_list():
    # this is calling a variable from different scope, not good
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


if __name__ == "__main__":
    # open a config file to read directory locations, or create the config file, if necessary
    try:
        cfg = configparser.ConfigParser()
        cfg.read("config.ini")
        movies_dir = cfg.get("directories", "movies_dir")
        torrents_dir = cfg.get("directories", "torrents_dir")

    except configparser.NoSectionError:
        print("no config file found!")
        print("Creating new config file...")
        movies_dir = input("Please enter the movies directory: ")
        torrents_dir = input("Please enter the torrents directory: ")

        cfg_ini = open("config.ini", "w+")
        cfg_ini.write("[directories]\n")
        cfg_ini.write("movies_dir = %s\n" % movies_dir)
        cfg_ini.write("torrents_dir = %s\n" % torrents_dir)

    # set dir to torrents directory
    os.chdir(torrents_dir)
    # list dirs/files in torrents directory
    listing = os.listdir()
    # list to hold dirs
    dirs = []
    # list to hold files
    files = []

    print("\n")

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
                # if name in dir list cd into dir and extract
                if listing[int(selection) - 1] in dirs:
                    os.chdir(listing[int(selection) - 1])
                    # create a listing of the directory and find the rar file
                    dir_list = os.listdir()
                    for entry in dir_list:
                        if entry[len(entry) - 4:] == ".rar":
                            print("Extracting...")
                            rar = rarfile.RarFile(entry)
                            rar.extractall()
                            # TODO check for extraction errors, etc?
                            print("extraction finished\n")
                    print("\nPlease type the new movie and directory name: ")
                    new_name = input()
                    print("You entered: " + new_name)
                    make_movie_dir(new_name)

                    # rereun dir list to find mkv, can probably increase efficiency here
                    dir_list = os.listdir()
                    for entry in dir_list:
                        if entry[len(entry) - 4:] == ".mkv":
                            old_file = entry
                            print(entry)

                    copy_movie(old_file, new_name)

                # in name in files list, move etc
                else:
                    new_name = input()
                    make_movie_dir(new_name)
                    old_file = "../pizza.mkv"
                    copy_movie(old_file, new_name)

            elif choice == 'no':
                print("chose again")
            else:
                print("Please type 'yes' or 'no'\n")
