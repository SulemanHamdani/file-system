import datetime
import os
import json
from memory_manager import MemoryManager

memManager = MemoryManager()


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
        self.chunks = []
        self.content = ""

    def __str__(self):
        return f"{self.token}: size: {self.size}"

    def retoken_file(self, token, new_token):
        file = self.find_file(token)

        if file:
            file.token = new_token
            return

    def save(self):
        memManager.deallocate(self.chunks)
        self.save_to_mem()
        self.last_modified_at = datetime.datetime.now()

    def get_content(self):
        self.content = self.load_from_mem()
        return self.content

    def update_size(self):
        self.size = len(self.get_content())

    def get_size(self):
        return self.size

    def __str__(self):
        return f"{self.token}: size: {self.size} Enabled: {self.enabled}"

    def write_to_file(self, content):
        if self.mode == "w":
            self.content = self.get_content() + content
            self.size = len(self.content)
            self.save()  # Saving to memory
        else:
            raise Exception("Entity not enabled for writing!")

    def read_from_file(self):
        return self.get_content()

    def write_to_file_at(self, content, offset):
        if self.mode == "w":
            txt = self.get_content()
            txt = txt[:offset] + content + txt[offset:]
            self.content = txt
            self.size += len(content)
            self.update_content()

        else:
            raise Exception("Entity not enabled for writing!")

    def read_from_file_at(self, offset, size):  # When size is defined
        if self.mode == "r" or self.mode == "w":
            txt = self.get_content()
            return txt[offset : offset + size]

        else:
            raise Exception("Entity not open!")

    def read_from_file_at(self, offset):  # When size is not defined
        if self.mode == "r" or self.mode == "w":
            txt = self.get_content()
            return txt[offset:]

        else:
            raise Exception("Entity not open!")

    def move_content_in_file(self, source, size, destination):
        if self.mode == "w":
            txt = self.get_content()
            txt = txt[:source] + txt[source + size :]
            txt = txt[:destination] + txt[source : source + size] + txt[destination:]
            self.content = txt
            self.update_size

        else:
            raise Exception("Entity not enabled for writing!")

    def chunkify(self, start, size):
        txt = self.content[start : start + size]
        return txt

    def save_to_mem(self):
        start = 0
        mem = memManager.allocate(self.size)
        for chunk in mem:
            chunk_size = chunk.limit - chunk.offset
            chunk.content = self.chunkify(start, chunk_size)
            memManager.write_content(chunk, chunk.content)
            start += chunk_size
            self.chunks.append(chunk)

    def load_from_mem(self):
        txt = ""

        for chunk in self.chunks:
            txt += memManager.get_content(chunk)

        return txt

    def get_JSON(self):
        return {
            "created_at": self.created_at.__str__(),
            "last_modified_at": self.last_modified_at.__str__(),
            "type": "file",
            "size": self.size,
        }


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

    def get_JSON(self):
        children = {}

        for child in self.children.values():
            children[child.token] = child.get_JSON()

        return {
            "type": "folder",
            "created_at": self.created_at.__str__(),
            "last_modified_at": self.last_modified_at.__str__(),
            "children": children,
        }


class FileManager:
    def __init__(self):
        self.root = Folder(token="~")
        self.cwd = self.root
        self.boot_up()

    def create(self, token):
        file = File(token)
        file.mode = "w"
        file.created_at = datetime.datetime.now()
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

        if entity and isinstance(entity, Folder):
            self.cwd = entity
        else:
            raise Exception("Invalid directory path!")

    def open(self, path, mode):
        file = self.find(path)

        if file:
            file.mode = mode
        else:
            raise Exception("Entity not found!")

        return file

    def close(self, path):
        file = self.find(path)
        if file:
            if file.mode == None:
                print("File is not opened!")
            else:
                file.mode = None
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

    def boot_up(self):
        data = json.load(open("memory_map.json"))
        self.load_children(self.root, data["children"])

    def load_children(self, folder, children):
        for child in children:
            if children[child]["type"] == "folder":

                dir = Folder(token=child)
                folder.add(dir)

                dir.created_at = datetime.datetime.strptime(
                    children[child]["created_at"], "%Y-%m-%d %H:%M:%S.%f"
                )

                dir.last_modified_at = datetime.datetime.strptime(
                    children[child]["last_modified_at"], "%Y-%m-%d %H:%M:%S.%f"
                )

                self.load_children(
                    dir,
                    children[child]["children"],
                )
            else:
                file = File(
                    token=child,
                    size=children[child]["size"],
                )

                file.created_at = datetime.datetime.strptime(
                    children[child]["created_at"], "%Y-%m-%d %H:%M:%S.%f"
                )

                file.last_modified_at = datetime.datetime.strptime(
                    children[child]["last_modified_at"], "%Y-%m-%d %H:%M:%S.%f"
                )

                folder.add(file)

    def dump_JSON(self):
        file = open("memory_map.json", "w")
        file.write(json.dumps(self.root.get_JSON(), indent=2))
