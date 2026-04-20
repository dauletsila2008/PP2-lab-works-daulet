CREATE OR REPLACE PROCEDURE upsert_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_users(p_users JSONB)
LANGUAGE plpgsql AS $$
DECLARE
    user_item JSONB;
    invalid_data JSONB := '[]'::JSONB;
BEGIN
    FOR user_item IN SELECT * FROM jsonb_array_elements(p_users)
    LOOP
        IF user_item->>'phone' ~ '^\+?\d{7,15}$' THEN
            PERFORM upsert_user(user_item->>'name', user_item->>'phone');
        ELSE
            invalid_data := invalid_data || user_item;
        END IF;
    END LOOP;

    RAISE NOTICE 'Invalid entries: %', invalid_data;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_user(p_name TEXT DEFAULT NULL, p_phone TEXT DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE (p_name IS NOT NULL AND name = p_name)
       OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;