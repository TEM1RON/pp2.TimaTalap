-- Procedure 1: Add another phone number

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type. Use home, work or mobile.';
    END IF;

    SELECT id
    INTO v_contact_id
    FROM contacts
    WHERE LOWER(name) = LOWER(p_contact_name)
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found.';
    END IF;

    INSERT INTO phones (contact_id, phone, phone_type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


-- Procedure 2: Move contact to a group

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
BEGIN
    SELECT id
    INTO v_contact_id
    FROM contacts
    WHERE LOWER(name) = LOWER(p_contact_name)
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found.';
    END IF;

    INSERT INTO groups (group_name)
    VALUES (p_group_name)
    ON CONFLICT (group_name)
    DO UPDATE SET group_name = EXCLUDED.group_name
    RETURNING id INTO v_group_id;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;
END;
$$;


-- Function: Search contacts by name, email or phone

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id INTEGER,
    name TEXT,
    email TEXT,
    birthday DATE,
    group_name TEXT,
    phones TEXT
)
LANGUAGE SQL
AS $$
    SELECT
        c.id,
        c.name::TEXT,
        c.email::TEXT,
        c.birthday,
        g.group_name::TEXT,
        STRING_AGG(DISTINCT p.phone, ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE
        c.name ILIKE '%' || p_query || '%'
        OR COALESCE(c.email, '') ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.name, c.email, c.birthday, g.group_name;
$$;