import time
import sys
import os
from plugins.laravel.getenv import *
from plugins.portscanning import *
from plugins.shell import *
from plugins.wordpress.fm_exploit import *
from lib.colors import light, close
from lib.banner import *

class Ethopia:
    def __init__(self):
        self.commands = {
            "help" : self.help,
            "use" : self.use,
            "exit" : self.exit,
            "show" : self.show,
            "ls" : self.ls,
            "dir" : self.ls,
            "clear" : self.clear,
            "cls" : self.clear
        }
        self.running = True
        self.current_plugin = None

    def start(self):
        message = 'starting the ethopia project...'
        for x in range(len(message)):
            sys.stdout.write('\r'+'[*] '+message[:x]+message[x:].capitalize())
            sys.stdout.flush()
            time.sleep(0.1)
        print('\n')
        print(f"{banner.logo}")
        while self.running:
            cmd = input(f"\t{light.cyan}Ethopia > {close.reset}").strip().split()
            if cmd:
                command = cmd[0]
                args = cmd[1:]
                if command in self.commands:
                    self.commands[command](args)
                else:
                    print(f"Unknown command: {command}")

    def help(self, *args):
        print(f"{banner.help}")

    def use(self, args):
        if len(args) != 1:
            print("Usage: use <plugin>")
            return
        
        plugin_name = args[0]
        if plugin_name == 'plugins/shellfinder':
            self.current_plugin = run = ShellFinder()
            run.start()
        elif plugin_name == 'plugins/portscanning':
            self.current_plugin = run = PortScanning()
            run.start()
        elif plugin_name == 'plugins/wordpress/fm_exploit':
            self.current_plugin = run = WpFm()
            run.shell()
        elif plugin_name == 'plugins/laravel/getenv':
            self.current_plugin = run = getEnv() 
            run.start()
        else:
            print(f"Plugin {plugin_name} not found")
            return

    def exit(self, *args):
        if self.current_plugin:
            self.current_plugin = None
            print("Exited from plugin")
        else:
            print("Exiting tool")
            self.running = False

    def show(self, args):
        if len(args) == 0:
            print("Usage: show <options|plugins>")
            return

        if args[0] == 'plugins':
            print("Available plugins:")
            print(" - plugins/shellfinder")
            print(" - plugins/portscanning")
            print(" - plugins/wordpress/fm_exploit")
            print(" - plugins/laravel/getenv")
        else:
            print("Invalid show command")
    def ls(self, *args):
        os.system("ls" if os.name != "nt" else "dir")

    def clear(self, *args):
        os.system("clear" if os.name != "nt" else "cls")

if __name__ == "__main__":
    run = Ethopia()
    run.start()
