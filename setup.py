#!/usr/bin/env python3

import os
import subprocess


def main():
    os.system("pip3 install PyQt5")
    os.system("pip3 install gdown")
    os.system("cd resources; git clone git@github.com:rumplestilzken/mksuper.git")
    os.system("cd ./resources/mksuper/; python install-dependencies.py")


if __name__ == '__main__':
    main()