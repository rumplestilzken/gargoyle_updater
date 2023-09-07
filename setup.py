#!/usr/bin/env python3

import os
import subprocess


def main():
    os.system("pip3 install PyQt5")
    os.system("cd resources; git clone git@github.com:rumplestilzken/mksuper.git")


if __name__ == '__main__':
    main()