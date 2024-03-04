from collections import UserDict, UserList
import pickle
import os


class Note(UserDict):
    def __init__(self, title: str, text: str, tags=None):
        tags = '' if tags is None or not tags else tags
        super().__init__({'title': title, 'text': text, 'tags': tags})

    def __str__(self):
        return f'Title: {self.data["title"]}\nTags: {self.data["tags"]}\nText: {self.data["text"]}\n'

    def text_view_full(self):
        return f'{self.data["title"]} {self.data["tags"]} {self.data["text"]}'


class NoteBook(UserList):
    def __init__(self):
        super().__init__()
        self.data_file_name = 'notebook_data.bin'
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.data_file_path = os.path.join(self.current_directory, self.data_file_name)

    def save_to_file(self):
        with open(self.data_file_path, 'wb') as file:
            pickle.dump(self.data, file)

    def read_from_file(self):
        if os.path.exists(self.data_file_path):
            with open(self.data_file_path, 'rb') as file:
                self.data = pickle.load(file)
        else:
            self.data = []

    def add_note(self, title: str, text: str, tags: str):
        self.data.append(Note(title, text, tags))

    def add_note_tags(self, index: int, tags: str):
        if 0 <= index < len(self.data):
            self.data[index].data['tags'] += tags if self.data[index].data['tags'] else tags
        else:
            raise IndexError(f'Note with index "{index}" does not exist')

    def edit_note(self, index, new_title, new_text, new_tags):
        if 0 <= index < len(self.data):
            self.data[index] = Note(new_title, new_text, new_tags)
        else:
            raise IndexError(f'Note with index "{index}" does not exist')

    def delete_note_by_index(self, index: int):
        if 0 <= index < len(self.data):
            del self.data[index]
        else:
            raise IndexError(f'Note with index "{index}" does not exist')

    def delete_note_by_title(self, title: str):
        indexes_to_delete = [index for index, note in enumerate(self.data) if title in note.data["title"]]
        for index in indexes_to_delete:
            self.delete_note_by_index(index)

    def search_full(self, query: str):
        return [note for note in self.data if query in
                ' '.join([note.data["title"], note.data["tags"], note.data["text"]])]

    def search_by_tag(self, tag):
        return [note for note in self.data if tag in note.data['tags']]

    def sort_notes_by_tag(self):
        return sorted(self.data, key=lambda note: note.data['tags'])

    def show_all(self):
        return [note for note in self.data]


# if __name__ == '__main__':
#
#     from colorama import init
#
#     init()
#
#
#     class TextStyle:
#         RESET = '\033[0m'
#         # Font style
#         BOLD = '\033[1m'
#         UNDERLINE = '\033[4m'
#         # Font color
#         BLACK = '\033[30m'
#         RED = '\033[31m'
#         GREEN = '\033[32m'
#         YELLOW = '\033[33m'
#         BLUE = '\033[34m'
#         MAGENTA = '\033[35m'
#         CYAN = '\033[36m'
#         WHITE = '\033[37m'
#         # Background color
#         BG_BLACK = '\033[40m'
#         BG_RED = '\033[41m'
#         BG_GREEN = '\033[42m'
#         BG_YELLOW = '\033[43m'
#         BG_BLUE = '\033[44m'
#         BG_MAGENTA = '\033[45m'
#         BG_CYAN = '\033[46m'
#         BG_WHITE = '\033[47m'
#
#
#     def print_colorful_test_title(text):
#         print(TextStyle.BOLD + TextStyle.CYAN + '{:^50}'.format(text), end=TextStyle.RESET + '\n\n')
#
#
#     def print_colorful_note(index, note):
#         print(TextStyle.RED + 'Index: ' + TextStyle.RESET + str(index) + '\n' +
#               TextStyle.BLUE + 'Title: ' + TextStyle.RESET + note.data["title"] + '\n' +
#               TextStyle.MAGENTA + 'Tags: ' + TextStyle.RESET + note.data["tags"] + TextStyle.RESET + '\n' +
#               TextStyle.YELLOW + 'Text: ' + TextStyle.RESET + note.data["text"], end='\n\n')
#
#
#     def print_colorful_delimiter():
#         print(TextStyle.GREEN + f'{"=" * 50}', end=TextStyle.RESET + '\n\n')
#
#
#     notebook = NoteBook()
#
#     print(TextStyle.BG_GREEN + TextStyle.BOLD + TextStyle.BLACK +
#           '{:^50}'.format('Test NoteBook test'),
#           end=TextStyle.RESET + '\n\n')
#
#     # add notes
#     print_colorful_test_title('Add several notes')
#     notebook.add_note('#2 note', 'Second note test text apple', 'tag2 python3')
#     notebook.add_note('#3 note', 'Third note test text grape', 'tag3 java')
#     notebook.add_note('#5 note', 'Third note test text cherry', 'tag5 php')
#     notebook.add_note('#4 note', 'Third note test text melon', 'tag4 java')
#     notebook.add_note('#1 note', 'First note test text grape', 'tag1 python2')
#
#     # show all notes
#     print_colorful_delimiter()
#     print_colorful_test_title('Show all notes')
#     all_notes = notebook.show_all()
#     for i, n in enumerate(all_notes):
#         print_colorful_note(i, n)
#
#     # edit note
#     print_colorful_delimiter()
#     print_colorful_test_title('Edit note with index 0')
#     notebook.edit_note(0, 'Edited note with index 0',
#                        'Edited note text text',
#                        'tag3 edited')
#     print_colorful_test_title('Edited notes')
#     all_notes = notebook.show_all()
#     for i, n in enumerate(all_notes):
#         print_colorful_note(i, n)
#
#     # search note by word
#     print_colorful_delimiter()
#     print_colorful_test_title('Full search notes by word "grape"')
#     search_results = notebook.search_full('grape')
#     for i, n in enumerate(all_notes):
#         print_colorful_note(i, n)
#
#     # search note by tag
#     print_colorful_delimiter()
#     print_colorful_test_title('Search notes by tag "python"')
#     search_results = notebook.search_by_tag('python')
#     for i, n in enumerate(all_notes):
#         print_colorful_note(i, n)
#
#     # delete note by index
#     print_colorful_delimiter()
#     print_colorful_test_title('Delete note with index 0')
#     notebook.delete_note_by_index(0)
#     all_notes = notebook.show_all()
#     for i, n in enumerate(all_notes):
#         print_colorful_note(i, n)
#
#     # delete note by word match in title
#     print_colorful_delimiter()
#     print_colorful_test_title('Delete note by word "#4" match in title')
#     notebook.delete_note_by_title('#4')
#     all_notes = notebook.show_all()
#     for i, n in enumerate(all_notes):
#         print_colorful_note(i, n)
#
#     # saving note data to file
#     print_colorful_delimiter()
#     print_colorful_test_title('Save note data to file')
#     notebook.save_to_file()
#
#     # clear notebook
#     print_colorful_test_title('Clear notebook')
#     notebook.data = []
#
#     # loading note data from file
#     print_colorful_test_title('Load note data to file')
#     notebook.read_from_file()
#     all_notes = notebook.show_all()
#     for i, n in enumerate(all_notes):
#         print_colorful_note(i, n)
#
#     # add several notes for test sorting
#     print_colorful_delimiter()
#     print_colorful_test_title('Add several notes for test sorting')
#     notebook.add_note('Test sort note2', 'Second note test text', 'tag6')
#     notebook.add_note('Test sort note1', 'Second note test text', 'tag5')
#
#     # show all notes before sorting
#     print_colorful_test_title('Show all notes BEFORE sorting')
#     all_notes = notebook.show_all()
#     for i, n in enumerate(all_notes):
#         print_colorful_note(i, n)
#
#     # sorting notes by tag
#     print_colorful_delimiter()
#     print_colorful_test_title('Sorting notes by tag')
#     sorted_notes = notebook.sort_notes_by_tag()
#
#     # show notes after sorting
#     print_colorful_test_title('Show all notes AFTER sorting')
#     for i, n in enumerate(all_notes):
#         print_colorful_note(i, n)
#
#     print_colorful_delimiter()
#     print_colorful_test_title('Clear notebook')
#     notebook.data = []
#     print_colorful_test_title('Add note without tag')
#     notebook.add_note('Test sort note2', 'Second note test text', '')
#     all_notes = notebook.show_all()
#     for i, n in enumerate(all_notes):
#         print_colorful_note(i, n)
#
#     print_colorful_test_title('Add tag to existing note with index 0')
#     notebook.add_note_tags(0, 'tag15')
#     all_notes = notebook.show_all()
#     for i, n in enumerate(all_notes):
#         print_colorful_note(i, n)
