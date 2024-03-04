import os
import shutil
from pathlib import Path


class FileSorter:

    def __init__(self, path_to_dir=None):
        self.path_to_dir = path_to_dir
        self.result_msg = ''
        self.files_by_type = {}
        self.known_extensions = set()
        self.unknown_extensions = set()
        self.file_types = {
            'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
            'archives': ['ZIP', 'GZ', 'TAR'],
            'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
            'images': ['BMP', 'WEBP', 'JPEG', 'PNG', 'JPG', 'SVG'],
            'video': ['AVI', 'MP4', 'MOV', 'MKV'],
            'others': []
        }
        self.transliterate_map = {
            # lowercase letters
            ord('а'): 'a', ord('б'): 'b', ord('в'): 'v', ord('г'): 'g', ord('д'): 'd',
            ord('е'): 'e', ord('ё'): 'e', ord('ж'): 'zh', ord('з'): 'z', ord('и'): 'i',
            ord('й'): 'y', ord('к'): 'k', ord('л'): 'l', ord('м'): 'm', ord('н'): 'n',
            ord('о'): 'o', ord('п'): 'p', ord('р'): 'r', ord('с'): 's', ord('т'): 't',
            ord('у'): 'u', ord('ф'): 'f', ord('х'): 'kh', ord('ц'): 'ts', ord('ч'): 'ch',
            ord('ш'): 'sh', ord('щ'): 'sch', ord('ъ'): '', ord('ы'): 'y',
            ord('ь'): '', ord('э'): 'e', ord('ю'): 'yu', ord('я'): 'ya',
            # uppercase letters
            ord('А'): 'A', ord('Б'): 'B', ord('В'): 'V', ord('Г'): 'G', ord('Д'): 'D',
            ord('Е'): 'E', ord('Ё'): 'E', ord('Ж'): 'Zh', ord('З'): 'Z', ord('И'): 'I',
            ord('Й'): 'Y', ord('К'): 'K', ord('Л'): 'L', ord('М'): 'M', ord('Н'): 'N',
            ord('О'): 'O', ord('П'): 'P', ord('Р'): 'R', ord('С'): 'S', ord('Т'): 'T',
            ord('У'): 'U', ord('Ф'): 'F', ord('Х'): 'Kh', ord('Ц'): 'Ts', ord('Ч'): 'Ch',
            ord('Ш'): 'Sh', ord('Щ'): 'Sch', ord('Ъ'): '', ord('Ы'): 'Y', ord('Ь'): '',
            ord('Э'): 'E', ord('Ю'): 'Yu', ord('Я'): 'Ya',
            # additional Ukrainian lowercase letters
            ord('ґ'): 'g', ord('є'): 'ye', ord('ї'): 'yi', ord('і'): 'i',
            # additional Ukrainian uppercase letters
            ord('Ґ'): 'G', ord('Є'): 'Ye', ord('Ї'): 'Yi', ord('І'): 'I',
        }

    def check_directory_exist_and_permissions(self) -> tuple[bool, str]:
        """
        Check the existence of the folder, the presence of files within it, and the app's read/write permissions
        :return: boolean of check and comment if false
        :return type: tuple
        """
        if not self.path_to_dir:
            return False, 'Folder path not specified'
        if not os.path.exists(self.path_to_dir):
            return False, f'Directory "{self.path_to_dir}" not exist!'
        if not os.listdir(self.path_to_dir):
            return False, 'Specified folder is empty'
        if not os.access(self.path_to_dir, os.R_OK):
            return False, f"Not enough permissions to read from directory: {self.path_to_dir}"
        if not os.access(self.path_to_dir, os.W_OK):
            return False, f"Not enough permissions to write to directory: {self.path_to_dir}"
        return True, ''

    def find_file_type(self, file) -> str:
        """
        Search for a file type based on specified conditions from the dictionary (file_types)

        :param file: Path object
        :return: recognized file type or 'others'
        :return type: string
        """
        extension = file.name if file.name.startswith('.') else file.suffix[1:]
        found_file_type = None

        for file_type, extensions in self.file_types.items():
            if extension.upper() in extensions:
                found_file_type = file_type
                self.known_extensions.add(extension.upper())

        if found_file_type is None:
            found_file_type = 'others'
            if extension:
                self.unknown_extensions.add(extension.upper())

        if found_file_type not in self.files_by_type:
            self.files_by_type.setdefault(found_file_type, set()).add(self.normalize(file))
        else:
            self.files_by_type[found_file_type].add(self.normalize(file))

        return found_file_type

    def normalize(self, file, with_ext: bool = True) -> str:
        """
        Transliterate filename
        - Cyrillic characters are converted. 
        - The Latin alphabet and numbers remain as is. 
        - The remaining characters are replaced with "_"
        - File extension does not change

        :param file: Path object
        :param with_ext: default return filename with extension
        :type with_ext: bool
        :return: Transliterate in latin
        :return type: string
        """
        # in Linux/Unix OS hidden files have name are starts with dot
        if file.name.startswith('.'):
            return file.name

        normalized_filename = ''
        filename = file.stem

        for char in filename:
            ord_char = ord(char)
            # english letters and digits added as is
            # english uppercase letters Unicode codes 65-90
            # english lowercase letters Unicode codes 97-122
            if char.isdigit() or \
                    (65 <= ord_char <= 90) or \
                    (97 <= ord_char <= 122):
                normalized_filename += char
            else:
                normalized_filename += self.transliterate_map.get(ord_char, '_')

        return normalized_filename if not with_ext else str(normalized_filename + file.suffix)

    def sort(self, path: Path):
        """
        Recursive function for sorting files 
        - File names are transliterated by function 'normalize'
        - Files are transferred to folders according to file type
        - Archives are unpacked into a folder 'archives' into the same name folder without extension
        - Broken archives are deleted

        :param path: directory for sort
        :type path: Path object
        """

        for item in path.iterdir():
            if item.is_file():
                item_file_type = self.find_file_type(item)
                path_to_replace = self.path_to_dir.joinpath(item_file_type)
                path_to_replace.mkdir(exist_ok=True)
                if item_file_type == 'archives':
                    try:
                        shutil.unpack_archive(
                            item.absolute(), self.path_to_dir.joinpath(
                                path_to_replace, self.normalize(item, with_ext=False)
                            ).as_posix()
                        )
                    except shutil.ReadError:
                        print(f'Archive is broken: {item.absolute()}')
                    finally:
                        item.unlink()
                else:
                    item.replace(self.path_to_dir.joinpath(path_to_replace, self.normalize(item)))

            elif item.is_dir():
                # if that is work folder of script
                if item.name in self.file_types:
                    continue
                self.sort(item)

        if not any(path.iterdir()):
            path.rmdir()

    def execute_sort(self) -> tuple[bool, str]:
        """
        Run sorting
        :return: result of sorting: bool and msg
        :return type: tuple
        """
        valid, comment = self.check_directory_exist_and_permissions()

        if valid:
            self.path_to_dir = Path(self.path_to_dir).absolute()
            self.sort(self.path_to_dir)

            if self.known_extensions:
                comment = (f'\nResult of sort files in directory:\n{self.path_to_dir}\n\n'
                           f'Known extensions: {", ".join(sorted(self.known_extensions))}\n\n'
                           f'Unknown extensions: {", ".join(sorted(self.unknown_extensions))}\n\n'
                           f'Files by type in target directory:')

                for file_category, files in self.files_by_type.items():
                    comment += f'[{file_category}]:\n{", ".join(sorted(files))}\n\n'
            else:
                comment = 'It looks like the specified folder is already sorted'

        return valid, comment


# if __name__ == '__main__':
#
#     file_sorter = FileSorter('')
#     ok, msg = file_sorter.execute_sort()
#     print(f'ok: {ok}\nmsg: {msg}\n{"-"*10}')
#
#     file_sorter = FileSorter('not_exist_folder')
#     ok, msg = file_sorter.execute_sort()
#     print(f'ok: {ok}\nmsg: {msg}\n{"-"*10}')
#
#     file_sorter = FileSorter('test_dir_files')
#     ok, msg = file_sorter.execute_sort()
#     print(f'ok: {ok}\nmsg: {msg}\n{"-"*10}')
