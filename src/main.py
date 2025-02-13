from tinydb import TinyDB, Query


def main():
    db = TinyDB("../db/db.json")

    db.insert({"code": "LEU123", "duration": 4})

    for item in db:
        print(item)


if __name__ == "__main__":
    main()
