from FileManager import FileManager

# manager = FileManager()
# manager.format()
# manager.mkdir('sule')
# manager.chDir('~/sule')
# me_file = manager.create_file('me.png')
# me_file.write('Suleman Hamdani')
# # me_file = manager.open('~/sule/me.png', mode='w')

# manager.ls()


# make a menu for the user to choose from 

# 1. Create a new file
# 2. Read a file and read from a specific index
# 3. Write to a file and write to a specific index
# 4. Delete a file
# 5. Make a directory
# 6. Delete a directory
# 7. change directory
# 8. Open a file with a mode
# 9. Close a file
# 10. Move contents of a file within the file
# 11. Truncate the size of a file
# 12. Display the memory map
# 13. Exit

def load_menu():
    # print the menu
    print("1. Create a new file")
    print("2. Read a file or read from a specific index")
    print("3. Write to a file at")
    print("4. Write to a file")
    print("5. Delete a file")
    print("6. Make a directory")
    print("7. Delete a directory")
    print("8. change directory")
    print("9. Open a file with a mode")
    print("10. Close a file")
    print("11. Move contents of a file within the file")
    print("12. Truncate the size of a file")
    print("13. Display the memory map")
    print("14. List the children of the CWD")
    print("15. Format drive")
    print("16. Exit")




# create a file manager object
file_manager = FileManager()

# create a loop to keep the program running
while True:
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

    # check if the user wants to read a file
    elif user_input == "2":
        # get the file name
        file_name = input("Enter the file name: ")
        file = file_manager.get_file(file_name)
        if file.mode == None:
            print("File not open! please open the file first")

        else:
            index = input("Enter the index: ")
            file.read(index)
            

    elif user_input == "3": # write to a file_at
        # get the file name
        file_name = input("Enter the file name: ")
        file = file_manager.get_file(file_name)
        if file.mode == None:
            print("File not open! please open the file first")

        else:
            index = input("Enter the index: ")
            content = input("Enter the content: ")
            file.write_at(content, index)
    
    elif user_input == "4": #wtite to a file
        # get the file name
        file_name = input("Enter the file name: ")
        file = file_manager.get_file(file_name)

        if file.mode == None:
            print("File not open! please open the file first")
        
        if file.mode == 'r':
            print("File not open for writing! please open the file for writing first")
        
        else:
            content = input("Enter the content: ")
            file.write(content)
    
    elif user_input == "5": #delete a file
        # get the file name
        file_name = input("Enter the file name: ")
        file = file_manager.get_file(file_name)
        file.delete()
    
    elif user_input == "6": #make a directory
        # get the directory name
        directory_name = input("Enter the directory name: ")
        file_manager.mkdir(directory_name)
    
    elif user_input == "7": #delete a directory
        # get the directory name
        directory_name = input("Enter the directory name: ")
        dir = file_manager.get_directory(directory_name)
        dir.delete()
    
    elif user_input == "8": #change directory
        # get the directory name
        directory_name = input("Enter the directory name: ")
        file_manager.chDir(directory_name)
    
    elif user_input == "9": #open a file
        # get the file name
        file_name = input("Enter the file name: ")
        mode = input("Enter the mode: ")
        file = file_manager.get_file(file_name)
        file.open(mode)
    
    elif user_input == "10": #close a file
        # get the file name
        file_name = input("Enter the file name: ")
        file = file_manager.get_file(file_name)
        file.close()
    
    elif user_input == "11": #move contents of a file within the file
        # get the file name
        file_name = input("Enter the file name: ")
        file = file_manager.get_file(file_name)
        if file.mode == None:
            print("File not open! please open the file first")
        
        elif file.mode == 'r':
            print("File not open for writing! please open the file for writing first")

        else:
            source_index = input("Enter the index: ")
            destination_index = input("Enter the destination index: ")
            size = input("Enter the size: ")
            file.move_content(source_index, size, destination_index)
    
    elif user_input == "12": #truncate the size of a file
        # get the file name
        file_name = input("Enter the file name: ")
        file = file_manager.get_file(file_name)
        if file.mode == None:
            print("File not open! please open the file first")
        
        elif file.mode == 'r':
            print("File not open for writing! please open the file for writing first")
        
        else:
            max_size = input("Enter the max size: ")
            file.truncate(max_size)

    elif user_input == "13": #display the memory map
        file_manager.memory_map()
        
    elif user_input == "14":
        file_manager.ls()

    elif user_input == "15":
        file_manager.format()

    else:
        print("Invalid command")

    
    # Create a load menu function

# Create a load menu function




    
    
    




