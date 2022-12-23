from MemoryManager import MemoryManager, Memory
from Nodes import FileNode, DirectoryNode
import json
import datetime


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


class FileManager:
    def __init__(self):
        self.root = DirectoryNode(token="~")
        self.cwd = self.root
        self.memory_manager = MemoryManager()

        file = open("memory_map.json", "r")
        data = json.load(file)
        self.load_children(self.root, data["children"])
        file.close()

    def create_file(self, token):
        file = FileNode(token, self.memory_manager, self)
        file.created_at = datetime.datetime.now()
        self.cwd.add(file)
        self.save()

    def delete(self, path):
        entity = self.find(path)

        if entity:
            entity.parent.delete(entity.token)
            entity.parent = None
            self.save()

            if hasattr(entity, "chunks") and entity.chunks:
                self.memory_manager.deallocate(entity.chunks)
        else:
            raise Exception("Invalid Path!")

    def mkdir(self, token):
        folder = DirectoryNode(token)
        self.cwd.add(folder)
        self.save()

    def chDir(self, path):
        if path == "~":
            self.cwd = self.root
            return

        entity = self.find(path)

        if entity and isinstance(entity, DirectoryNode):
            self.cwd = entity
        else:
            raise Exception("Invalid directory path!")

    def move(self, source, destination):
        entity = self.find(source)
        new_entity = self.find(destination)

        if entity and new_entity:
            entity.parent.delete(entity.token)
            new_entity.add(entity)
            self.save()
        else:
            raise Exception("Entity not found!")

    def open(self, path, mode):
        file = self.find(path)

        if not file or isinstance(file, DirectoryNode):
            raise Exception("Invalid file path!")

        if file.mode == None:
            file.mode = mode
        else:
            raise Exception("FileNode is already open!")

        return file

    def close(self, path):
        file = self.find(path)

        if not file or isinstance(file, DirectoryNode):
            raise Exception("Invalid file path!")

        if file:
            file.mode = None
        else:
            raise Exception("File not found!")

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

            if not isinstance(entity, DirectoryNode) and token != path_array[-1]:
                return None

        return entity

    def load_children(self, folder, children):
        for child in children:
            if children[child]["type"] == "folder":
                dir = DirectoryNode(token=child)
                folder.add(dir)

                dir.created_at = datetime.datetime.strptime(children[child]["created_at"], "%Y-%m-%d %H:%M:%S.%f")

                dir.last_modified_at = datetime.datetime.strptime(
                    children[child]["last_modified_at"], "%Y-%m-%d %H:%M:%S.%f"
                )

                self.load_children(
                    dir,
                    children[child]["children"],
                )
            else:
                file = FileNode(token=child, memory_manager=self.memory_manager, file_manager=self)

                file.size = children[child]["size"]
                file.chunks = []

                for chunk in children[child]["chunks"]:
                    file.chunks.append(Memory(chunk["block_num"], chunk["offset"], chunk["limit"]))

                file.created_at = datetime.datetime.strptime(children[child]["created_at"], "%Y-%m-%d %H:%M:%S.%f")

                file.last_modified_at = datetime.datetime.strptime(
                    children[child]["last_modified_at"], "%Y-%m-%d %H:%M:%S.%f"
                )

                folder.add(file)

    def save(self):
        file = open("memory_map.json", "w")
        file.write(json.dumps(self.root.get_JSON(), indent=2))
        file.close()

    def format(self):
        self.memory_manager.format_drive()
        self.root = DirectoryNode(token="~")
        self.cwd = self.root
        self.save()

    def memory_map(self):
        return json.dumps(self.root.get_JSON(), indent=2)
