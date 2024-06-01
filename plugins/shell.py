import os
import requests
import concurrent.futures
from re import findall
import time
from lib.colors import *

# SET DEFAULT THREADING
DEFAULT_THREADS = 10

class ShellFinder:
    def __init__(self):
        self.options = {
            "TARGET": {"value": None, "required": True, "description": "The target address or target list"},
            "FILE": {"value": "lib/files/dir.txt", "required": True, "description": "File containing list of directories"},
        }
        self.commands = {
            "exploit": self.run_exploit,
            "set": self.set_option,
            "show": self.show_options,
            "exit": self.exit_shell
        }
        self.running = True

    def shell(self):
        pl = f'{light.blue}={close.reset}'*50
        print(f"""
\t{pl}\n
\t\t\tSHELL FINDER\n
\tcommand 'options' view for options this tool\n
\t{pl}
          """)
        while self.running:
            cmd = input(f"\t{light.cyan}Ethopia > {close.reset}").strip().split()
            if cmd:
                command = cmd[0]
                args = cmd[1:]
                if command in self.commands:
                    self.commands[command](args)
                else:
                    print(f"Unknown command: {command}")

    def run_exploit(self, args):
        target_list = self.get_target_list(self.options["TARGET"]["value"])
        if target_list and self.options["FILE"]["value"]:
            dir_list = self.getContents(self.options["FILE"]["value"])
            for target in target_list:
                self.ScanDir(target, dir_list)
        else:
            print("TARGET or FILE option not set")

    def set_option(self, args):
        if len(args) >= 2:
            option = args[0].upper()
            value = " ".join(args[1:])
            if option in self.options:
                self.options[option]["value"] = value
                print(f"Set {option} to {value}")
            else:
                print(f"Invalid option: {option}")
        else:
            print("Usage: set OPTION VALUE")

    def show_options(self, args):
        print(f"\n\tPlugins option ({light.magenta}shell finder{close.reset})\n")
        print(f"\t{'Name':<10} {'Current Setting':<20} {'Required':<10} {'Description':<40}")
        print(f"\t{'-'*10} {'-'*20} {'-'*10} {'-'*40}")
        for option, details in self.options.items():
            value = details["value"] if details["value"] else ""
            required = "yes" if details["required"] else "no"
            description = details["description"]
            print(f"\t{option:<10} {value:<20} {required:<10} {description:<40}")
        print("")

    def exit_shell(self, args):
        self.running = False
        print("Exiting Shell Finder")

    def start(self):
        self.shell()

    # Utility functions
    def getContents(self, files):
        with open(files, 'r') as file:
            return file.read().splitlines()

    def get_rhost_list(self, rhost):
        if os.path.isfile(rhost):
            return self.getContents(rhost)
        else:
            return [rhost]

    def MakeResult(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def SaveResult(self, data, files):
        with open(files, 'a') as file:
            file.write(data + '\n')

    def ScanDir(self, url, dirList):
        with concurrent.futures.ThreadPoolExecutor(max_workers=DEFAULT_THREADS) as ex:
            futures = {ex.submit(self.scanDirEngine, url, DirName): DirName for DirName in dirList}
            concurrent.futures.wait(futures)

    def scanDirEngine(self, url, DirName):
        DirUrl = f"{url}/{DirName}"
        try:
            response = requests.get(DirUrl)
            self.HandleEngine(response, DirUrl)
        except requests.exceptions.SSLError:
            print(f"[{dark.red} ✗ {close.reset}] {DirUrl} [{dark.red} Trying To HTTPS {close.reset}]")
            DirUrl = DirUrl.replace("https://", "http://")
            response = requests.get(DirUrl)
            self.HandleEngine(response, DirUrl)

    def HandleEngine(self, response, url):
        if response.status_code == 403:
            print(f"[{light.green} ✓ {close.reset}] {url} [{light.green} FOUND {close.reset}]")
            self.CmsDetect(url)
            self.ScanShell(url, "found")
        elif response.status_code == 200:
            print(f"[{light.magenta} ? {close.reset}] {url} [{light.magenta} DIR LISTENING / RIDERECT / NOT FOUND {close.reset}]")
            self.ScanShell(url, "listening")
        else:
            print(f"[{dark.red} ✗ {close.reset}] {url} [{dark.red} NOT FOUND {close.reset}]")

    def ScanShell(self, url, ScanType):
        FileUrl = f"{url}"
        if ScanType == "found" or ScanType == "listening":
            GetFiles = self.getContents("lib/files/NameShell.txt")
            with concurrent.futures.ThreadPoolExecutor(max_workers=DEFAULT_THREADS) as ex:
                futures = {ex.submit(self.ScanShellEngine, f"{FileUrl}{FileShell}"): FileShell for FileShell in GetFiles}
                concurrent.futures.wait(futures)

    def ScanShellEngine(self, fileUrl):
        try:
            response = requests.get(fileUrl)
            if response.status_code == 200:
                print(f"[{light.green} ✓ {close.reset}] {fileUrl} [{light.green} FOUND {close.reset}]")
                self.SaveResult(f"{fileUrl}", f"result/shellfound.txt")
            else:
                print(f"[{dark.red} ✗ {close.reset}] {fileUrl} [{dark.red} NOT FOUND {close.reset}]")
        except requests.exceptions.SSLError:
            print(f"[{dark.yellow} ? {close.reset}] {fileUrl} [{dark.yellow} SSL ERROR {close.reset}]")

    def CmsDetect(self, url):
        CmsDIr = ["/wp-content/", "/administrator/", "/admin/", "/catalog/", "/pkp/", "/sites"]
        for CmsDIrs in CmsDIr:
            CmsUrl = f"{url}{CmsDIrs}"
            response = requests.get(CmsUrl)
            if response.status_code == 200:
                print(f"[ # ] {CmsUrl} [ FOUND {self.GetNameCms(CmsDIr)} ]")
                

    def GetNameCms(self, CmsDir):
        Mapping = {
            "/wp-content/": "Wordpress",
            "/administrator/": "Joomla",
            "/admin/": "OpenCart",
            "/catalog/": "Open Journal System",
            "/sites/": "Drupal"
        }
        return Mapping.get(CmsDir, "No CMS")
