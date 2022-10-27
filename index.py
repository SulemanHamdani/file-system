from file_manager import FileManager, File


manager = FileManager()
# manager.close("./subaru/../subaru/../natsuki")
manager.create("natsumi")
natsuki = manager.open("~/natsuki", "w")
natsuki.write_to_file("Hello, world!")
natsuki.write_to_file("Hello, world! - Natuski")
natsuki.write_to_file_at("-hahah ", len("Hello, world! "))
print(natsuki.read_from_file())
print(natsuki.read_from_file_at(len("Hello, world! ")))
natsuki.truncate(len("Hello, world! "))
print(natsuki.read_from_file())

# ok.write_to_file("Hello")
# # manager.create("sayori")
# mem_manager = MemoryManager()
# mem_manager.format_drive()
# mem_manager.allocate(500)
# mem_manager.allocate(500)
# mem_manager.allocate(500)
