"""
    Searches deep inside a directory structure, looking for duplicate file.
    Duplicates aka copies have the same content, but not necessarily the same name.
"""
__author__ = "Simon Lee"
__email__ = "lees118@my.erau.edu"
__version__ = "1.0"

# noinspection PyUnresolvedReferences
from os.path import getsize, join
from time import time

# noinspection PyUnresolvedReferences
from p1utils import all_files, compare

lst_of_images = (all_files('images'))

def search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Basic search strategy goes like this:
    - until the provided list is empty.
    - remove the 1st item from the provided file_list
    - search for its duplicates in the remaining list and put the item and all its duplicates into a new list
    - if that new list has more than one item (i.e. we did find duplicates) save the list in the list of lists
    As a result we have a list, each item of that list is a list,
    each of those lists contains files that have the same content
    """
    lol = []
    while 0 < len(file_list):
        dups = [file_list.pop(0)]
        for i in range(len(file_list) - 1, -1, -1):
            if compare(dups[0], file_list[i]):
                dups.append(file_list.pop(i))
        if 1 < len(dups):
            lol.append(dups)
    return lol

def faster_search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Here's an idea: executing the compare() function seems to take a lot of time.
    Therefore, let's optimize and try to call it a little less often.
    """
    lol = []
    file_sizes = list(map(getsize, file_list))
    dups = list(filter(lambda x: 1 < file_sizes.count(getsize(x)), file_list))
    for i in dups:
        extras = [x for x in dups if compare(i, x)]
        if 1 < len(extras):
            lol.append(extras)
    return lol

def report(lol):
    """ Prints a report
    :param lol: list of lists (each containing files with equal content)
    :return: None
    Prints a report:
    - longest list, i.e. the files with the most duplicates
    - list where the items require the largest amount or disk-space
    """
    print("== == Duplicate File Finder Report == ==")

if len(lol) > 0:
    m = list(max(lol, key=lambda x: len(x)))
    print(f"The file with the most duplicates is {m[0]} \n")
    m.pop(0)
    print(f"Here are it's {len(m)} copies:", * m, sep="\n")

    file_sizes = list(max(lol, key=lambda x: sum([getsize(n) for n in x])))
    print(f"\n The most disk space {sum([getsize(n) for n in file_sizes])} could be recovered by"
          f"deleting copies of this file:{file_sizes[0]}")
    file_sizes.pop(0)
    print(f"\n Here are its {len(file_sizes)} copies:")

else:
    print("No duplicates found")

if __name__ == '__main__':
    path = join(".", "images")

    # measure how long the search and reporting takes:
    t0 = time()
    report(search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")

    print("\n\n .. and now w/ a faster search implementation:")

    # measure how long the search and reporting takes:
    t0 = time()
    report(faster_search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")
