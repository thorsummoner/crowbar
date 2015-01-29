import sys
import string

printable = set(string.printable)

def process(stream):
    found_str = ""
    while True:
        data = stream.read(1024*4)
        if not data:
            break
        for char in data:
            if char in printable:
                found_str += char
            elif len(found_str) >= 4:
                yield found_str
                found_str = ""
            else:
                found_str = ""

if __name__ == "__main__":
    for found_str in process(sys.stdin):
       print found_str
