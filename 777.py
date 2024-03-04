from abc import abstractmethod, ABC
from colorama import *


class UserInterface(ABC):
    @abstractmethod
    def help(self):
        pass

    @abstractmethod
    def show_all_contacts(self):
        pass

    @abstractmethod
    def show_all_notes(self):
        pass


class Interface(UserInterface):
    def __init__(self, value: str):
        self.value = value

    def help(self):
        return Fore.YELLOW + self.value

    def show_all_contacts(self):
        return Fore.CYAN + self.value

    def show_all_notes(self):
        return Fore.MAGENTA + self.value


msg = Interface("hello")

print(msg.help())
print(msg.show_all_notes())
print(msg.show_all_contacts())
