from Nodes import DirectoryNode
from User import User

# Make a validate arguments function
def parse_arguments(args, expected_args):
    new_args = []

    if len(args) != len(expected_args):
        raise Exception("Invalid Arguments")

    for i in range(len(args)):
        if expected_args[i] == "int":
            new_args.append(int(args[i]))
        elif expected_args[i] == "str":
            new_args.append(str(args[i]))
        else:
            raise Exception("Invalid Arguments")

    return new_args


def show_format():
    return """
        create <fname> 
        delete <fname>
        mkDir <dirName>
        chDir <dirName>
        move <source_fname, target_fname>
        open <fName,mode>
        close<Fname>
        write_to_file <filename>, text
        write_to_file <filename>,text, startLocation
        read_from_file <filename,start,size
        fileObj.Truncate_file maxSize
        show_memory_map
    """


def parse_command(command):
    # split on spaces and commas
    command = command.replace(",", " ")
    command = command.split(" ")
    # remove empty strings
    command = list(filter(lambda x: x != "", command))
    # return the command and the arguments
    return (command[0], command[1:])


def get_file(file_manager, name):
    file = file_manager.find(name)

    if not file or isinstance(file, DirectoryNode):
        raise Exception("Invalid file path!")

    return file


def execute_command(command, file_manager, user: User):
    command, args = parse_command(command)

    try:
        if len(args) == 0:
            if command == "show_memory_map":
                return file_manager.memory_map()
            elif command == "--help":
                return show_format()
            elif command == "format":
                file_manager.format()
                return "Memory Formatted"
            else:
                raise Exception("Invalid Command")
        elif len(args) == 1:
            if command == "create":
                file_manager.create_file(args[0])
                return "File Created!"
            elif command == "delete":
                file_manager.delete(args[0])
                return "File Deleted"
            elif command == "mkDir":
                file_manager.mkdir(args[0])
                return "Directory created"
            elif command == "chDir":
                file_manager.chDir(args[0])
                return "CWD is now: " + args[0]
            elif command == "close":
                file = user.find_opened_file(args[0])
                if file:
                    file_manager.close(args[0])
                    user.close_file(args[0])
                return "File Closed!"
            elif command == "read_from_file":
                file = get_file(file_manager, args[0])
                return file.read()
            else:
                raise Exception("Invalid Command")
        elif len(args) == 2:
            if command == "open":
                if args[1] != "r" and args[1] != "w":
                    raise Exception("Invalid Mode")

                file = user.find_opened_file(args[0])

                if not file:
                    file = file_manager.open(args[0], args[1])
                    user.open_file(file, args[1])

                return "File Opened!"
            elif command == "move":
                file_manager.move(args[0], args[1])
                return "File Moved!"
            elif command == "write_to_file":
                file = get_file(file_manager, args[0])
                file.write(args[1])
                return "Content written!"
            elif command == "read_from_file":
                file = get_file(file_manager, args[0])
                args = parse_arguments(args, ["str", "int"])
                return file.read(args[1])
            elif command == "truncate":
                args = parse_arguments(args, ["str", "int"])
                file = get_file(file_manager, args[0])
                file.truncate(args[1])
                return "File truncated!"
            else:
                raise Exception("Invalid Command")
        elif len(args) == 3:
            if command == "read_from_file":
                args = parse_arguments(args, ["str", "str", "int"])
                file = get_file(file_manager, args[0])
                return file.read(args[1], args[2])
            if command == "write_to_file":
                args = parse_arguments(args, ["str", "str", "int"])
                file = get_file(file_manager, args[0])
                file.write_at(args[1], args[2])
                return "Content written!"
        else:
            raise Exception("Invalid Command")
    except Exception as e:
        return f"Error: {e}. Try --help to view format"


def exec_file(file_manager, thread_num):
    input = open("./test/input_" + str(thread_num) + ".txt", "r")
    output = open("./test/out_thread_" + str(thread_num) + ".txt", "a")
    output.truncate(0)

    for line in input:
        res = execute_command(line.strip(), file_manager)
        output.write(res + "\n")
