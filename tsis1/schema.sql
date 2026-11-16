-- Create groups table

CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    group_name VARCHAR(50) UNIQUE NOT NULL
);


-- Insert default groups

INSERT INTO groups (group_name)
VALUES
    ('Family'),
    ('Work'),
    ('Friend'),
    ('Other')
ON CONFLICT (group_name) DO NOTHING;


-- Add new columns to contacts

ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS email VARCHAR(100);

ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS birthday DATE;

ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS group_id INTEGER;

ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;


-- Add foreign key to groups

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.table_constraints
        WHERE constraint_name = 'contacts_group_id_fkey'
          AND table_name = 'contacts'
    ) THEN
        ALTER TABLE contacts
        ADD CONSTRAINT contacts_group_id_fkey
        FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE SET NULL;
    END IF;
END $$;


-- Create phones table

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL,
    phone VARCHAR(30) UNIQUE NOT NULL,

    phone_type VARCHAR(10) NOT NULL
        CHECK (phone_type IN ('home', 'work', 'mobile')),

    FOREIGN KEY (contact_id)
        REFERENCES contacts(id)
        ON DELETE CASCADE
);


-- Copy existing phone numbers from contacts

INSERT INTO phones (contact_id, phone, phone_type)
SELECT id, phone, 'mobile'
FROM contacts
WHERE phone IS NOT NULL
  AND phone <> ''
ON CONFLICT (phone) DO NOTHING;