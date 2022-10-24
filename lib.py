import datetime
import os


class Entity:
    def __init__(self, token, parent=None):
        self.token = token
        time_stamp = datetime.datetime.now()
        self.created_at = time_stamp
        self.last_modified_at = time_stamp
        self.parent = parent

    def update_time_stamp(self):
        self.last_modified_at = datetime.datetime.now()


class File(Entity):
    def __init__(self, token, size=0):
        Entity.__init__(self, token)
        self.size = size  # in bytes
        self.mode = None  # 'r' | 'w'
        self.enabled = False

    def __str__(self):
        return f"{self.token}: size: {self.size}"

    def retoken_file(self, token, new_token):
        file = self.find_file(token)

        if file:
            file.token = new_token
            return

    def update_content(self, content):
        self.content = content
        self.update_size()

    def get_content(self):
        return self.content

    def update_size(self):
        self.size = len(self.get_content())

    def get_size(self):
        return self.size

    def __str__(self):
        return f"{self.token}: size: {self.size} Enabled: {self.enabled}"


class Folder(Entity):
    def __init__(self, token):
        Entity.__init__(self, token)
        self.children = {}

    def __str__(self):
        file_count = len(
            list(filter(lambda child: isinstance(child, File), self.children.values()))
        )
        folder_count = len(
            list(
                filter(lambda child: isinstance(child, Folder), self.children.values())
            )
        )
        return f"{self.token}: {file_count} files and {folder_count} folders" ""

    def add(self, entity: Entity):
        if self.find(entity.token):
            raise Exception("Entity already exists!")

        if entity != self:
            self.children[entity.token] = entity
            entity.parent = self

    def delete(self, token):
        entity = self.find(token)

        if entity:
            del self.children[entity.token]
            entity.parent = None
        else:
            raise Exception("Entity not found!")

    def get_size(self):
        size = 0
        for child in self.children.values():
            size += child.get_size()
        return size

    def ls(self):
        for child in self.children.values():
            print(child)

    def find(self, token):
        if token in self.children:
            return self.children[token]
        return None


class Manager:
    def __init__(self):
        self.root = Folder(token="~")
        self.cwd = self.root
        self.open_files = {}

    def create(self, token):
        file = File(token)
        file.mode = "w"
        self.cwd.add(file)
        return file

    def delete(self, path):
        entity = self.find(path)

        if entity:
            entity.parent.delete(entity.token)
            entity.parent = None
        else:
            raise Exception("Entity not found!")

    def mkdir(self, token):
        folder = Folder(token)
        self.cwd.add(folder)

    def ls(self):
        self.cwd.ls()

    def find(self, path):
        path_array = path.split("/")

        if len(path_array) == 1:
            return self.cwd.find(path)

        if path_array[0] == "~":
            entity = self.root
        elif path_array[0] == "..":
            entity = self.cwd.parent
        else:
            entity = self.cwd

        for index, token in enumerate(path_array[1:]):
            if token == "~" or token == ".":
                raise Exception("Invalid path!")

            if token == "" and index == len(path_array) - 2:
                continue

            if token == "..":
                entity = entity.parent
                continue

            entity = entity.find(token)

            if not isinstance(entity, Folder) and token != path_array[-1]:
                return None

        return entity

    def chDir(self, path):

        if path == "~":
            self.cwd = self.root
            return

        entity = self.find(path)

        if entity:
            self.cwd = entity
        else:
            raise Exception("Entity not found!")

    def open(self, path, mode):  #
        file = self.find(path)

        if file:
            file.mode = mode
            if file.mode == "r":
                self.open_files[
                    path
                ] = file  # Using path as key / Can be changed to file.token
                print("File:", file.token, "opened for reading.")
            elif file.mode == "w":
                self.open_files[path] = file
                file.enabled = True
                print("File:", file.token, "opened for reading.")

            return file  # Returning object
            # content = file.get_content()
            # return content

        else:
            raise Exception("Entity not found!")

    def close(self, path):
        file = self.find(path)
        if file:
            file.mode = None
            file.enabled = False
            del self.open_files[path]
            print("File:", file.token, "closed.")
        else:
            raise Exception("Entity not found!")

    def move(self, source, destination):
        entity = self.find(source)
        new_entity = self.find(destination)
        if entity and new_entity:
            entity.parent.delete(entity.token)
            new_entity.add(entity)
        else:
            raise Exception("Entity not found!")

    def write_to_file(self, path, content):

        if path in self.open_files:
            file = self.open_files[path]
            if file.enabled:
                file.update_content(content)
            else:
                raise Exception("Entity not enabled for writing!")
        else:
            raise Exception("Entity not found!")

    def read_from_file(self, path):
        if path in self.open_files:
            file = self.open_files[path]
            return file.get_content()

        else:
            raise Exception("Entity not found!")
