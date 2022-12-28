import datetime
import os
import json
import threading


class Entity:
    def __init__(self, token, parent=None):
        self.token = token
        time_stamp = datetime.datetime.now()
        self.created_at = time_stamp
        self.last_modified_at = time_stamp
        self.parent = parent

    def update_time_stamp(self):
        self.last_modified_at = datetime.datetime.now()


class FileNode(Entity):
    def __init__(self, token, memory_manager, file_manager, parent=None):
        Entity.__init__(self, token, parent)
        self.size = 0  # in bytes
        self.mode = None
        self.chunks = []
        self.content = ""
        self.memory_manager = memory_manager
        self.file_manager = file_manager
        self.readers = 0
        self.mutex = threading.Semaphore()
        self.wrt = threading.Semaphore()

    def request_read(self):
        self.mutex.acquire()
        self.readers = self.readers + 1

        # if atleast one reader in critical section no writer can enter (preference to readers)
        if self.readers == 1:
            self.wrt.acquire()
            self.mode = "r"

        self.mutex.release()  # other readers can enter

    def release_read(self):
        self.mutex.acquire()  # reader wants to leave
        self.readers = self.readers - 1

        if self.readers == 0:
            self.mode = None
            self.wrt.release()
            # writers can enter if no readers left in critical section

        self.mutex.release()  # reader leaves

    def request_write(self):
        self.wrt.acquire()
        self.mode = "w"

    def release_write(self):
        self.mode = None
        self.wrt.release()

    def open(self, mode):
        if mode == "r":
            self.request_read()
        elif mode == "w":
            self.request_write()

    def close(self):
        if self.mode == "r":
            self.release_read()
        elif self.mode == "w":
            self.release_write()

    def get_content(self):
        self.content = ""

        for chunk in self.chunks:
            self.content += self.memory_manager.get_content(chunk)

        return self.content

    def write(self, content):
        if self.mode != "w":
            raise Exception("File not enabled for writing!")

        self.content = content
        self.save()

    def write_at(self, content, offset):
        if self.mode != "w":
            raise Exception("File not enabled for writing!")

        if offset > self.size:
            raise Exception("Invalid offset!")

        txt = self.get_content()
        self.content = txt[:offset] + content + txt[offset:]
        self.save()

    def append(self, content):
        if self.mode != "w":
            raise Exception("File not enabled for writing!")

        self.content += content
        self.save()

    def read(self, offset=0, size=None):
        if size == None or size <= 0:
            size = self.size

        if self.mode == None:
            raise Exception("File not open!")

        return self.get_content()[offset : min(offset + size, self.size)]

    def move_content(self, source_index, size, destination_index):
        if self.mode == "w":
            txt = self.get_content()

            if source_index + size > len(txt):
                raise Exception("Invalid source index!")

            if destination_index + size > len(txt):
                raise Exception("Invalid destination index!")

            if source_index > destination_index:
                source_index, destination_index = (destination_index, destination_index)

            self.content = (
                txt[:source_index]
                + txt[destination_index : destination_index + size]
                + txt[source_index:destination_index]
                + txt[destination_index + size :]
            )

            self.save()

        else:
            raise Exception("File not enabled for writing!")

    def truncate(self, max_size):
        if self.mode == "w":
            self.request_write()
            self.content = self.get_content()[:max_size]
            self.save()
        else:
            raise Exception("File not enabled for writing!")

    def save(self):
        self.size = len(self.content)
        self.memory_manager.deallocate(self.chunks)
        self.chunks = self.memory_manager.allocate(self.size)
        self.last_modified_at = datetime.datetime.now()
        self.memory_manager.write_content(self.chunks, self.content)
        self.file_manager.save()

    def __str__(self):
        return f"name: {self.token} | type: file | created_at: {self.created_at} | last_modified_at: {self.last_modified_at}"

    def get_JSON(self):
        return {
            "created_at": self.created_at.__str__(),
            "last_modified_at": self.last_modified_at.__str__(),
            "type": "file",
            "size": self.size,
            "chunks": [chunk.get_JSON() for chunk in self.chunks],
        }


class DirectoryNode(Entity):
    def __init__(self, token):
        Entity.__init__(self, token)
        self.children = {}

    def __str__(self):
        return f"name: {self.token} | type: folder | created_at: {self.created_at} | last_modified_at: {self.last_modified_at}"

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
