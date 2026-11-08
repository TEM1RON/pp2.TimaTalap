from connect import get_connection

def main():
    conn = get_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    while True:
        print("\n================== PHONEBOOK MENU ==================")
        print("1. Search contacts by pattern (name or phone)")
        print("2. Add or Update contact (Upsert)")
        print("3. Bulk insert contacts with validation")
        print("4. View contacts (Pagination)")
        print("5. Delete contact")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ").strip()

        if choice == '1':
            pattern = input("Enter search query (name or part of phone): ").strip()
            try:
                cursor.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
                rows = cursor.fetchall()
                print("\n--- Search Results ---")
                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No contacts found.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '2':
            name = input("Enter contact name: ").strip()
            phone = input("Enter phone number: ").strip()
            try:
                cursor.execute("CALL upsert_contact(%s, %s);", (name, phone))
                print(f"Contact '{name}' successfully added or updated!")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '3':
            print("Enter multiple contacts separated by comma.")
            raw_names = input("Names (e.g. Alice, Bob): ").strip()
            raw_phones = input("Phones (e.g. +77011112233, 87023334455): ").strip()
            
            names = [n.strip() for n in raw_names.split(',') if n.strip()]
            phones = [p.strip() for p in raw_phones.split(',') if p.strip()]
            
            if len(names) != len(phones):
                print("Error: The number of names and phones must match!")
                continue

            try:
                cursor.execute("CALL bulk_insert_contacts(%s, %s, 0);", (names, phones))
                print("Bulk insert process completed. Check console/notices for invalid numbers.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '4':
            try:
                limit = int(input("Enter limit (how many records to show): ").strip())
                offset = int(input("Enter offset (how many records to skip): ").strip())
                cursor.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
                rows = cursor.fetchall()
                print("\n--- Paginated Contacts ---")
                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No records in this range.")
            except ValueError:
                print("Error: Please enter valid numbers for limit and offset.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '5':
            identifier = input("Enter name or phone of the contact to delete: ").strip()
            try:
                cursor.execute("CALL delete_contact(%s);", (identifier,))
                print(f"Deletion procedure executed for '{identifier}'.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '6':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please select a number from 1 to 6.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()