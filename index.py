from file_manager import FileManager, File
from memory_manager import MemoryManager


manager = FileManager()
print(manager.cwd)
manager.mkdir("subaru")
manager.create("natsuki")
manager.create("yuri")
# manager.open("./subaru/../subaru/../natsuki", "w")
# manager.open("./subaru/../subaru/../yuri", "w")
# manager.ls()
print(manager.cwd)
# manager.close("./subaru/../subaru/../natsuki")
manager.chDir("subaru")
manager.mkdir("sule")
manager.chDir("~")
manager.chDir("~/subaru/sule")
manager.create("ok")
ok = manager.open("~/subaru/sule/ok", "w")
ok.write_to_file("Hello")

# # manager.create("sayori")
manager.dump_JSON()

# mem_manager = MemoryManager()
# mem_manager.format_drive()
# mem_manager.allocate(500)
# mem_manager.allocate(500)
# mem_manager.allocate(500)