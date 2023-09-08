#!/usr/bin/env python3

import os
import gdown
from updater import download, ota


def main():
    here = os.path.dirname(os.path.realpath(__file__))
    url = ota.get_stock_rom_id_by_full_variant("Titan_EEA")
    gdown.download(url, here + "/../resources/Titan_EEA_Stock_Rom.zip", quiet=False)
    return


if __name__ == '__main__':
    main()
