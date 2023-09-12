import sys
import os
import urllib.request
import zipfile
import json
import stat
import tarfile
import gdown

from enum import Enum

from updater import ota


class OS(Enum):
    NotSet = ""
    Linux = "linux"
    Windows = "windows"


class DeviceReqion(Enum):
    NotSet = ""
    EEA = "EEA"
    TEE = "TEE"
    UFS = "UFS"


class DeviceType(Enum):
    NotSet = ""
    Titan = "gargoyle"
    Pocket = "pocket"
    Slim = "slim"
    Jelly2E = "jelly2e"


class Qualifier(Enum):
    NotSet = ""
    bvN = "bvN"
    bgN = "bgN"
    bvN_vndklite = "bvN-vndklite"
    bgN_vndklite = "bgN-vndklite"


class FlashType(Enum):
    NotSet = ""
    Update = "update"
    Flash = "flash"
    FlashFull = "flash full"


os_type = OS.NotSet
region = DeviceReqion.NotSet
progress_bar = None
filename = ""
outfile = ""
dev = DeviceType.NotSet
qualifier = Qualifier.NotSet


def process_flash(json_url, variant, given_region, given_qualifier, progressbar):
    global progress_bar
    global dev
    global region
    global qualifier

    region = DeviceReqion[given_region]
    qualifier = Qualifier[given_qualifier.replace("-", "_")]
    progress_bar = progressbar
    progressbar.setValue(10)

    prepare_resources()
    progressbar.setValue(20)

    download_update(json_url, variant, given_qualifier)
    progressbar.setValue(50)

    mksuper()

    if not is_mksuper():
        flash_gsi("system")
    else:
        flash_gsi("super")


def is_mksuper():
    global dev
    if dev == DeviceType.Titan:
        return False

    return True


def mksuper():
    global dev
    global region
    global outfile
    global qualifier

    if not is_mksuper():
        return

    here = os.path.dirname(os.path.realpath(__file__))
    print("mksuper process running")

    full_variant = dev.name + "_" + region.name
    if not os.path.exists(here + "/../resources/super." + full_variant + "-" + qualifier.value + ".img"):
        folder_name = ""
        for folder in os.listdir(here + "/../resources/" + full_variant):
            if os.path.isdir(here + "/../resources/" + full_variant + "/" + folder):
                folder_name = folder
                break
        os.system(
            "cd " + here + "/../resources/mksuper/; python extract.py -stock " + here + "/../resources/" + full_variant
            + "/" + folder_name)
        os.system("cd " + here + "/../resources/mksuper/; python mksuper.py -dev " + dev.value + " -gsi "
                  + outfile.replace(".xz", "") + " -out " + here + "/../resources/super." + full_variant + "-" +
                  qualifier.value + ".img -no-product")

    outfile = here + "/../resources/super." + full_variant + "-" + qualifier.value + ".img"


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

    full_path = here + "/../resources/" + filename

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
    global region

    here = os.path.dirname(os.path.realpath(__file__))
    json_contents = urllib.request.urlopen(json_url)
    data = json.load(json_contents)
    variants = data["variants"]

    variant_code = ota.get_variant_map(qualifier)[variant]
    for enm in DeviceType:
        count = len(variant_code.split("_"))
        if count == 4:
            if variant_code.split("_")[2] in enm.value:
                dev = enm
                break
        else:
            if variant_code.split("_")[1] in enm.value:
                dev = enm
                break

    variant_url = "";
    for i in variants:
        if variant_code == i["name"]:
            variant_url = i["url"];
            break

    global outfile
    outfile = here + "/../resources/" + os.path.basename(variant_url)
    if not os.path.exists(outfile):
        if os_type == OS.Windows:
            os.system(
                "cd " + here + "/..resources/ & curl-8.2.1_5-win64-mingw\curl-8.2.1_5-win64-mingw\\bin\curl " + variant_url + " --output " + outfile)
        else:
            os.system("cd " + here + "/../resources/; wget " + variant_url)

    global progress_bar
    progress_bar.setValue(30)

    if not os.path.exists(outfile.strip(".xz")) and ".xz" in outfile:
        print("Extracting gargoyle GSI '" + outfile + "'")
        if os_type == OS.Windows:
            os.system("resources\\xz-5.2.9-windows\\bin_x86-64\\xz -kd -T 0 " + outfile)
        else:
            os.system("xz -kd -T 0 " + outfile)

    if is_mksuper():
        full_variant = dev.name + "_" + region.name
        if not os.path.exists(here + "/../resources/" + full_variant + ".zip"):
            print("Download and Extracting " + full_variant + ".zip")
            url = ota.get_stock_rom_url_by_full_variant(full_variant)
            gdown.download(url, here + "/../resources/" + full_variant + ".zip")
            with zipfile.ZipFile(here + "/../resources/" + full_variant + ".zip", 'r') as zip_ref:
                zip_ref.extractall(here + "/../resources/" + full_variant)


def flash_gsi(partition_name):
    here = os.path.dirname(os.path.realpath(__file__))
    global filename
    global os_type
    global outfile

    full_path = here + "/../resources/" + filename.rstrip(".zip") + "/platform-tools/"
    command = "/adb reboot bootloader"

    # if "system" in partition_name:
    #     command = "/adb reboot fastboot"

    os.system(full_path + command)

    progress_bar.setValue(70)
    command = "/fastboot flash " + partition_name + " " + outfile
    os.system(full_path + command)

    command = "/fastboot reboot"
    os.system(full_path + command)

    progress_bar.setValue(90)
