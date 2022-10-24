from lib import Manager

manager = Manager()
manager.mkdir("subaru")
manager.create("natsuki")
manager.create("yuri")
manager.ls()
print(manager.find("./subaru/../subaru/../natsuki"))
