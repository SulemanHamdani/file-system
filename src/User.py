class OpenedFile:
    def __init__(self, file, mode):
        self.file = file
        self.mode = mode


class User:
    def __init__(self, name):
        self.name = name
        self.opened_files = []

    def open_file(self, file, mode):
        self.opened_files.append(OpenedFile(file, mode))

    def close_file(self, file):
        for opened_file in self.opened_files:
            if opened_file.file == file:
                self.opened_files.remove(opened_file)
                return
