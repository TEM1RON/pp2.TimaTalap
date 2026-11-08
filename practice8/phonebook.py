from connect import get_connection

def test_functions_and_procedures():
    conn = get_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        print("--- 1. Pattern Search Function Test ---")
        cursor.execute("SELECT * FROM get_contacts_by_pattern(%s);", ('Alim',))
        for row in cursor.fetchall():
            print(row)

        print("\n--- 2. Upsert Procedure Test ---")
        cursor.execute("CALL upsert_contact(%s, %s);", ('Damir', '+77011234567'))
        print("Contact successfully added/updated via Upsert.")

        print("\n--- 3. Bulk Insert Procedure Test with Validation ---")
        names = ['Aigerim', 'Erasyl', 'BadPhoneUser']
        phones = ['+77079998877', '87023334455', 'abc-not-a-phone']
        
        cursor.execute("CALL bulk_insert_contacts(%s, %s, 0);", (names, phones))
        print("Bulk insert completed.")

        print("\n--- 4. Pagination Function Test ---")
        cursor.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (5, 0))
        for row in cursor.fetchall():
            print(row)

        print("\n--- 5. Delete Procedure Test ---")
        cursor.execute("CALL delete_contact(%s);", ('BadPhoneUser',))
        print("Deletion completed.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    test_functions_and_procedures()