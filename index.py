from file_manager import FileManager, File
from memory_manager import MemoryManager


manager = FileManager()
# manager.close("./subaru/../subaru/../natsuki")
manager.create("natsumi")
natsuki = manager.open("~/natsuki", "w")
natsuki.write_to_file("Hello, world!")
natsuki.write_to_file("Hello, world! - Natuski")
ok = manager.open("~/subaru/sule/ok", "w")
ok.write_to_file("Hello")
print(natsuki.get_content())
print(ok.get_content())
# # manager.create("sayori")
# mem_manager = MemoryManager()
# mem_manager.format_drive()
# mem_manager.allocate(500)
# mem_manager.allocate(500)
# mem_manager.allocate(500)
