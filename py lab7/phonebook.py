from connect import connect
import csv

def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20) UNIQUE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created")


def insert_from_console():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV inserted")


def get_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def search_by_name(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts WHERE name ILIKE %s", (f"%{name}%",))
    print(cur.fetchall())

    cur.close()
    conn.close()


def search_by_phone(prefix):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts WHERE phone LIKE %s", (f"{prefix}%",))
    print(cur.fetchall())

    cur.close()
    conn.close()


def update_contact(old_name, new_name=None, new_phone=None):
    conn = connect()
    cur = conn.cursor()

    if new_name:
        cur.execute(
            "UPDATE contacts SET name=%s WHERE name=%s",
            (new_name, old_name)
        )

    if new_phone:
        cur.execute(
            "UPDATE contacts SET phone=%s WHERE name=%s",
            (new_phone, old_name)
        )

    conn.commit()
    cur.close()
    conn.close()


def delete_contact(value):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE name=%s OR phone=%s",
        (value, value)
    )

    conn.commit()
    cur.close()
    conn.close()


def menu():
    create_table()

    while True:
        print("""
1. Insert console
2. Insert CSV
3. Show all
4. Search name
5. Search phone
6. Update
7. Delete
0. Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            get_all()
        elif choice == "4":
            search_by_name(input("Name: "))
        elif choice == "5":
            search_by_phone(input("Prefix: "))
        elif choice == "6":
            update_contact(
                input("Old name: "),
                input("New name: ") or None,
                input("New phone: ") or None
            )
        elif choice == "7":
            delete_contact(input("Value: "))
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()