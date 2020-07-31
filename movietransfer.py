#!/usr/bin/python3

import configparser
import os
from colorama import init, Fore, Back, Style
import shutil
from unrar import rarfile

init(autoreset=True)


def new_print_dir(dirname: str):
    ls = os.listdir(dirname)
    for entry in ls:
        if entry[len(entry) - 4] == ".":
            print("\t" + Fore.RED + str(listing.index(entry) + 1) + ": " + entry)
            files.append(entry)
        else:
            print("\t" + str(listing.index(entry) + 1) + ": " + entry)
            dirs.append(entry)


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
        print("\n")
        return new_name

    @staticmethod
    def make_movie_dir(new_directory_name):
        try:
            path = os.path.join(movies_dir, new_directory_name)
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
    def copy_movie(orig_movie_name: str, new_file_name):
        try:
            shutil.copy2(orig_movie_name, movies_dir + "/" + new_file_name)
            positive_outcome("Movie copied!")
        except:
            negative_outcome("An error has occurred during copying!")

    def rename_movie(self, original_name: str, new_dir_and_file_name: str):
        # new_dir_and_file_name = self.get_new_name()
        try:
            os.rename(movies_dir + "/" + new_dir_and_file_name + "/" + original_name,
                      movies_dir + "/" + new_dir_and_file_name + "/" + new_dir_and_file_name + ".mkv")
            positive_outcome("File has been renamed")
        except FileExistsError:
            negative_outcome("Directory/File already exists!")


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

    new_print_dir(os.getcwd())

    while True:
        # TODO create a "file locator" method to traverse choices and find a file, return file name to
        # send to movie operations class
        # TODO add support for mp4, avi, etc, find list of video types online and search list?
        # video_file_type_list = ["mkv", "avi", "mp4"]
        os.chdir(torrents_dir)

        selection = input(Fore.CYAN + "Choose file/directory from the list, type list to see the list, or 'q' to "
                                      "quit: ").lower()
        # TODO input validation, errors here depending on entry
        if selection == "list":
            new_print_dir(os.getcwd())
        elif selection in ['q', 'quit', 'qui', 'qu']:
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
                            movie_object = MovieOperations(entry)
                            movie_object.unrar_movie(movie_object.original_file_name)

                    new_dir_list = os.listdir()
                    for entry in new_dir_list:
                        if entry[len(entry) - 4:] == ".mkv":
                            movie_object = MovieOperations(entry)
                            new_name = movie_object.get_new_name()
                            movie_object.make_movie_dir(new_name)
                            # todo different name for entry?
                            movie_object.copy_movie(entry, new_name)
                            movie_object.rename_movie(entry, new_name)

                # in name in files list, move etc
                else:
                    file = listing[int(selection) - 1]
                    movie_object = MovieOperations(file)
                    new_name = movie_object.get_new_name()
                    movie_object.make_movie_dir(new_name)
                    movie_object.copy_movie(file, new_name)
                    movie_object.rename_movie(file, new_name)
                    os.chdir(torrents_dir)

            elif choice == 'no':
                print("choose again")

            else:
                print("Please type 'yes' or 'no'\n")
