from classes import Record, AddressBook
from colorama import *
from file_sorter import FileSorter
from notebook import NoteBook
from abc import abstractmethod, ABC

init(autoreset=True)

phone_book = AddressBook()
notebook = NoteBook()

instruction = ("Hello, I am a bot assistant for work with the phone book. \n"
               "Enter the command:\n"
               "'show all' - if you want to view the entire phone book.\n"
               "'exit', 'close' or 'good bye' - if you want to finish the work.\n"
               "'add_contact name birthday' - if you want to add a contact to the phone book,\n"
               "for example 'add Tom 07-12-1949'. Birthday is an optional field.\n"
               "'add_phone name phone' - if you want to add a phone number to the contact.\n"
               "Phone must consist of 10 digits. You can add different phone numbers to the contact.\n"
               "'remove_phone name phone' - if you want to remove a phone number from the contact.\n"
               "'edit_phone name old_number new_number' - if you want to edit a phone number.\n"
               "'find_phone name number' - if yoy want to find a phone number in the contact.\n"
               "'add_birthday name birthday' - if you want to add a birthday in the contact. \n"
               "'days name' - if you want to know how many days are left until the contact's birthday.\n"
               "'find_user name' - if you want to find a definite user in the phone book.\n"
               "'add_secondname name' - if you want to add a secondname to the contact.\n"
               "'edit_secondname name' - if you want to edit a secondname to the contact.\n"
               "'delete_user name' - if you want to delete a contact from the phone book.\n"
               "'find_info text' - to find users by several digits of a phone number or several letters of a name.\n"
               "'add_secondname name secondname' - if you want to add a secondname to the contact.\n"
               "'add_address name address' - if you want to add address to the contact.\n"
               "'remove_address name address' - if you want to remove address from the contact.\n"
               "'edit_address name address' - if you want to edit address.\n"
               "'add_email name email' - if you want to add an email to the contact.\n"
               "'remove_email name email' - if you want to remove an email from the contact.\n"
               "'edit_email name old_email new_email' - if you want to edit an email.\n"
               "'birthday_in number' - if you want to see users which have birthday in number days.\n"
               "'file_sort path' - if you want to sort some directory (enter path to the directory).\n"
               "'add_note' - if you want to create a new note.\n"
               "'edit_note' - if you want to edit some note.\n"
               "'delete_note_by_index' - if you want to delete a note by index.\n"
               "'delete_note_by_title' - if you want to delete a note by title.\n"
               "'search_note_by_tag' - if you want to search notes by tag.\n"
               "'sort_notes_by_tag' - if you want to sort notes by tag.\n"
               "'notes_show_all' - if you want to see all notes.\n"
               "'search_note_by text' - if you want to search a note by the text.\n")


class AbstractInterface(ABC):
    @abstractmethod
    def help(self):
        pass

    @abstractmethod
    def show_all_contacts(self):
        pass

    @abstractmethod
    def show_all_notes(self):
        pass

    @abstractmethod
    def final(self):
        pass


class Interface(AbstractInterface):
    value: str

    def __init__(self, value: str):
        self.value = value

    def help(self):
        return Fore.MAGENTA + self.value

    def show_all_contacts(self):
        return Fore.CYAN + self.value

    def show_all_notes(self):
        return Fore.RED + self.value

    def final(self):
        return Fore.YELLOW + self.value


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except IndexError as Error:
            return Error
        except KeyError as Error:
            return Error
        except ValueError as Error:
            return Error
        except AttributeError as Error:
            return Error
        except TypeError:
            return "Wrong command"

    return inner


@input_error
def add_contact(contact):
    if not contact:
        raise ValueError("Give me user name please")
    elif not contact[0].isalpha():
        raise ValueError("Enter correct username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name):
            raise KeyError("Contact already exists")
        else:
            if len(contact) == 1:
                username_record = Record(name)
                phone_book.add_contact(username_record)
                return f'Contact {name} has been added to the phone book'
            else:
                try:
                    birthday = contact[1]
                    username_record = Record(name, birthday)
                    phone_book.add_contact(username_record)
                    return f'Contact {name} with birthday {birthday} has been added to the phone book'
                except ValueError:
                    raise ValueError('Invalid data format')


@input_error
def add_phone(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) == 1:
            raise IndexError("Enter phone please")
        else:
            try:
                phone = contact[1]
                phone_book.get(name).add_phone(phone)
                return f'Phone {phone} has been added to contact {name}'
            except ValueError:
                raise ValueError("Invalid phone number")


@input_error
def remove_phone(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) == 1:
            raise IndexError("Enter phone please")
        else:
            try:
                phone = contact[1]
                phone_book.get(name).remove_phone(phone)
                return f'Phone {phone} has been removed from contact {name}'
            except ValueError:
                raise ValueError("Invalid or non-existent phone number")


@input_error
def edit_phone(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) < 3:
            raise IndexError("Enter two phone number please")
        else:
            try:
                old_phone = contact[1]
                new_phone = contact[2]
                phone_book.get(name).edit_phone(old_phone, new_phone)
                return f'Phone number {old_phone} has been changed to {new_phone} for contact {name}'
            except ValueError:
                raise ValueError("Invalid or non-existent phone number")


@input_error
def find_phone(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) == 1:
            raise IndexError("Enter phone please")
        else:
            try:
                phone = contact[1]
                phone_book.get(name).find_phone(phone)
                return phone
            except ValueError:
                raise ValueError("Invalid phone number")


@input_error
def days_to_birthday(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        else:
            try:
                days = phone_book.get(name).days_to_birthday
                return days
            except AttributeError:
                raise AttributeError("No information about this user's birthday")


@input_error
def find_user(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        return phone_book.get(name)


@input_error
def delete_user(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name):
            phone_book.delete(name)
            return f'Contact {name} has been deleted from the phone book'


@input_error
def find_info(info):
    return phone_book.find_info(info[0])


def show_all():
    if not phone_book.data:
        return "No users available"
    msg = Interface("\n".join(str(record) for record in phone_book.data.values()))
    return msg.show_all_contacts()


@input_error
def show(contact):
    if not contact:
        raise IndexError("Enter a number of elements")
    n = int(contact[0])
    if n > len(phone_book):
        raise ValueError(f"This number is too big, length of phone book is {len(phone_book)}")
    else:
        page = phone_book.iterator(n)
        for elem in page:
            if elem:
                print(elem)


@input_error
def add_birthday(contact):
    if not contact:
        raise ValueError("Enter username and birthday please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) == 1:
            raise IndexError("Enter birthday please")
        else:
            try:
                birthday = contact[1]
                phone_book.get(name).add_birthday(birthday)
                return f'Birthday {birthday} has been added to contact {name}'
            except ValueError:
                raise ValueError("Invalid birthday")


@input_error
def birthday_in(contact):
    if not contact:
        raise ValueError("Enter the number of days")
    number = int(contact[0])
    list_of_birthday_contacts = phone_book.birthday_in_a_given_number_of_days(number)
    return f"{','.join((birthday for birthday in list_of_birthday_contacts))} birthday is in {number} days"


@input_error
def add_secondname(contact):
    if not contact:
        raise ValueError("Enter username and secondname please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) == 1:
            raise IndexError("Enter secondname please")
        else:
            try:
                secondname = contact[1]
                phone_book.get(name).add_secondname(secondname.capitalize())
                return f'Secondname {secondname.capitalize()} has been added to contact {name}'
            except ValueError:
                raise ValueError("Invalid secondname")


@input_error
def edit_secondname(contact):
    if not contact:
        raise ValueError("Enter username and secondname please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) == 1:
            raise IndexError("Enter secondname please")
        else:
            try:
                secondname = contact[1]
                phone_book.get(name).edit_secondname(secondname.capitalize())
                return f'Secondname {secondname.capitalize()} has been edited to contact {name}'
            except ValueError:
                raise ValueError("Invalid secondname")


@input_error
def add_address(contact):
    if not contact:
        raise ValueError("Enter address please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) == 1:
            raise IndexError("Enter address please")
        else:
            address = ' '.join(contact[1:])
            phone_book.get(name).add_address(address.capitalize())
            return f'Address {address} has been added to contact {name}'


@input_error
def remove_address(contact):
    if not contact:
        raise ValueError("Enter address please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) == 1:
            raise IndexError("Enter address please")
        else:
            phone_book.get(name).remove_address()
            return f'Address has been removed from contact {name}'


@input_error
def edit_address(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        else:
            new_address = ' '.join(contact[1:])
            phone_book.get(name).edit_address(new_address.capitalize())
            return f'Address has been changed to {new_address} for contact {name}'


@input_error
def add_email(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) == 1:
            raise IndexError("Enter email please")
        else:
            try:
                email = contact[1]
                phone_book.get(name).add_email(email)
                return f'Email {email} has been added to contact {name}'
            except ValueError:
                raise ValueError("Invalid email")


@input_error
def remove_email(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        else:
            phone_book.get(name).remove_email()
            return f'Email has been removed from contact {name}'


@input_error
def edit_email(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) < 3:
            raise IndexError("Enter two emails please")
        else:
            try:
                old_email = contact[1]
                new_email = contact[2]
                phone_book.get(name).edit_email(old_email, new_email)
                return f'Email {old_email} has been changed to {new_email} for contact {name}'
            except ValueError:
                raise ValueError("Invalid or non-existent email")


def file_sort(contact):
    if not contact:
        raise ValueError("Enter directory path")
    else:
        name = ' '.join(i for i in contact)
        file_sorter = FileSorter(name)
        ok, msg = file_sorter.execute_sort()
        return f'ok: {ok}\nmsg: {msg}\n{"-" * 10}'


def add_note():
    title = input("Enter note title: ")
    text = input("Enter note text: ")
    tags = input("Enter note tags: ")
    notebook.add_note(title, text, tags)
    return f"Note {title} added successfully"


def edit_note():
    index = int(input("Enter index of the note you want to edit: "))
    new_title = input("Enter new title: ")
    new_text = input("Enter new text: ")
    new_tags = input("Enter new tags: ")
    notebook.edit_note(index, new_title, new_text, new_tags)
    return "Note edited successfully"


def delete_note_by_index():
    index = int(input("Enter index of the note you want to delete: "))
    notebook.delete_note_by_index(index)
    return "Note deleted successfully"


def delete_note_by_title():
    title = input("Enter title of the note you want to delete: ")
    notebook.delete_note_by_title(title)
    return "Note deleted successfully"


def add_note_tags():
    index = int(input("Enter index of the note you want to add tag: "))
    tags = input("Enter tags to add: ")
    notebook.add_note_tags(index, tags)
    return "Tag added successfully"


def search_note_by_tag():
    tag = input("Enter tag to search notes: ")
    search_results = notebook.search_by_tag(tag)
    print("Search results:")
    for note in search_results:
        print(note)


def sort_notes_by_tag():
    sorted_notes = notebook.sort_notes_by_tag()
    print("Sorted notes:")
    for note in sorted_notes:
        print(note)


def notes_show_all():
    all_notes = notebook.show_all()
    print("All notes:")
    for index, note in enumerate(all_notes):
        msg = Interface(str(index))
        print(msg.show_all_notes(), note)


def search_note_by():
    qwerty = input("Enter what u want to search for: ")
    result = notebook.search_full(qwerty)
    print("Search results:")
    for note in result:
        print(note)


def final():
    msg = Interface('Good bye!')
    return msg.final()


def greeting():
    msg = Interface(instruction)
    return msg.help()


command_dict1 = {"good bye": final, "close": final, "exit": final, "hello": greeting, "show all": show_all,
                 'add_note': add_note, 'edit_note': edit_note, 'add_note_tags': add_note_tags,
                 'delete_note_by_idx': delete_note_by_index, 'delete_note_by_title': delete_note_by_title,
                 'search_note_by_tag': search_note_by_tag, 'sort_notes_by_tag': sort_notes_by_tag,
                 'search_note_by': search_note_by, 'notes_show_all': notes_show_all}

command_dict2 = dict(add_contact=add_contact, add_phone=add_phone, remove_phone=remove_phone, find_phone=find_phone,
                     edit_phone=edit_phone, days=days_to_birthday, find_user=find_user, delete_user=delete_user,
                     find_info=find_info, show=show, add_birthday=add_birthday, birthday_in=birthday_in,
                     add_secondname=add_secondname,
                     edit_secondname=edit_secondname, file_sorter=file_sort, add_address=add_address,
                     edit_address=edit_address, remove_address=remove_address, add_email=add_email,
                     edit_email=edit_email, remove_email=remove_email)


def get_handler1(x):
    return command_dict1[x]


def get_handler2(x):
    return command_dict2[x]


def main():
    global phone_book
    global notebook
    try:
        phone_book = phone_book.read_from_file(filename='phone_book.bin')
    except FileNotFoundError:
        phone_book = AddressBook()
    notebook = NoteBook()
    notebook.read_from_file()
    while True:
        command = input().lower().strip()

        if command in command_dict1:
            result = get_handler1(command)()
            if result is not None:
                print(result)
            if result == "Good bye!":
                phone_book.save_to_file(filename='phone_book.bin')
                notebook.save_to_file()
                break
        else:
            command = command.split(" ")
            contact = command[1:]

            if command[0] in command_dict2 and contact:
                result = get_handler2(command[0])(contact)
                if result is not None:
                    print(result)
            elif command[0] in command_dict2 and not contact:
                result = get_handler2(command[0])(contact)
                if result is not None:
                    print(result)
            else:
                print("This is an incorrect command. Try again, please")


if __name__ == "__main__":
    main()
