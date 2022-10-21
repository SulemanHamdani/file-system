import datetime

class Entity:
    def __init__(self, name):
        self.name = name
        time_stamp = datetime.datetime.now()
        self.created_at = time_stamp
        self.last_modified_at = time_stamp

    def update_time_stamp(self):
        self.last_modified_at = datetime.datetime.now()

class File(Entity):
    def __init__(self, name, location, size = 0):
        Entity.__init__(self, name)
        self.size = size # in bytes
        self.location = location

    def __str__(self):
        return f"{self.name}: size: {self.size}"

    def rename_file(self, name, new_name):
        file = self.find_file(name)

        if file: 
            file.name = new_name
            return

    def move_file(self, name, new_location):
        file = self.find_file(name)

        if file:
            file.location = new_location
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

class Folder(Entity):
    def __init__(self, name, children = []):
        Entity.__init__(self, name)
        self.children = children

    def __str__(self):
        file_count = len(list(filter(lambda child: isinstance(child, File), self.children)))
        folder_count = len(list(filter(lambda child: isinstance(child, Folder), self.children)))
        return f"{self.name}: {file_count} files and {folder_count} folders" ""

    def add(self, entity: Entity):
        if self.find(entity.name):
            raise Exception("Entity already exists!")

        if (entity != self):
            self.children.append(entity)
    
            
    
    def remove(self, file_name):
        child = self.find(file_name)

        if child: 
            self.remove(child)
            return

        raise Exception("File not found!")

    def get_size(self):
        size = 0
        for child in self.children:
            size += child.get_size()
        return size

    def ls(self):
        for child in self.children:
            print(child)

    def find(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None
