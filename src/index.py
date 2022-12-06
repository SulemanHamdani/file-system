from FileManager import FileManager
from Nodes import DirectoryNode

def load_menu():
    # print the menu
    print("1. Create a new file")
    print("2. Open a file with a mode")
    print("3. Close a file")
    print("4. Delete a file")
    print("5. Write to a file")
    print("6. Write to a file at")
    print("7. Read a file or read from a specific index")
    print("8. Move contents of a file within the file")
    print("9. Truncate the size of a file")
    print("10. Make a directory")
    print("11. Delete a directory")
    print("12. Change directory")
    print("13. List the children of the CWD")
    print("14. Display the memory map")
    print("15. Format drive")
    print("16. Exit")


# create a file manager object
file_manager = FileManager()

# create a loop to keep the program running
while True:
    try:
        load_menu()
        # get the user's input
        user_input = input("Enter a command: ")

        # check if the user wants to exit
        if user_input == "16":
            # exit the program
            break

        # check if the user wants to create a new file
        elif user_input == "1":
            # get the file name
            file_name = input("Enter the file name: ")
            # create the file
            file_manager.create_file(file_name)
        
        elif user_input == "2": #open a file
            # get the file name
            file_path = input("Enter File path: ")
            mode = input("Enter the mode: ")
            file = file_manager.find(file_path)

            if not file or isinstance(file, DirectoryNode):
                raise Exception("Invalid File Name")

            file.mode = mode

        elif user_input == "3": #close a file
            # get the file name
            file_path = input("Enter File path: ")
            file = file_manager.close(file_path)

        # Delete File
        elif user_input == "4":
            # get the file name
            file_path = input("Enter File path: ")
            file = file_manager.delete(file_path)

        elif user_input == "5": #wtite to a file
            # get the file name
            file_path = input("Enter File path: ")
            file = file_manager.find(file_path)

            if not file or isinstance(file, DirectoryNode):
                raise Exception("Invalid File Name")

            if file.mode == None:
                raise Exception("File not open! please open the file first")
            
            if file.mode == 'r':
                raise Exception("File not enabled for writing!")
            
            else:
                content = input("Enter the content: ")
                file.write(content)

        elif user_input == "6": # write to a file_at
            # get the file name
            file_path = input("Enter File path: ")
            file = file_manager.find(file_path)
            if file.mode == None:
                raise Exception("File not open! please open the file first")
            else:
                index = int(input("Enter the index: "))
                content = input("Enter the content: ")
                file.write_at(content, index)

        elif user_input == "7": #read a file or read from a specific index
            file_path = input("Enter File path: ")
            file = file_manager.find(file_path)
            if file.mode == None:
                raise Exception("File not open! please open the file first")
            else:
                index = int(input("Enter the index: "))
                size = int(input("Enter length: "))
                print(file.read(index, size))

        elif user_input == "8": #move contents of a file within the file
            # get the file name
            file_path = input("Enter File path: ")
            file = file_manager.find(file_path)
            if file.mode == None:
                raise Exception("File not open! please open the file first")
            
            elif file.mode == 'r':
                raise Exception("File not open for writing! please open the file for writing first")

            else:
                source_index = int(input("Enter the index: "))
                destination_index = int(input("Enter the destination index: "))
                size = int(input("Enter the size: "))
                file.move_content(source_index, size, destination_index)

        elif user_input == "9": #truncate the size of a file
            # get the file name
            file_path = input("Enter File path: ")
            file = file_manager.find(file_path)

            if not file or isinstance(file, DirectoryNode):
                raise Exception("Invalid File Name")

            if file.mode == None:
                raise Exception("File not open! please open the file first")
            
            if file.mode == 'r':
                raise Exception("File not open for writing! please open the file for writing first")
            
            max_size = int(input("Enter the max size: "))
            
            if (max_size < 0):
                raise Exception("Invalid size! (size must be greater than 0)")

            file.truncate(max_size)
        
        elif user_input == "10": #make a directory
            # get the directory name
            directory_name = input("Enter the directory name: ")
            file_manager.mkdir(directory_name)
        
        elif user_input == "11": #delete a directory
            # get the directory name
            directory_path = input("Enter the directory path: ")
            file_manager.delete(directory_path)
        
        elif user_input == "12": #change directory
            # get the directory name
            directory_path = input("Enter the directory path: ")
            file_manager.chDir(directory_path)
        
        elif user_input == "13":
            file_manager.ls()

        elif user_input == "14": #display the memory map
            file_manager.memory_map()
            
        elif user_input == "15":
            file_manager.format()

        else:
            print("Invalid command")

    except Exception as e:
        print(e)
