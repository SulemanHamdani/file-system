from lib import Manager

manager = Manager()
manager.mkdir("subaru")
manager.create("natsuki")
manager.create("yuri")
manager.open("./subaru/../subaru/../natsuki", "w")
manager.open("./subaru/../subaru/../yuri", "w")
print(manager.open_files)
manager.close("./subaru/../subaru/../natsuki")
print(manager.open_files)
manager.chDir("~")

# print(manager.cwd)
# manager.mkdir("subaru")
# print(manager.cwd)
# manager.chDir("subaru")
# print(manager.cwd)
# manager.create("natsuki")
# manager.create("yuri")

