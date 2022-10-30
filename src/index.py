from FileManager import FileManager

manager = FileManager()
test = manager.open("test.txt", "w")
print("Before Truncate: ", test.read())
test.truncate(5)
print("After Truncate: ", test.read())
