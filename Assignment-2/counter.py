import os
import server_info

COUNTER_FILE_PATH = "counter.txt"

def get_next_id():
    if not os.path.exists(COUNTER_FILE_PATH):
        with open(COUNTER_FILE_PATH, "w") as counter_file:
            counter_file.write("1")

    with open(COUNTER_FILE_PATH, "r") as counter_file:
        counter_value = int(counter_file.read().strip())

    next_id = counter_value + 1

    with open(COUNTER_FILE_PATH, "w") as counter_file:
        counter_file.write(str(next_id))

    return (counter_value % server_info.N)

if __name__ == "__main__":
    next_id = get_next_id()
    print("Next ID:", next_id)
