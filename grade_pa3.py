#!/usr/bin/env python3
'''
Grading script for PA3 (Huffman)
Niema Moshiri 2017
'''
import argparse,signal
from subprocess import check_output,CalledProcessError,DEVNULL
from os.path import getsize,isfile
from random import choice,randint

# global constants
TIME = 180 # max number of seconds for runtime
DNA = 'ACGT' # DNA alphabet
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' # English alphabet
ALPHANUM = ALPHABET + '0123456789' # English alphanumeric
ALPHAEXT = ALPHANUM + '~`!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?' # English alphanumeric with symbols
BYTES = [i for i in range(256)] # all possible bytes
SMALL_K = 1000 # number of bytes in small random dataset (1 KB)
MID_K = 100000 # number of bytes in medium random dataset (100 KB)
LARGE_K = 10000000 # number of bytes in large random dataset (10 MB)
COMP_RANGE = 1.25 # largest percentage of the reference solution filesize to be within (i.e., compress passes if <= COMP_RANGE * refcompress)
RECON_P = "+1 for compressing and decompressing successfully"
RECON_F = "+0 for not compressing and decompressing successfully"
SIZE_P = "+1 for being within %f of refcompress" % (COMP_RANGE-1)
SIZE_F = "+0 for not being within %f of refcompress" % (COMP_RANGE-1)
REFSIZE_P = "+1 for beating refcompress"
REFSIZE_F = "+0 for not beating refcompress"
MEMLEAK_P = "+1 for no memory leaks"
MEMLEAK_F = "+0 for memory leaks"

# definitions for killing function after certain amount of time
class TimeoutException(Exception):
    pass
def timeout_handler(signum, frame):
    raise TimeoutException
signal.signal(signal.SIGALRM, timeout_handler)

# grade PA3
def grade(refcompress): # parameter is full path to refcompress executable
    score = 0 # total possible = 23 (20 for correctness, 3 for performance vs. refcompress) (+2 for style)
    pos = 0

    # check if code can compile
    print("Checking if code compiles:")
    pos += 1
    try:
        check_output("make clean".split())
        check_output("rm -f compress uncompress".split())
        check_output("make".split())
        if not isfile("compress") or not isfile("uncompress"):
            print("Failed to compile using 'make' command. 0 points")
            exit()
        print("+1 for code compiling"); score += 1
    except CalledProcessError:
        print("Failed to compile using 'make' command. 0 points")
        exit()
    check_output("rm -f niema_test niema_ref niema_comp niema_uncomp".split())
    print()

    # test small file of DNA alphabet
    print("Running small DNA file:")
    pos += 2
    word = ''.join([choice(DNA) for _ in range(SMALL_K)])
    f = open('niema_test','w')
    f.write(word)
    f.close()
    check_output([refcompress,'niema_test','niema_ref'], stderr=DEVNULL)
    try:
        signal.alarm(TIME)
        check_output('./compress niema_test niema_comp'.split(), stderr=DEVNULL)
        check_output('./uncompress niema_comp niema_uncomp'.split(), stderr=DEVNULL)
        signal.alarm(0)
        o = check_output('diff niema_test niema_uncomp'.split()).decode().strip()
        if len(o) == 0:
            print(RECON_P); score += 1
        else:
            print(RECON_F)
        if getsize('niema_comp') < COMP_RANGE*getsize('niema_ref'):
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
    except CalledProcessError:
        print("Your program crashed when running the small DNA file. 0 points")
    except TimeoutException:
        print("Your program took longer than %d seconds when running the small DNA file. 0 points" % TIME)
    check_output("rm -f niema_test niema_ref niema_comp niema_uncomp".split())
    print()

    # test medium file of DNA alphabet
    print("Running medium DNA file")
    pos += 2
    word = ''.join([choice(DNA) for _ in range(MID_K)])
    f = open('niema_test','w')
    f.write(word)
    f.close()
    check_output([refcompress,'niema_test','niema_ref'], stderr=DEVNULL)
    try:
        signal.alarm(TIME)
        check_output('./compress niema_test niema_comp'.split(), stderr=DEVNULL)
        check_output('./uncompress niema_comp niema_uncomp'.split(), stderr=DEVNULL)
        signal.alarm(0)
        o = check_output('diff niema_test niema_uncomp'.split()).decode().strip()
        if len(o) == 0:
            print(RECON_P); score += 1
        else:
            print(RECON_F)
        if getsize('niema_comp') < COMP_RANGE*getsize('niema_ref'):
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
    except CalledProcessError:
        print("Your program crashed when running the medium DNA file. 0 points")
    except TimeoutException:
        print("Your program took longer than %d seconds when running the medium DNA file. 0 points" % TIME)
    check_output("rm -f niema_test niema_ref niema_comp niema_uncomp".split())
    print()
    '''
    # test large file of DNA alphabet
    print("Running large DNA file")
    pos += 3
    word = ''.join([choice(DNA) for _ in range(LARGE_K)])
    f = open('niema_test','w')
    f.write(word)
    f.close()
    check_output([refcompress,'niema_test','niema_ref'], stderr=DEVNULL)
    try:
        signal.alarm(TIME)
        check_output('./compress niema_test niema_comp'.split(), stderr=DEVNULL)
        check_output('./uncompress niema_comp niema_uncomp'.split(), stderr=DEVNULL)
        signal.alarm(0)
        o = check_output('diff niema_test niema_uncomp'.split()).decode().strip()
        if len(o) == 0:
            print(RECON_P); score += 1
        else:
            print(RECON_F)
        if getsize('niema_comp') < COMP_RANGE*getsize('niema_ref'):
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
        if getsize('niema_comp') < getsize('niema_ref'):
            print(REFSIZE_P); score += 1
        else:
            print(REFSIZE_F)
    except CalledProcessError:
        print("Your program crashed when running the large DNA file. 0 points")
    except TimeoutException:
        print("Your program took longer than %d seconds when running the large DNA file. 0 points" % TIME)
    check_output("rm -f niema_test niema_ref niema_comp niema_uncomp".split())
    print()

    # test small file of extended alphanumerical alphabet
    print("Running small extended alphanumerical file:")
    pos += 2
    word = ''.join([choice(ALPHAEXT) for _ in range(SMALL_K)])
    f = open('niema_test','w')
    f.write(word)
    f.close()
    check_output([refcompress,'niema_test','niema_ref'], stderr=DEVNULL)
    try:
        signal.alarm(TIME)
        check_output('./compress niema_test niema_comp'.split(), stderr=DEVNULL)
        check_output('./uncompress niema_comp niema_uncomp'.split(), stderr=DEVNULL)
        signal.alarm(0)
        o = check_output('diff niema_test niema_uncomp'.split()).decode().strip()
        if len(o) == 0:
            print(RECON_P); score += 1
        else:
            print(RECON_F)
        if getsize('niema_comp') < COMP_RANGE*getsize('niema_ref'):
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
    except CalledProcessError:
        print("Your program crashed when running the small extended alphanumerical file. 0 points")
    except TimeoutException:
        print("Your program took longer than %d seconds when running the small extended alphanumerical file. 0 points" % TIME)
    check_output("rm -f niema_test niema_ref niema_comp niema_uncomp".split())
    print()

    # test medium file of extended alphanumerical alphabet
    print("Running medium extended alphanumerical file:")
    pos += 2
    word = ''.join([choice(ALPHAEXT) for _ in range(MID_K)])
    f = open('niema_test','w')
    f.write(word)
    f.close()
    check_output([refcompress,'niema_test','niema_ref'], stderr=DEVNULL)
    try:
        signal.alarm(TIME)
        check_output('./compress niema_test niema_comp'.split(), stderr=DEVNULL)
        check_output('./uncompress niema_comp niema_uncomp'.split(), stderr=DEVNULL)
        signal.alarm(0)
        o = check_output('diff niema_test niema_uncomp'.split()).decode().strip()
        if len(o) == 0:
            print(RECON_P); score += 1
        else:
            print(RECON_F)
        if getsize('niema_comp') < COMP_RANGE*getsize('niema_ref'):
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
    except CalledProcessError:
        print("Your program crashed when running the medium extended alphanumerical file. 0 points")
    except TimeoutException:
        print("Your program took longer than %d seconds when running the medium extended alphanumerical file. 0 points" % TIME)
    check_output("rm -f niema_test niema_ref niema_comp niema_uncomp".split())
    print()

    # test large file of extended alphanumerical alphabet
    print("Running large extended alphanumerical file:")
    pos += 3
    word = ''.join([choice(ALPHAEXT) for _ in range(LARGE_K)])
    f = open('niema_test','w')
    f.write(word)
    f.close()
    check_output([refcompress,'niema_test','niema_ref'], stderr=DEVNULL)
    try:
        signal.alarm(TIME)
        check_output('./compress niema_test niema_comp'.split(), stderr=DEVNULL)
        check_output('./uncompress niema_comp niema_uncomp'.split(), stderr=DEVNULL)
        signal.alarm(0)
        o = check_output('diff niema_test niema_uncomp'.split()).decode().strip()
        if len(o) == 0:
            print(RECON_P); score += 1
        else:
            print(RECON_F)
        if getsize('niema_comp') < COMP_RANGE*getsize('niema_ref'):
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
        if getsize('niema_comp') < getsize('niema_ref'):
            print(REFSIZE_P); score += 1
        else:
            print(REFSIZE_F)
    except CalledProcessError:
        print("Your program crashed when running the large extended alphanumerical file. 0 points")
    except TimeoutException:
        print("Your program took longer than %d seconds when running the large extended alphanumerical file. 0 points" % TIME)
    check_output("rm -f niema_test niema_ref niema_comp niema_uncomp".split())
    print()
   '''
    # test small file of binary alphabet
    print("Running small binary file:")
    pos += 2
    word = bytes([choice(BYTES) for _ in range(SMALL_K)])
    f = open('niema_test','wb')
    f.write(word)
    f.close()
    check_output([refcompress,'niema_test','niema_ref'], stderr=DEVNULL)
    try:
        signal.alarm(TIME)
        check_output('./compress niema_test niema_comp'.split(), stderr=DEVNULL)
        check_output('./uncompress niema_comp niema_uncomp'.split(), stderr=DEVNULL)
        signal.alarm(0)
        o = check_output('diff niema_test niema_uncomp'.split()).decode().strip()
        if len(o) == 0:
            print(RECON_P); score += 1
        else:
            print(RECON_F)
        if getsize('niema_comp') < COMP_RANGE*getsize('niema_ref'):
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
    except CalledProcessError:
        print("Your program crashed when running the small binary file. 0 points")
    except TimeoutException:
        print("Your program took longer than %d seconds when running the small binary file. 0 points" % TIME)
    check_output("rm -f niema_test niema_ref niema_comp niema_uncomp".split())
    print()

    # test medium file of binary alphabet
    print("Running medium binary file:")
    pos += 2
    word = bytes([choice(BYTES) for _ in range(MID_K)])
    f = open('niema_test','wb')
    f.write(word)
    f.close()
    check_output([refcompress,'niema_test','niema_ref'], stderr=DEVNULL)
    try:
        signal.alarm(TIME)
        check_output('./compress niema_test niema_comp'.split(), stderr=DEVNULL)
        check_output('./uncompress niema_comp niema_uncomp'.split(), stderr=DEVNULL)
        signal.alarm(0)
        o = check_output('diff niema_test niema_uncomp'.split()).decode().strip()
        if len(o) == 0:
            print(RECON_P); score += 1
        else:
            print(RECON_F)
        if getsize('niema_comp') < COMP_RANGE*getsize('niema_ref'):
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
    except CalledProcessError:
        print("Your program crashed when running the medium binary file. 0 points")
    except TimeoutException:
        print("Your program took longer than %d seconds when running the medium binary file. 0 points" % TIME)
    check_output("rm -f niema_test niema_ref niema_comp niema_uncomp".split())
    print()

    # test large file of binary alphabet
    print("Running large binary file:")
    pos += 3
    word = bytes([choice(BYTES) for _ in range(LARGE_K)])
    f = open('niema_test','wb')
    f.write(word)
    f.close()
    check_output([refcompress,'niema_test','niema_ref'], stderr=DEVNULL)
    try:
        signal.alarm(TIME)
        check_output('./compress niema_test niema_comp'.split(), stderr=DEVNULL)
        check_output('./uncompress niema_comp niema_uncomp'.split(), stderr=DEVNULL)
        signal.alarm(0)
        o = check_output('diff niema_test niema_uncomp'.split()).decode().strip()
        if len(o) == 0:
            print(RECON_P); score += 1
        else:
            print(RECON_F)
        if getsize('niema_comp') < COMP_RANGE*getsize('niema_ref'):
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
        if getsize('niema_comp') < getsize('niema_ref'):
            print(REFSIZE_P); score += 1
        else:
            print(REFSIZE_F)
    except CalledProcessError:
        print("Your program crashed when running the large binary file. 0 points")
    except TimeoutException:
        print("Your program took longer than %d seconds when running the large binary file. 0 points" % TIME)
    check_output("rm -f niema_comp niema_uncomp".split())
    print()

    # check for memory leaks
    print("Checking for memory leaks:")
    pos += 1
    leak = False
    try:
        signal.alarm(TIME)
        o = check_output("valgrind --log-fd=1 --leak-check=yes ./compress niema_test niema_comp".split()).decode()
        if "no leaks are possible" not in o and not ("definitely lost: 0 bytes" in o and "indirectly lost: 0 bytes" in o):
            leak = True
        if not leak:
            o = check_output("valgrind --log-fd=1 --leak-check=yes ./uncompress niema_comp niema_uncomp".split()).decode()
            if "no leaks are possible" not in o and not ("definitely lost: 0 bytes" in o and "indirectly lost: 0 bytes" in o):
                leak = True
        signal.alarm(0)
        if not leak:
            print(MEMLEAK_P); score += 1
        else:
            print(MEMLEAK_F)
    except CalledProcessError:
        print("Your program crashed when running the memory leak test. 0 points")
    except TimeoutException:
        print("Your program took longer than %d seconds when running the memory leak test. 0 points" % TIME)
    print()

    # clean up at the end
    print("Total Score: %d/%d" % (score,pos))
    check_output("rm -f niema_test niema_ref niema_comp niema_uncomp".split())
    check_output("make clean".split())

# main function: call grader
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-r', '--refcompress', required=False, type=str, default="/home/linux/ieng6/cs100v/public/grading_scripts/refcompress", help="Full path to refcompress")
    args = parser.parse_args()
    assert isfile(args.refcompress), "refcompress executable not found: %s" % args.refcompress
    grade(args.refcompress)
