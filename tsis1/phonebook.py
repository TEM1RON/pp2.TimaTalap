
import json
import csv
from connect import connect


def add_contact():
    conn = connect()
    cur = conn.cursor()

    name = input("Contact name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group (Family/Work/Friend/Other): ")
    phone_type = input("Phone type (home/work/mobile): ")

    cur.execute("""
        INSERT INTO contacts (name, phone, email, birthday)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (name, phone, email or None, birthday or None))

    contact_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO phones (contact_id, phone, phone_type)
        VALUES (%s, %s, %s)
    """, (contact_id, phone, phone_type))

    if group:
        cur.execute("""
            INSERT INTO groups (group_name)
            VALUES (%s)
            ON CONFLICT (group_name) DO NOTHING
        """, (group,))

        cur.execute(
            "SELECT id FROM groups WHERE group_name = %s",
            (group,)
        )

        group_id = cur.fetchone()[0]

        cur.execute(
            "UPDATE contacts SET group_id = %s WHERE id = %s",
            (group_id, contact_id)
        )

    conn.commit()
    print("Contact added successfully!")

    cur.close()
    conn.close()


def advanced_search():
    conn = connect()
    cur = conn.cursor()

    query = input("Enter name, email or phone: ")

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def add_new_phone():
    conn = connect()
    cur = conn.cursor()

    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Phone type (home/work/mobile): ")

    cur.execute(
        "CALL add_phone(%s, %s, %s)",
        (name, phone, phone_type)
    )

    conn.commit()
    print("Phone added successfully!")

    cur.close()
    conn.close()


def assign_group():
    conn = connect()
    cur = conn.cursor()

    name = input("Contact name: ")
    group = input("Group name: ")

    cur.execute(
        "CALL move_to_group(%s, %s)",
        (name, group)
    )

    conn.commit()
    print("Group assigned successfully!")

    cur.close()
    conn.close()


def filter_by_group():
    conn = connect()
    cur = conn.cursor()

    group = input("Enter group name: ")

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE LOWER(g.group_name) = LOWER(%s)
    """, (group,))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def sort_contacts():
    conn = connect()
    cur = conn.cursor()

    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by creation date")

    choice = input("Choose: ")

    if choice == "1":
        order = "name"
    elif choice == "2":
        order = "birthday"
    elif choice == "3":
        order = "created_at"
    else:
        print("Invalid choice")
        cur.close()
        conn.close()
        return

    cur.execute(
        "SELECT id, name, email, birthday FROM contacts ORDER BY " + order
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def pagination():
    conn = connect()
    cur = conn.cursor()

    limit = 5
    offset = 0

    while True:
        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s)",
            (limit, offset)
        )

        rows = cur.fetchall()

        print("\nContacts:")

        for row in rows:
            print(row)

        print("\n1. Next page")
        print("2. Previous page")
        print("3. Exit")

        choice = input("Choose: ")

        if choice == "1" and len(rows) == limit:
            offset += limit
        elif choice == "2" and offset >= limit:
            offset -= limit
        elif choice == "3":
            break

    cur.close()
    conn.close()


def export_to_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.phone, c.email, c.birthday,
               g.group_name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)

    contacts = cur.fetchall()
    result = []

    for contact in contacts:
        cur.execute("""
            SELECT phone, phone_type
            FROM phones
            WHERE contact_id = %s
        """, (contact[0],))

        phones = cur.fetchall()

        result.append({
            "id": contact[0],
            "name": contact[1],
            "phone": contact[2],
            "email": contact[3],
            "birthday": str(contact[4]) if contact[4] else None,
            "group": contact[5],
            "phones": [
                {"phone": p[0], "type": p[1]}
                for p in phones
            ]
        })

    with open("contacts.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print("Contacts exported successfully!")

    cur.close()
    conn.close()


def import_from_json():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.json", "r", encoding="utf-8") as file:
        contacts = json.load(file)

    for contact in contacts:
        cur.execute(
            "SELECT id FROM contacts WHERE LOWER(name) = LOWER(%s)",
            (contact["name"],)
        )

        existing = cur.fetchone()

        if existing:
            answer = input(
                contact["name"] + " already exists. Overwrite? (y/n): "
            )

            if answer.lower() == "n":
                continue

            contact_id = existing[0]

            cur.execute("""
                UPDATE contacts
                SET email = %s, birthday = %s
                WHERE id = %s
            """, (
                contact.get("email"),
                contact.get("birthday"),
                contact_id
            ))

        else:
            if not contact.get("phone"):
                print("Skipping contact without phone:", contact["name"])
                continue

            cur.execute("""
                INSERT INTO contacts (name, phone, email, birthday)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (
                contact["name"],
                contact["phone"],
                contact.get("email"),
                contact.get("birthday")
            ))

            contact_id = cur.fetchone()[0]

        group = contact.get("group")

        if group:
            cur.execute("""
                INSERT INTO groups (group_name)
                VALUES (%s)
                ON CONFLICT (group_name) DO NOTHING
            """, (group,))

            cur.execute(
                "SELECT id FROM groups WHERE group_name = %s",
                (group,)
            )

            group_id = cur.fetchone()[0]

            cur.execute(
                "UPDATE contacts SET group_id = %s WHERE id = %s",
                (group_id, contact_id)
            )

        for phone in contact.get("phones", []):
            cur.execute("""
                INSERT INTO phones (contact_id, phone, phone_type)
                VALUES (%s, %s, %s)
                ON CONFLICT (phone) DO NOTHING
            """, (
                contact_id,
                phone["phone"],
                phone["type"]
            ))

    conn.commit()
    print("Contacts imported successfully!")

    cur.close()
    conn.close()


def import_from_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cur.execute("""
                INSERT INTO contacts (name, phone, email, birthday)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (phone) DO UPDATE
                SET email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday
                RETURNING id
            """, (
                row["name"],
                row["phone"],
                row.get("email") or None,
                row.get("birthday") or None
            ))

            contact_id = cur.fetchone()[0]

            phone_type = row.get("phone_type") or "mobile"

            cur.execute("""
                INSERT INTO phones (contact_id, phone, phone_type)
                VALUES (%s, %s, %s)
                ON CONFLICT (phone) DO NOTHING
            """, (contact_id, row["phone"], phone_type))

            group = row.get("group")

            if group:
                cur.execute("""
                    INSERT INTO groups (group_name)
                    VALUES (%s)
                    ON CONFLICT (group_name) DO NOTHING
                """, (group,))

                cur.execute(
                    "SELECT id FROM groups WHERE group_name = %s",
                    (group,)
                )

                group_id = cur.fetchone()[0]

                cur.execute(
                    "UPDATE contacts SET group_id = %s WHERE id = %s",
                    (group_id, contact_id)
                )

    conn.commit()
    print("CSV imported successfully!")

    cur.close()
    conn.close()


def main():
    while True:
        print("\n========== PHONEBOOK ==========")
        print("1. Add new contact")
        print("2. Search contacts")
        print("3. Add new phone")
        print("4. Move contact to group")
        print("5. Filter by group")
        print("6. Sort contacts")
        print("7. Show contacts (pagination)")
        print("8. Export to JSON")
        print("9. Import from JSON")
        print("10. Import from CSV")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            advanced_search()
        elif choice == "3":
            add_new_phone()
        elif choice == "4":
            assign_group()
        elif choice == "5":
            filter_by_group()
        elif choice == "6":
            sort_contacts()
        elif choice == "7":
            pagination()
        elif choice == "8":
            export_to_json()
        elif choice == "9":
            import_from_json()
        elif choice == "10":
            import_from_csv()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
