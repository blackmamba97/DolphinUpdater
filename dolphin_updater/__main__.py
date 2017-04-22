import abc
import argparse
import bs4
import colorama
import os
import re
import shutil
import subprocess
import sys
import urllib.request

END = colorama.Style.RESET_ALL
CYAN = colorama.Fore.CYAN
GREEN = colorama.Fore.GREEN


class Builds(abc.ABC):
    def __init__(self, path):
        self.path = path
        self.table = self.fetch_version_table()
        self.latest_version = self.get_latest_version()
        self.latest_download = self.get_latest_download()
        self.installed_version = None

    @abc.abstractmethod
    def fetch_version_table(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_latest_version(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def print_latest_version(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_latest_download(self):
        raise NotImplementedError()

    def get_installed_version(self, pattern):
        with open(self.path, "rb") as f:
            match = re.search(pattern, f.read())
            return match.group().decode("utf-8")

    def is_outdated(self):
        return self.latest_version != self.installed_version


class DolphinBuilds(Builds):
    def __init__(self, path):
        super().__init__(path)
        self.installed_version = self.get_installed_version(br"[1-9]\.[0-9]-[0-9]+")

    def fetch_version_table(self):
        url = "https://dolphin-emu.org/download/list/master/1/?nocr=true"
        return fetch_html_from_website(url).find("table", attrs={"class": "versions-list"})

    def get_latest_version(self):
        pattern = re.compile(r"[1-9]\.[0-9]-[0-9]*(?=-x64\.7z)")
        for tr in self.table.findAll("tr", attrs={"class": "download"}):
            td = tr.find("td", attrs={"class": "download-links"})
            a = td.find("a", attrs={"class": "win"})
            if a:
                return pattern.search(a.get("href")).group()

    def print_latest_version(self):
        print("Current master builds:")
        for row in self.table.findAll("tr", attrs={"class": "infos"}):
            version = row.find("td", attrs={"class": "version"}).find("a").get_text()
            change = row.find("td", attrs={"class": "description"}).get_text()
            time = row.find("td", attrs={"class": "reldate"}).get_text()
            build = f"{version:<10} | {time:<20} | {change.split(' (')[0]}"
            if version == self.installed_version:
                print(CYAN, "\t", build, END)
            elif version == self.latest_version:
                print(GREEN, "\t", build, END)
            else:
                print("\t", build)

    def get_latest_download(self):
        for tr in self.table.findAll("tr", attrs={"class": "download"}):
            td = tr.find("td", attrs={"class": "download-links"})
            a = td.find("a", attrs={"class": "win"})
            if a:
                return a.get("href")


class IshiirukaBuilds(Builds):
    def __init__(self, path):
        super().__init__(path)
        self.installed_version = self.get_installed_version(br"[0-9]+(?=[ ]?\([^)]+\)[\x00]+master)")

    def fetch_version_table(self):
        url = "https://www.dropbox.com/sh/7f78x2czhknfrmr/AADhXhA0b8EIcCyejITS697Ca?dl=0"
        table = fetch_html_from_website(url).find("ol", attrs={"class": "sl-grid-body"})
        return table.decode_contents()

    def get_latest_version(self):
        versions = re.findall(r"[0-9]{3,}(?=%28[\S]+%29\.x64\.7z\?dl=0)", self.table)
        return max(versions)

    def print_latest_version(self):
        print("Latest build:\t\t\t", GREEN, self.latest_version, END)

    def get_latest_download(self):
        regex = rf"https://www\.dropbox\.com/sh/[\S]+\.{self.latest_version}%28[\S]+%29\.x64\.7z\?dl=0"
        match = re.search(regex, self.table)
        return match.group()[:-1] + "1"


def fetch_html_from_website(url):
    html = urllib.request.urlopen(url).read()
    return bs4.BeautifulSoup(html, "html.parser")


def is_ishiiruka_build(path):
    with open(path, "rb") as f:
        return bool(re.search(b"Ishiiruka", f.read()))


def get_resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def update_dolphin_if_necessary(dolphin_exe_path):
    print("You are updating:\t\t", CYAN, dolphin_exe_path, END)
    if is_ishiiruka_build(dolphin_exe_path):
        builds = IshiirukaBuilds(dolphin_exe_path)
    else:
        builds = DolphinBuilds(dolphin_exe_path)
    if builds.is_outdated():
        print("Current version installed:\t", CYAN, builds.installed_version, END)
        builds.print_latest_version()
        if not input("Press Enter to update\n"):
            download_and_update(builds)


def download_and_update(builds):
    directory = os.path.dirname(builds.path)
    dolphin_7z_path = os.path.join(directory, "Dolphin.7z")
    extracted_folder = os.path.join(directory, "Extracted")
    print()
    download(builds.latest_download, dolphin_7z_path)
    print("\nExtracting...")
    extract_dolphin_7z(dolphin_7z_path, extracted_folder)
    print("Updating...")
    update_dolphin(directory, extracted_folder)
    os.remove(dolphin_7z_path)


def download(url, file_path):
    urllib.request.urlretrieve(url, filename=file_path, reporthook=download_report_hook)


def download_report_hook(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    print("\rDownloading... ", percent, "%", end="", flush=True)


def extract_dolphin_7z(file_name, extracted_folder):
    if os.path.exists(extracted_folder):
        shutil.rmtree(extracted_folder)
    call = f'{get_resource_path("7zr.exe")} x "{file_name}" -o"{extracted_folder}" -aoa'
    subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()


def update_dolphin(directory, extracted_folder):
    packed_folder_name = "Dolphin-x64"
    files_to_move = os.listdir(extracted_folder)
    if files_to_move == [packed_folder_name]:
        extracted_folder = os.path.join(extracted_folder, packed_folder_name)
        files_to_move = os.listdir(extracted_folder)
    for file in files_to_move:
        old_file = os.path.join(directory, file)
        new_file = os.path.join(extracted_folder, file)
        if os.path.exists(old_file):
            shutil.rmtree(old_file) if os.path.isdir(old_file) else os.remove(old_file)
        shutil.move(new_file, old_file)
    if extracted_folder.endswith(packed_folder_name):
        extracted_folder = os.path.join(extracted_folder, "..")
    shutil.rmtree(extracted_folder)


def main():
    colorama.init()
    parser = argparse.ArgumentParser(description="Update the Dolphin Emulator or a Ishiiruka build to the latest "
                                                 "master build. Leave out the --path argument if a Dolphin build is "
                                                 "in the script directory.")
    parser.add_argument("-p", "--path", default=os.path.abspath("Dolphin.exe"), help="absolute path to the Dolphin.exe")
    dolphin_exe_path = parser.parse_args().path
    if not dolphin_exe_path.endswith("Dolphin.exe"):
        print("Path must end with 'Dolphin.exe'")
        sys.exit(1)
    if not os.path.exists(dolphin_exe_path):
        print("No Dolphin.exe found at '", dolphin_exe_path, "'", sep="")
        sys.exit(1)
    update_dolphin_if_necessary(dolphin_exe_path)
    subprocess.Popen(dolphin_exe_path)


if __name__ == "__main__":
    main()
