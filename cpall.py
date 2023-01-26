import os, sys
from colorama import Fore

maxfileload = 1000000
blksize = 1024 * 500


def copyfile(pathFrom, pathTo, maxfileload=maxfileload):
    if os.path.getsize(pathFrom) <= maxfileload:
        bytesFrom = open(pathFrom, 'rb').read()  # read small file all at once
        open(pathTo, 'wb').write(bytesFrom)
    else:
        fileFrom = open(pathFrom, 'rb')  # read big files in chunk
        fileTo = open(pathTo, 'wb')  # need b mode for both
        while True:
            bytesFrom = fileFrom.read(blksize)  # get one block at the end
            if not bytesFrom:
                break
            fileTo.write(bytesFrom)  # empty after last chunk


def copytree(dirFrom, dirTo, verbose=0):
    fcount = dcount = 0
    for filename in os.listdir(dirFrom):
        pathFrom = os.path.join(dirFrom, filename)
        pathTo = os.path.join(dirTo, filename)
        if not os.path.isdir(pathFrom):  # copy simple files
            try:
                if verbose > 1: print(Fore.LIGHTGREEN_EX, 'copying', pathFrom, 'to', pathTo)
                copyfile(pathFrom, pathTo)
                fcount += 1
            except:
                print(Fore.LIGHTRED_EX, 'Error copying', pathFrom, 'to', pathTo, '--skipped')
                print(Fore.LIGHTMAGENTA_EX, sys.exc_info()[0], sys.exc_info()[1])
        else:
            if verbose: print(Fore.LIGHTMAGENTA_EX, 'copying dir', pathFrom, 'to', pathTo)
            try:
                os.mkdir(pathTo)  # make new subdir
                below = copytree(pathFrom, pathTo)  # recur into subdirs
                fcount += below[0]  # add subdir counts
                dcount += below[1]
                dcount += 1
            except:
                print(Fore.LIGHTRED_EX, 'Error creating', 'to', pathTo, '--skipped')
                print(Fore.LIGHTMAGENTA_EX, sys.exc_info()[0], sys.exc_info()[1])
    return (fcount, dcount)


def getargs():
    try:
        dirFrom, dirTo = sys.argv[1:]
    except:
        print(Fore.LIGHTCYAN_EX, 'Usage error : cpall.py dirFrom dirTo')
    else:
        if not os.path.isdir(dirFrom):
            print(Fore.LIGHTMAGENTA_EX, 'Error: dirFrom is not a directory')
        elif not os.path.exists(dirTo):
            os.mkdir(dirTo)
            print(Fore.BLUE, 'Warning: dirTo already exists')
            if hasattr(os.path, 'samefile'):
                same = os.path.samefile(dirFrom, dirTo)
            else:
                same = os.path.abspath(dirFrom) == os.path.abspath(dirTo)
            if same:
                print(Fore.LIGHTMAGENTA_EX, 'Error dirFrom same as dirTo')
            else:
                return (dirFrom, dirTo)


if __name__ == '__main__':
    import time

    dirstuple = getargs()
    if dirstuple:
        print(Fore.LIGHTRED_EX, 'Copying ....')
        start = time.clock()
        fcount = dcount = copytree(*dirstuple)
        print(Fore.LIGHTRED_EX, 'Copied', fcount, 'files', dcount, 'directories', end=' ')
        print(Fore.LIGHTGREEN_EX, 'in', time.clock(), -start, 'seconds')
