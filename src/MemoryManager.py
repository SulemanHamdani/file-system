import datetime
import json


class Memory:
    def __init__(self, block_num, offset, limit):
        self.block_num = block_num
        self.offset = offset
        self.limit = limit

    def get_JSON(self):
        return {
            "block_num": self.block_num,
            "offset": self.offset,
            "limit": self.limit,
        }


class MemoryManager:
    def __init__(self):
        file = open(file="drive.json", mode="r")
        drive = json.load(file)
        file.close()

        self.num_blocks = drive["num_blocks"]
        self.block_size = drive["block_size"]
        self.blocks = drive["blocks"]

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

        self.deallocate(memory)
        raise Exception("Not enough space!")

    def deallocate(self, memory):
        for chunk in memory:
            block = self.blocks[str(chunk.block_num)]
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
            self.blocks[str(num_block)] = {
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
        mem_drive = {
            "block_size": self.block_size,
            "num_blocks": self.num_blocks,
            "blocks": self.blocks,
        }

        drive = open(file="drive.json", mode="w")
        drive.write(json.dumps(mem_drive, indent=2))
        drive.close()

    def get_content(self, memory_chunk):
        return self.blocks[str(memory_chunk.block_num)]["content"][
            memory_chunk.offset : memory_chunk.limit
        ]

    def write_content(self, memory_chunks, content):
        start = 0

        for chunk in memory_chunks:
            chunk_size = chunk.limit - chunk.offset

            original_content = self.blocks[chunk.block_num]["content"]

            self.blocks[chunk.block_num]["content"] = (
                original_content[: chunk.offset]
                + content[start : start + chunk_size]
                + original_content[chunk.limit :]
            )
            start += chunk_size

        self.save_to_drive()
