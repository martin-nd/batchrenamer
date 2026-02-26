import os
import re
import shutil
from datetime import date as d
from datetime import datetime as dt
from datetime import timedelta as td

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
\t(4) File type extension\n"""

ADDITION_TYPE_MENU = """Which kind of affix would you like to add?
\t(1) Incrementer
\t(2) Static custom\n"""

INC_MENU = """Which kind of counter would you like to add?
\t(1) Integer
\t(2) Date\n"""

FINAL_RENAME_MENU = """Would you like to update filenames in a new subfolder or in place?
\t(1) Subfolder
\t(2) In place\n"""

MOD_CREATION_MENU = """Would you like to add the most recent modification date or the file creation date?
\t(1) Most recent modification date
\t(2) File creation date\n"""

DATE_SUFF_PRE_MENU = """Suffix or prefix?
\t(1) Suffix
\t(2) Prefix\n"""


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
    while not userinput.isnumeric() or int(userinput) not in [1, 2, 3, 4]:
        userinput = takeinput("Please enter either 1, 2, 3, or 4\n")
    files = sorted(
        [
            file
            for file in os.listdir()
            if os.path.isfile(file) and not file.startswith(".")
        ]
    )
    if int(userinput) in [1, 2]:
        numfiles = takeinput("How many?\n")
        while not numfiles.isnumeric() or int(numfiles) > len(files):
            numfiles = takeinput(
                "The number of files must be an integer less than or equal to the number of files in the directory\n"
            )
        if int(userinput) == 1:
            return files[: int(numfiles)]
        else:
            return files[::-1][: int(numfiles)][::-1]
    if int(userinput) == 3:
        substr = input('Please enter the substring, to use regex, prefix with ":re:"\n')
        if substr.startswith(":re:"):
            substr = substr[4:]
            return [file for file in files if re.search(substr, file)]
        else:
            return [file for file in files if substr in file]
    if int(userinput) == 4:
        extension = input("Please enter the file extension.\n")
        return [file for file in files if file.split(".")[-1] == extension]


def fileselect_subroutine():
    userinput = takeinput(SUBSET_MENU)
    while not userinput.isnumeric() or int(userinput) not in [1, 2]:
        userinput = takeinput("Please enter either 1 or 2\n")
    if int(userinput) == 1:
        files = sorted(
            [
                file
                for file in os.listdir()
                if os.path.isfile(file) and not file.startswith(".")
            ]
        )
        print("Files to be renamed:\n\t" + "\n\t".join(files))
        correct = takeinput("Does this look correct? (y/n)\n")
        while correct not in ["y", "n"]:
            correct = takeinput("Does this look correct? (y/n)\n")
        if correct == "y":
            return files
        else:
            return None
    else:
        files = fileselect_subset_subroutine()
        print("Files to be renamed:\n\t" + "\n\t".join(files))
        correct = takeinput("Does this look correct? (y/n)\n")
        while correct not in ["y", "n"]:
            correct = takeinput("Does this look correct? (y/n)\n")
        if correct == "y":
            return files
        else:
            return None


def affix_subroutine(files, affix_type):
    userinput = takeinput(ADDITION_TYPE_MENU)
    while not userinput.isnumeric() or int(userinput) not in [1, 2, 3]:
        userinput = takeinput("")
    if int(userinput) == 2:
        custom_affix = input("Please enter the custom affix\n")
        filename_dict = {
            filename: ".".join(filename.split(".")[:-1])
            + custom_affix
            + filename.split(".")[-1]
            for filename in files
        }
        return filename_dict
    if int(userinput) == 1:
        userinput2 = takeinput(INC_MENU)
        while not userinput2.isnumeric() or int(userinput2) not in [1, 2]:
            userinput2 = takeinput("")
        if int(userinput2) == 1:
            counter_params = input(
                "Enter the number of leading zeros followed by a space and then the starting index, followed by a space, and then the step\n"
            )
            counter_params = counter_params.split()
            while (
                len(counter_params) != 3
                or not counter_params[0].isnumeric()
                or not counter_params[1].isnumeric()
                or not counter_params[2].isnumeric()
            ):
                counter_params = input(
                    "Enter the number of leading zeros followed by a space and then the starting index, followed by a space, and then the step\n"
                )
                counter_params = counter_params.split()
            newfilenames = []
            for _ in range(len(files)):
                num = int(counter_params[1]) + (_ * int(counter_params[2]))
                num_zeros = int(counter_params[0]) - (
                    len(str(num)) - len(counter_params[1])
                )
                if num_zeros < 0:
                    num_zeros = 0
                append_str = num_zeros * "0" + str(num)
                if affix_type == "suffix":
                    newfilename = (
                        ".".join(files[_].split(".")[:-1])
                        + append_str
                        + files[_].split(".")[-1]
                    )
                elif affix_type == "prefix":
                    newfilename = append_str + files[_]
                newfilenames.append(newfilename)
            return zip(files, newfilenames)
        if int(userinput2) == 2:
            dating_params = input(
                "Please enter the start date in format YYYY-MM-DD and then a space and the step in number of days,\nand then a space and the output format using the format codes here: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior\n"
            )
            start_date = dating_params.split()[0]
            start_date = dt.strptime(start_date, "%Y-%m-%d")
            start_date = d(start_date.year, start_date.month, start_date.day)
            day_step = dating_params.split()[1]
            newfilenames = []
            for _ in range(len(files)):
                writedate = start_date + td(days=_ * int(day_step))
                writedate = writedate.strftime(" ".join(dating_params.split()[2:]))
                if affix_type == "suffix":
                    newfilename = (
                        ".".join(files[_].split(".")[:-1])
                        + writedate
                        + files[_].split(".")[-1]
                    )
                elif affix_type == "prefix":
                    newfilename = writedate + files[_]
                newfilenames.append(newfilename)
            return zip(files, newfilenames)


def prefix_subroutine(files):
    return affix_subroutine(files, "prefix")


def suffix_subroutine(files):
    return affix_subroutine(files, "suffix")


def replacement_subroutine(files):
    to_replace = input(
        "Type the string you would like replaced (start your string with :re: to enable regex)\n"
    )
    replacement = input("Type the string you would like to replace with\n")
    extensions = [file.split(".")[-1] for file in files]
    names = [file.split(".")[:-1] for file in files]

    if to_replace.startswith(":re:"):
        re_to_replace = to_replace[4:]
        newnames = [re.sub(re_to_replace, replacement, name) for name in names]
    else:
        newnames = [name.replace(to_replace, replacement) for name in names]

    newnames_full = [
        ".".join([name, extension]) for name, extension in zip(newnames, extensions)
    ]

    return zip(files, newnames_full)


def dating_subroutine(files):
    userinput = takeinput(MOD_CREATION_MENU)
    while not userinput.isnumeric() or int(userinput) not in [1, 2]:
        userinput = takeinput("")
    if int(userinput) == 1:
        times = [dt.fromtimestamp(os.stat(file).st_mtime) for file in files]
    else:
        times = [dt.fromtimestamp(os.stat(file).st_birthtime) for file in files]
    dates = [d(time.year, time.month, time.day) for time in times]
    userinput = takeinput(DATE_SUFF_PRE_MENU)
    while not userinput.isnumeric() or int(userinput) not in [1, 2]:
        userinput = takeinput("")
    if int(userinput) == 1:
        newfilenames = [
            ".".join(file.split(".")[:-1])
            + date.strftime("%Y_%m_%d")
            + file.split(".")[-1]
            for file, date in zip(files, dates)
        ]
    else:
        newfilenames = [
            date.strftime("%Y_%m_%d") + file for file, date in zip(files, dates)
        ]
    return zip(files, newfilenames)


def rename(filezip):
    fileziplist = list(filezip)
    userinput = takeinput(FINAL_RENAME_MENU)
    while not userinput.isnumeric() or int(userinput) not in [1, 2]:
        userinput = takeinput("")
    if int(userinput) == 1:
        newdirname = f"files_renamed_{d.today().strftime('%Y_%m_%d')}"
        if os.path.isdir(newdirname):
            overwrite = takeinput(f"{newdirname} already exists, overwrite? (y/n)")
            while overwrite not in ["y", "n"]:
                overwrite = takeinput("")
            if overwrite == "y":
                shutil.rmtree(newdirname)
            else:
                newdirname = input(
                    "Please enter alternative subfolder name, leave blank to exit"
                )
        if newdirname == "":
            return None
        herepath = os.getcwd()
        print(f"Creating Directory {newdirname}")
        os.mkdir(newdirname)
        to_copy = [t[0] for t in fileziplist]
        print(f"Copying files to {newdirname}")
        for file in to_copy:
            src = herepath + f"/{file}"
            dst = herepath + f"/{newdirname}/{file}"
            shutil.copy2(src, dst)
        os.chdir(newdirname)
    print("Renaming files...")
    for old_name, new_name in fileziplist:
        os.rename(old_name, new_name)


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
        filezip = None
        if int(firstchoice) == 1:
            filezip = suffix_subroutine(files)
        if int(firstchoice) == 2:
            filezip = prefix_subroutine(files)
        if int(firstchoice) == 3:
            filezip = replacement_subroutine(files)
        if int(firstchoice) == 4:
            filezip = dating_subroutine(files)
        if not filezip:
            continue
        rename(filezip)


if __name__ == "__main__":
    main()
