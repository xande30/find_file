import os, sys
from colorama import Fore


def reportfdiffs(unique1, unique2, dir1, dir2):
    if not (unique1 or unique2):
        print(Fore.LIGHTGREEN_EX, 'Directory lists are identical')
    else:
        if unique1:
            print(Fore.LIGHTGREEN_EX, 'Files unique to', dir1)
            for file in unique1:
                print(Fore.LIGHTGREEN_EX, '...', file)

        if unique2:
            print(Fore.LIGHTGREEN_EX, 'Files unique to', dir2)
            for file in unique2:
                print(Fore.LIGHTGREEN_EX, '...', file)


def difference(seq1, seq2):
    """
    Return all items in seq1 only;
    a set(seq1) - set(seq2) would work too, but sets are randomly
    ordered, so any platform-dependent directory order would be lost
    """
    return [item for item in seq1 if item not in seq2]


def comparedirs(dir1, dir2, files1=None, files2=None):
    """
    Compare directory contents, but not actual files;
    may need bytes listdir arg for undecodable filenames on some platforms
    """
    print('Comparing', dir1, 'to', dir2)
    files1 = os.listdir(dir1) if files1 is None else files1
    files2 = os.listdir(dir2) if files2 is None else files2
    unique1 = difference(files1, files2)
    unique2 = difference(files2, files1)
    reportfdiffs(unique1, unique2, dir1, dir2)


    return not (unique1 or unique2)  # true if no diffs


def getargs():
    "Args for command-line mode"
    try:
        dir1, dir2 = sys.argv[1:]  # 2 command-line args
    except:
        print('Usage: dirdiff.py dir1 dir2')
        sys.exit(1)
    else:
        return (dir1, dir2)


if __name__ == '__main__':
    dir1, dir2 = getargs()
    comparedirs(dir1, dir2)
