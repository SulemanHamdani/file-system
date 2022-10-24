from lib import Manager

manager = Manager()
manager.mkdir("subaru")
manager.create("natsuki")
manager.create("yuri")
manager.open("./subaru/../subaru/../natsuki", "w")
manager.open("./subaru/../subaru/../yuri", "w")
manager.ls()
manager.close("./subaru/../subaru/../natsuki")
manager.chDir("~/subaru")
manager.create("sayori")
print(manager.cwd)
