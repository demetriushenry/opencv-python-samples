import sys


def get_value(position):
    list = [11]
    for x in range(position):
        list.append(list[-1] + 7)
    print(list)
    print(list[position - 1])


if __name__ == "__main__":
    sys.exit(get_value(253))
