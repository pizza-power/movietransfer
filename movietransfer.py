#!/usr/bin/python3

import configparser
import os
from colorama import init, Fore, Back, Style
import shutil
from unrar import rarfile

init(autoreset=True)


def print_list():
    # this is calling a variable from different scope, probably should change
    print("\n")
    for entry in listing:
        if entry[len(entry) - 4] == ".":
            print("\t" + Fore.RED + str(listing.index(entry) + 1) + ": " + entry)
            files.append(entry)
        else:
            print("\t" + str(listing.index(entry) + 1) + ": " + entry)
            dirs.append(entry)
    print("\n")


def copy_movie(file, name):
    shutil.copy2(file, movies_dir + "/" + name)
    os.rename(movies_dir + "/" + name + "/" + file, movies_dir + "/" + name + "/" + name + ".mkv")
    print("\n\t" + Fore.GREEN + "[+] file copied and renamed\n")


def positive_outcome(text: str):
    print(Fore.GREEN + "\t[+] " + Style.RESET_ALL + text)


def negative_outcome(text: str):
    print(Fore.RED + "\t[+] " + Style.RESET_ALL + text)


class MovieOperations:
    """A class for a file transfer including unrar'ing, renaming, making directories, etc"""

    def __init__(self, original_file_name):
        self.original_file_name = original_file_name

    @staticmethod
    def get_new_name():
        new_name = input("\nPlease type the new movie and directory name: ")
        return new_name

    @staticmethod
    def make_movie_dir(new_name):
        try:
            path = os.path.join(movies_dir, new_name)
            os.mkdir(path)
            positive_outcome(path + " created!")
        except FileExistsError:
            negative_outcome("directory already exists!")

    @staticmethod
    def unrar_movie(movie_to_unrar):
        try:
            rar = rarfile.RarFile(movie_to_unrar)
            rar.extractall()
            positive_outcome("Successfully extracted!")
        except:
            negative_outcome("Exception has occurred!")

    @staticmethod
    def copy_movie(movie_name: str):
        try:
            shutil.copy2(movie_name, movies_dir + "/" + name)
        except:
            negative_outcome("An error has occurred!")


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

    print_list()

    while True:
        # TODO create a "file locator" method to traverse choices and find a file, return file name to
        # send to movie operations class

        # TODO add support for mp4, avi, etc, find list of video types online and search list?

        # TODO during reslect after doing one operation, this fails because directories haven't been reset?
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
                            # extract with unrar
                            movie_to_transfer = MovieOperations(entry)
                            movie_to_transfer.unrar_movie(movie_to_transfer.original_file_name)

                    new_name = input("\nPlease type the new movie and directory name: ")
                    print("\n\tperforming actions\n")
                    make_movie_dir(new_name)

                    # rerun dir list to find mkv, can probably increase efficiency here by using some sort of list
                    # comparison or something?
                    dir_list = os.listdir()
                    for entry in dir_list:
                        if entry[len(entry) - 4:] == ".mkv":
                            old_file = entry
                            copy_movie(old_file, new_name)

                # in name in files list, move etc
                else:
                    new_name = input()
                    old_file = listing[int(selection) - 1]
                    print("old file is: %s" % old_file)
                    print("making new dir and copying file")
                    make_movie_dir(new_name)
                    copy_movie(old_file, new_name)

            elif choice == 'no':
                print("chose again")
            else:
                print("Please type 'yes' or 'no'\n")
