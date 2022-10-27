import datetime
import json


class Memory:
    def __init__(self, block_num, offset, limit):
        self.block_num = block_num
        self.offset = offset
        self.limit = limit

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)


class MemoryManager:
    def __init__(self):
        map = json.load(open(file="drive.json", mode="r"))
        self.num_blocks = map["num_blocks"]
        self.block_size = map["block_size"]
        self.blocks = map["blocks"]

    def allocate(self, size):
        memory = []
        remaining_size = size

        for block_num, block in self.blocks.items():
            if block["is_full"]:
                continue
            else:
                for chunk in block["free_chunks"]:
                    free_space = chunk["limit"] - chunk["offset"]

                    if free_space > remaining_size:
                        memory.append(
                            Memory(
                                block_num=block_num,
                                offset=chunk["offset"],
                                limit=chunk["offset"] + remaining_size,
                            )
                        )

                        if remaining_size < free_space:
                            chunk["offset"] += remaining_size

                        remaining_size = 0
                    else:
                        memory.append(
                            Memory(
                                block_num=block_num,
                                offset=chunk["offset"],
                                limit=chunk["limit"],
                            )
                        )

                        block["free_chunks"].remove(chunk)
                        block["is_full"] = True
                        remaining_size -= free_space

                    if remaining_size == 0:
                        self.save_to_drive()
                        return memory

        raise Exception("Not enough space!")

    def deallocate(self, memory):
        for chunk in memory:
            block = self.blocks[chunk.block_num]
            block["free_chunks"].append(
                {
                    "offset": chunk.offset,
                    "limit": chunk.limit,
                }
            )
            block["is_full"] = False

        self.save_to_drive()

    def format_drive(self):
        self.blocks = {}

        for num_block in range(1, self.num_blocks + 1):
            self.blocks[num_block] = {
                "content": "",
                "is_full": False,
                "free_chunks": [
                    {
                        "offset": 0,
                        "limit": self.block_size,
                    }
                ],
            }

        self.save_to_drive()

    def save_to_drive(self):
        mem_map = {
            "block_size": self.block_size,
            "num_blocks": self.num_blocks,
            "blocks": self.blocks,
        }

        drive = open("drive.json", "w")
        drive.write(json.dumps(mem_map, indent=2))

    def get_content(self, memory_chunk):
        return self.blocks[memory_chunk.block_num]["content"][
            memory_chunk.offset : memory_chunk.limit
        ]

    def write_content(self, memory_chunk, content):
        original_content = self.blocks[memory_chunk.block_num]["content"]
        self.blocks[memory_chunk.block_num]["content"] = (
            original_content[:memory_chunk.offset]
            + content
            + original_content[memory_chunk.limit:]
        )
        self.save_to_drive()
