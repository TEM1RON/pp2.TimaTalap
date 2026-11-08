CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    IN p_names VARCHAR[], 
    IN p_phones VARCHAR[], 
    OUT invalid_count INT
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    v_name VARCHAR;
    v_phone VARCHAR;
BEGIN
    invalid_count := 0;
    
    FOR i IN 1 .. array_length(p_names, 1) LOOP
        v_name := p_names[i];
        v_phone := p_phones[i];
        
        IF v_phone ~ '^\+?[0-9\-\(\)\s]{7,15}$' THEN
            CALL upsert_contact(v_name, v_phone);
        ELSE
            invalid_count := invalid_count + 1;
            RAISE NOTICE 'Invalid phone for contact %: %', v_name, v_phone;
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE name = p_identifier OR phone = p_identifier;
END;
$$;