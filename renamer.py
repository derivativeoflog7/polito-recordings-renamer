import os, re

# Regex to find <beginnig of filename>dd.mm.yyy<rest of filename> (or with dashes instead of dots)
PATTERN = re.compile(r".*(?P<day>\d{2})[\.-](?P<month>\d{2})[\.-](?P<year>\d{4})(?P<end>.*)", re.IGNORECASE)
RED_ANSI = "\33[31m"
YELLOW_ANSI = "\33[33m"
RESET_ANSI = "\33[39m"

def rename_files(directory: str, dry_run: bool) -> int:
    """
    Returns the number of failed items
    """
    failed = 0
    # Add trailing slash to the directory if not already present
    if directory[-1] not in ("/", "\\"):
        directory = directory + "/"
    # Iterate files in directory
    for filename in os.listdir(directory):
        # Skip directories
        if os.path.isfile(directory + filename):
            match = re.search(PATTERN, filename)
            # Show warning if filename didn't match pattern
            if not match:
                print(f"{RED_ANSI}WARNING! File {filename} did not match the pattern!\nIt will not be renamed.{RESET_ANSI}\n")
                failed += 1
            else:
                # Print original and target filename
                newname = f"{match.group("year")}.{match.group("month")}.{match.group("day")}{match.group("end")}"
                print(filename)
                print("↓↓↓↓↓")
                print(newname + "\n")
                # Do renaming if run isn't dry
                if not dry_run:
                    os.rename(directory + filename, directory + newname)
    return failed

def main() -> None:
    # Ask for directory until a valid one is entered
    while not os.path.isdir(directory := input("Directory containing files?>")):
        print("Invalid directory")
    # Do a dry run
    failed = rename_files(directory, True)
    # Print warning if there are non-matching files
    if failed:
        print(f"{YELLOW_ANSI}Warning: some files did not match the pattern{RESET_ANSI}")
    # Ask for input until y/n is entered (case insensitive)
    while (opt := input("Proceed? [y/n]>").lower()) not in ("y", "n"):
        pass
    # Rename files
    if opt == "y":
        rename_files(directory, False)


if __name__ == "__main__":
    main()
