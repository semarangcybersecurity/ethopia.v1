import socket
from lib.colors import *

class PortScanning:
    def __init__(self):
        self.options = {
            "TARGET" : {
                'value' : None,
                "required": True,
                "description" : "Target IP or Domain",
            },
            "START_PORT" : {
                "value" : None,
                "required": False,
                "description" : "Start port (default: 1)"
            },
            "END_PORT" : {
                "value" : None,
                "required": False,
                "description" : "End port (default: 1000)"
            }
        }
        self.commands = {
            "set" : self.set_option,
            "show" : self.show_options,
            "run" : self.run_exploit,
            "exit" : self.exit_shell
        }
        self.running = True

    def shell(self):
        pl = f'{light.blue}={close.reset}'*50
        print(f"""
\t{pl}\n
\t\t\tPORT SCANNER\n
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
                if option == "TARGET":
                    try:
                        ip = socket.gethostbyname(value)
                        self.options["TARGET"]["value"] = ip
                        print(f"Domain {value} resolved to IP: {ip}")
                    except socket.gaierror:
                        print(f"Error resolving domain {value} to IP")
            else:
                print(f"Invalid option: {option}")
        else:
            print("Usage: set OPTION VALUE")

    def show_options(self, args):
        print(f"\n\tPlugins Options ({light.magenta}portscanning{close.reset})\n")
        print(f"\t{'Name':<10} {'Current Setting':<20} {'Required':<10} {'Description':<40}")
        print(f"\t{'-'*10} {'-'*20} {'-'*10} {'-'*40}")
        for option, details in self.options.items():
            value = details["value"] if details["value"] else ""
            required = "yes" if details["required"] else "no"
            description = details["description"]
            print(f"\t{option:<10} {value:<20} {required:<10} {description:<40}")
        print("")

    def run_exploit(self, args):
        target = self.options["TARGET"]["value"]
        start_port = int(self.options["START_PORT"]["value"]) if self.options["START_PORT"]["value"] else 1
        end_port = int(self.options["END_PORT"]["value"]) if self.options["END_PORT"]["value"] else 1000
        if not target:
            print("TARGET option not set")
            return
        try:
            for port in range(start_port, end_port + 1):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    print(f"{target}:{port} is OPEN")
                sock.close()
        except socket.error as e:
            print(f"Error: {e}")

    def exit_shell(self, args):
        self.running = False
        print("Exiting Port Scanner")

    def start(self):
        self.shell()