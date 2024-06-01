from colorama import Fore, Style, init
init()

# light colors
class light:
    green = Fore.LIGHTGREEN_EX
    red = Fore.LIGHTRED_EX
    yellow = Fore.LIGHTYELLOW_EX
    cyan = Fore.LIGHTCYAN_EX
    magenta = Fore.LIGHTMAGENTA_EX
    blue = Fore.LIGHTBLUE_EX
    black = Fore.LIGHTBLACK_EX
# dark colors
class dark:
    green = Fore.GREEN
    red = Fore.RED
    yellow = Fore.YELLOW
    cyan = Fore.CYAN
    magenta = Fore.MAGENTA
    blue = Fore.BLUE
    black = Fore.BLACK

class close :
    reset = Style.RESET_ALL