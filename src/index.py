from FileManager import FileManager


manager = FileManager()
natsuki = manager.open("~/natsuki", "w")

print(natsuki.read())
