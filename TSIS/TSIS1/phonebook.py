import json
from connect import get_connection


def add_contact(conn, name, email, birthday):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO contacts(name, email, birthday)
        VALUES (%s, %s, %s)
    """, (name, email, birthday))
    conn.commit()


def filter_by_group(conn, group_name):
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group_name,))
    return cur.fetchall()


def search_by_email(conn, email_part):
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM contacts
        WHERE email ILIKE %s
    """, (f"%{email_part}%",))
    return cur.fetchall()


def get_sorted_contacts(conn, sort_by):
    cur = conn.cursor()
    allowed = ["name", "birthday", "id"]
    if sort_by not in allowed:
        sort_by = "name"

    cur.execute(f"""
        SELECT * FROM contacts
        ORDER BY {sort_by}
    """)
    return cur.fetchall()


def paginate(conn, limit=5):
    cur = conn.cursor()
    offset = 0

    while True:
        cur.execute("""
            SELECT * FROM contacts
            ORDER BY id
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()
        print("\n--- PAGE ---")
        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev" and offset > 0:
            offset -= limit
        else:
            break


def export_json(conn, filename="contacts.json"):
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)
    contacts = cur.fetchall()

    result = []

    for c in contacts:
        cur.execute("""
            SELECT phone, type FROM phones WHERE contact_id=%s
        """, (c[0],))
        phones = cur.fetchall()

        result.append({
            "id": c[0],
            "name": c[1],
            "email": c[2],
            "birthday": str(c[3]) if c[3] else None,
            "group": c[4],
            "phones": [{"phone": p[0], "type": p[1]} for p in phones]
        })

    with open(filename, "w") as f:
        json.dump(result, f, indent=4)


def import_json(conn, filename="contacts.json"):
    cur = conn.cursor()

    with open(filename, "r") as f:
        data = json.load(f)

    for c in data:
        cur.execute("SELECT id FROM contacts WHERE name=%s", (c["name"],))
        exists = cur.fetchone()

        if exists:
            action = input(f"{c['name']} exists (skip/overwrite): ")
            if action == "skip":
                continue

            cur.execute("DELETE FROM contacts WHERE name=%s", (c["name"],))

        cur.execute("""
            INSERT INTO contacts(name, email, birthday)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (c["name"], c["email"], c["birthday"]))

        contact_id = cur.fetchone()[0]

        for p in c["phones"]:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, p["phone"], p["type"]))

    conn.commit()


def main():
    conn = get_connection()

    while True:
        print("""
1. Add contact
2. Filter by group
3. Search email
4. Sorted list
5. Pagination
6. Export JSON
7. Import JSON
0. Exit
        """)

        choice = input("Choose: ")

        if choice == "1":
            add_contact(conn,
                        input("name: "),
                        input("email: "),
                        input("birthday YYYY-MM-DD: "))

        elif choice == "2":
            print(filter_by_group(conn, input("group: ")))

        elif choice == "3":
            print(search_by_email(conn, input("email part: ")))

        elif choice == "4":
            print(get_sorted_contacts(conn, input("sort by: ")))

        elif choice == "5":
            paginate(conn)

        elif choice == "6":
            export_json(conn)

        elif choice == "7":
            import_json(conn)

        elif choice == "0":
            break


if __name__ == "__main__":
    main()