from file_manager import FileManager, File
from memory_manager import MemoryManager


manager = FileManager()
# manager.close("./subaru/../subaru/../natsuki")
ok = manager.open("~/subaru/sule/ok", "w")
ok.write_to_file("Hello")

# # manager.create("sayori")
# mem_manager = MemoryManager()
# mem_manager.format_drive()
# mem_manager.allocate(500)
# mem_manager.allocate(500)
# mem_manager.allocate(500)
