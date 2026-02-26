import os
from datetime import date as d
from datetime import datetime as dt

TOPLEVEL_MENU = """What operation would you like to perform?
\t(0) Change directory
\t(1) Add suffix to filenames
\t(2) Add prefix to filenames
\t(3) Replace parts of filenames
\t(4) Add modification or creation date to filenames\n"""

SUBSET_MENU = """All files or a subset?
\t(1) All files in the current directory
\t(2) Subset of files in the current directory\n"""

SUBSET_HOW_MENU = """How would you like to subset?
\t(1) First n
\t(2) Last n
\t(3) Presence of substring in filename
\t(4) File type extension"""


def checkquit(userinput):
    if userinput == "quit":
        quit()


def takeinput(message):
    userinput = input(message).lower().strip()
    checkquit(userinput)
    return userinput


def dirchange_subroutine():
    newdir = input("Please enter the new directory\n")
    newdir = newdir.replace("'", "")
    newdir = newdir.replace('"', "")
    os.chdir(newdir)


def fileselect_subset_subroutine():
    userinput = takeinput(SUBSET_HOW_MENU)
    while not userinput.isnumeric() or userinput not in [1, 2, 3, 4]:
        userinput = takeinput("Please enter either 1, 2, 3, or 4")


def fileselect_subroutine():
    userinput = takeinput(SUBSET_MENU)
    while not userinput.isnumeric() or int(userinput) not in [1, 2]:
        userinput = takeinput("Please enter either 1 or 2")
    if int(userinput) == 1:
        print("Files to be renamed:\n\t" + "\n\t".join(os.listdir()))
        correct = takeinput("Does this look correct? (y/n)")
        while correct not in ["y", "n"]:
            correct = takeinput("Does this look correct? (y/n)")
        if correct == "y":
            return os.listdir()
        else:
            return None
    else:
        return fileselect_subset_subroutine()


def suffix_subroutine(files):
    pass


def prefix_subroutine(files):
    pass


def replacement_subroutine(files):
    pass


def dating_subroutine(files):
    pass


def main():
    curdir = os.getcwd()
    print(f"Current Directory: {curdir}")
    while True:
        if os.getcwd() != curdir:
            curdir = os.getcwd()
            print(f"Current Directory: {curdir}")
        firstchoice = takeinput(TOPLEVEL_MENU)
        if not firstchoice.isnumeric() or int(firstchoice) not in [0, 1, 2, 3, 4]:
            print("Please enter either 0, 1, 2, 3, or 4")
            continue
        files = None
        if int(firstchoice) == 0:
            dirchange_subroutine()
        else:
            files = fileselect_subroutine()
        if not files:
            continue
        if int(firstchoice) == 1:
            suffix_subroutine(files)
        if int(firstchoice) == 2:
            prefix_subroutine(files)
        if int(firstchoice) == 3:
            replacement_subroutine(files)
        if int(firstchoice) == 4:
            dating_subroutine(files)


if __name__ == "__main__":
    main()
