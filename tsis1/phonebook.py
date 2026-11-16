import csv
import json

from connect import connect


# 1. Add contact

def add_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()
    email = input("Enter email: ").strip()
    birthday = input("Enter birthday (YYYY-MM-DD): ").strip()

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO contacts (name, phone, email, birthday)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (name, phone, email or None, birthday or None)
        )

        contact_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO phones (contact_id, phone, phone_type)
            VALUES (%s, %s, 'mobile')
            """,
            (contact_id, phone)
        )

        conn.commit()
        print("Contact added successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


# 2. Search contacts

def search_contacts():
    query = input("Enter name, email or phone: ")

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM search_contacts(%s)",
            (query,)
        )

        results = cur.fetchall()

        if not results:
            print("No contacts found.")

        for contact in results:
            print(contact)

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


# 3. Filter contacts by group

def filter_by_group():
    group_name = input("Enter group name: ")

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT c.id, c.name, c.phone, c.email, c.birthday
            FROM contacts c
            JOIN groups g ON c.group_id = g.id
            WHERE LOWER(g.group_name) = LOWER(%s)
            ORDER BY c.name
            """,
            (group_name,)
        )

        results = cur.fetchall()

        if not results:
            print("No contacts found in this group.")

        for contact in results:
            print(contact)

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


# 4. Sort contacts

def sort_contacts():
    print("\nSort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    choice = input("Choose: ")

    sorting = {
        "1": "name",
        "2": "birthday",
        "3": "created_at"
    }

    column = sorting.get(choice)

    if column is None:
        print("Invalid choice.")
        return

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute(
            f"""
            SELECT id, name, phone, email, birthday, created_at
            FROM contacts
            ORDER BY {column} NULLS LAST
            """
        )

        for contact in cur.fetchall():
            print(contact)

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


# 5. Pagination

def paginate_contacts():
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        limit = 5
        offset = 0

        while True:
            cur.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s)",
                (limit, offset)
            )

            contacts = cur.fetchall()

            print("\n--- CONTACTS ---")

            for contact in contacts:
                print(contact)

            print("\nN - Next page")
            print("P - Previous page")
            print("Q - Quit")

            choice = input("Choose: ").lower()

            if choice == "n":
                if len(contacts) == limit:
                    offset += limit
                else:
                    print("Last page reached.")

            elif choice == "p":
                offset = max(0, offset - limit)

            elif choice == "q":
                break

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


# 6. Add another phone

def add_phone():
    name = input("Enter contact name: ")
    phone = input("Enter phone number: ")
    phone_type = input("Enter type (home/work/mobile): ").lower()

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute(
            "CALL add_phone(%s, %s, %s)",
            (name, phone, phone_type)
        )

        conn.commit()
        print("Phone added successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


# 7. Move contact to group

def move_to_group():
    name = input("Enter contact name: ")
    group_name = input("Enter group name: ")

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute(
            "CALL move_to_group(%s, %s)",
            (name, group_name)
        )

        conn.commit()
        print("Contact moved successfully.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


# 8. Export contacts to JSON

def export_json():
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                c.id,
                c.name,
                c.email,
                c.birthday,
                g.group_name,
                p.phone,
                p.phone_type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY c.id
            """
        )

        rows = cur.fetchall()
        contacts = {}

        for row in rows:
            contact_id = row[0]

            if contact_id not in contacts:
                contacts[contact_id] = {
                    "name": row[1],
                    "email": row[2],
                    "birthday": str(row[3]) if row[3] else None,
                    "group_name": row[4],
                    "phones": []
                }

            if row[5]:
                contacts[contact_id]["phones"].append({
                    "number": row[5],
                    "type": row[6]
                })

        with open("contacts.json", "w", encoding="utf-8") as file:
            json.dump(
                list(contacts.values()),
                file,
                indent=4,
                ensure_ascii=False
            )

        print("Contacts exported successfully.")

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


# 9. Import contacts from JSON

def import_json():
    try:
        with open("contacts.json", "r", encoding="utf-8") as file:
            contacts = json.load(file)

    except FileNotFoundError:
        print("contacts.json not found.")
        return

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        for contact in contacts:
            name = contact["name"]

            cur.execute(
                """
                SELECT id FROM contacts
                WHERE LOWER(name) = LOWER(%s)
                """,
                (name,)
            )

            existing = cur.fetchone()

            if existing:
                answer = input(
                    f"{name} already exists. Overwrite? (y/n): "
                ).lower()

                if answer != "y":
                    continue

                contact_id = existing[0]

                cur.execute(
                    """
                    UPDATE contacts
                    SET email = %s, birthday = %s
                    WHERE id = %s
                    """,
                    (
                        contact.get("email"),
                        contact.get("birthday"),
                        contact_id
                    )
                )

            else:
                phones = contact.get("phones", [])
                first_phone = phones[0]["number"] if phones else ""

                cur.execute(
                    """
                    INSERT INTO contacts (name, phone, email, birthday)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        name,
                        first_phone,
                        contact.get("email"),
                        contact.get("birthday")
                    )
                )

                contact_id = cur.fetchone()[0]

            group_name = contact.get("group_name")

            if group_name:
                cur.execute(
                    """
                    INSERT INTO groups (group_name)
                    VALUES (%s)
                    ON CONFLICT (group_name)
                    DO UPDATE SET group_name = EXCLUDED.group_name
                    RETURNING id
                    """,
                    (group_name,)
                )

                group_id = cur.fetchone()[0]

                cur.execute(
                    """
                    UPDATE contacts
                    SET group_id = %s
                    WHERE id = %s
                    """,
                    (group_id, contact_id)
                )

            for phone in contact.get("phones", []):
                cur.execute(
                    """
                    INSERT INTO phones (contact_id, phone, phone_type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (phone) DO NOTHING
                    """,
                    (
                        contact_id,
                        phone["number"],
                        phone.get("type", "mobile")
                    )
                )

        conn.commit()
        print("JSON import completed.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


# 10. Import contacts from CSV

def import_csv():
    filename = input(
        "Enter CSV filename (default contacts.csv): "
    ).strip()

    if not filename:
        filename = "contacts.csv"

    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        with open(filename, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["name"].strip()
                phone = row["phone"].strip()
                email = row.get("email", "").strip() or None
                birthday = row.get("birthday", "").strip() or None
                group_name = row.get("group", "").strip()
                phone_type = row.get("phone_type", "mobile").strip().lower()

                cur.execute(
                    """
                    SELECT id FROM contacts
                    WHERE phone = %s
                    """,
                    (phone,)
                )

                existing = cur.fetchone()

                if existing:
                    contact_id = existing[0]

                    cur.execute(
                        """
                        UPDATE contacts
                        SET name = %s, email = %s, birthday = %s
                        WHERE id = %s
                        """,
                        (name, email, birthday, contact_id)
                    )

                else:
                    cur.execute(
                        """
                        INSERT INTO contacts (name, phone, email, birthday)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                        """,
                        (name, phone, email, birthday)
                    )

                    contact_id = cur.fetchone()[0]

                cur.execute(
                    """
                    INSERT INTO phones (contact_id, phone, phone_type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (phone) DO NOTHING
                    """,
                    (contact_id, phone, phone_type)
                )

                if group_name:
                    cur.execute(
                        """
                        INSERT INTO groups (group_name)
                        VALUES (%s)
                        ON CONFLICT (group_name)
                        DO UPDATE SET group_name = EXCLUDED.group_name
                        RETURNING id
                        """,
                        (group_name,)
                    )

                    group_id = cur.fetchone()[0]

                    cur.execute(
                        """
                        UPDATE contacts
                        SET group_id = %s
                        WHERE id = %s
                        """,
                        (group_id, contact_id)
                    )

        conn.commit()
        print("CSV import completed.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


# Main menu

def main():
    while True:
        print("\n========== PHONEBOOK ==========")
        print("1. Add contact")
        print("2. Search contacts")
        print("3. Filter by group")
        print("4. Sort contacts")
        print("5. Show contacts (pagination)")
        print("6. Add another phone")
        print("7. Move contact to group")
        print("8. Export contacts to JSON")
        print("9. Import contacts from JSON")
        print("10. Import contacts from CSV")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            search_contacts()
        elif choice == "3":
            filter_by_group()
        elif choice == "4":
            sort_contacts()
        elif choice == "5":
            paginate_contacts()
        elif choice == "6":
            add_phone()
        elif choice == "7":
            move_to_group()
        elif choice == "8":
            export_json()
        elif choice == "9":
            import_json()
        elif choice == "10":
            import_csv()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()