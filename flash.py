import sys
import os
import urllib.request
import zipfile
import json
import stat
import tarfile

from enum import Enum

import ota


class OS(Enum):
    NotSet = ""
    Linux = "linux"
    Windows = "windows"


class DeviceType(Enum):
    NotSet = ""
    Titan = "titan"
    Pocket = "pocket"
    Slim = "slim"
    Jelly2E = "jelly2e"


os_type = OS.NotSet
progress_bar = None
filename = ""
outfile = ""
dev = DeviceType.NotSet


def process_flash(json_url, variant, qualifier, progressbar):
    global progress_bar
    global dev
    progress_bar = progressbar
    progressbar.setValue(10)

    prepare_resources()
    progressbar.setValue(20)

    download_update(json_url, variant, qualifier)
    progressbar.setValue(50)

    flash_gsi("super")


def prepare_resources():
    here = os.path.dirname(os.path.realpath(__file__))

    global filename
    global os_type
    filename = ""
    if 'linux' in sys.platform:
        os_type = OS.Linux
        filename = "platform-tools_r34.0.4-linux.zip"
    elif 'win' in sys.platform:
        os_type = OS.Windows
        filename = "platform-tools_r34.0.4-windows.zip"

    url = "https://github.com/rumplestilzken/gargoyle_updater/releases/download/resources/" + filename

    full_path = here + "/resources/" + filename

    # Download
    if not os.path.exists(full_path):
        urllib.request.urlretrieve(url, full_path)

    # Unzip
    if not os.path.exists(full_path.strip(".zip")):
        with zipfile.ZipFile(full_path, 'r') as zip_ref:
            zip_ref.extractall(full_path.strip(".zip"))

    if os_type == OS.Windows:
        url = "https://github.com/rumplestilzken/gargoyle_updater/releases/download/resources/xz-5.2.9-windows" \
              ".zip"
        fn = os.path.basename(url)

        # Download and Unzip
        urllib.request.urlretrieve(url, here + "/resources/" + fn)
        with zipfile.ZipFile(here + "/resources/" + fn, 'r') as zip_ref:
            zip_ref.extractall(here + "/resources/" + fn.rstrip(".zip"))

        url = "https://github.com/rumplestilzken/gargoyle_updater/releases/download/resources/curl-8.2.1_5-win64-mingw" \
              ".zip"
        fn = os.path.basename(url)

        # Download and Unzip
        urllib.request.urlretrieve(url, here + "/resources/" + fn)
        with zipfile.ZipFile(here + "/resources/" + fn, 'r') as zip_ref:
            zip_ref.extractall(here + "/resources/" + fn.rstrip(".zip"))

    else:
        exe = full_path.rstrip(".zip") + "/platform-tools/adb"
        st = os.stat(exe)
        os.chmod(exe, st.st_mode | stat.S_IEXEC)
        exe = full_path.rstrip(".zip") + "/platform-tools/fastboot"
        st = os.stat(exe)
        os.chmod(exe, st.st_mode | stat.S_IEXEC)


def download_update(json_url, variant, qualifier):
    global dev
    global os_type

    here = os.path.dirname(os.path.realpath(__file__))
    json_contents = urllib.request.urlopen(json_url)
    data = json.load(json_contents)
    variants = data["variants"]

    variant_code = ota.get_variant_map(qualifier)[variant]
    for enm in DeviceType:
        if variant_code.split("_")[2] in enm.value:
            dev = enm

    variant_url = "";
    for i in variants:
        if variant_code == i["name"]:
            variant_url = i["url"];

    global outfile
    outfile = here + "/resources/" + os.path.basename(variant_url)
    if not os.path.exists(outfile):
        if os_type == OS.Windows:
            os.system(
                "cd resources/ & curl-8.2.1_5-win64-mingw\curl-8.2.1_5-win64-mingw\\bin\curl " + variant_url + " --output " + outfile)
        else:
            os.system("cd " + here + "/resources/; wget " + variant_url)

    global progress_bar
    progress_bar.setValue(30)

    if not os.path.exists(outfile.strip(".xz")) and ".xz" in outfile:
        print("Extracting gargoyle GSI '" + outfile + "'")
        if os_type == OS.Windows:
            os.system("resources\\xz-5.2.9-windows\\bin_x86-64\\xz -kd -T 0 " + outfile)
        else:
            os.system("xz -kd -T 0 " + outfile)

    if not os.path.exists(outfile.rstrip(".tar.gz")) and ".tar.gz" in outfile:
        print("Extracting gargoyle GSI '" + outfile + "'")
        with tarfile.open(outfile, "r") as tf:
            tf.extractall(path=here + "/resources/")


def flash_gsi(partition_name):
    here = os.path.dirname(os.path.realpath(__file__))
    global filename
    global os_type
    global outfile

    full_path = here + "/resources/" + filename.rstrip(".zip") + "/platform-tools/"
    command = "/adb reboot bootloader"

    if "system" in partition_name:
        command = "/adb reboot fastboot"

    os.system(full_path + command)

    progress_bar.setValue(70)
    command = "/fastboot flash " + partition_name + " " + outfile.replace(".tar.gz", "").replace(".xz", "")
    os.system(full_path + command)

    command = "/fastboot reboot"
    os.system(full_path + command)

    progress_bar.setValue(90)
