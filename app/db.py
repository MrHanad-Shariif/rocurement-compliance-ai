import psycopg2
import psycopg2.extras
import os

def get_db():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "procurement_ai"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "admin123"),
        host=os.getenv("POSTGRES_HOST", "localhost")
    )
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(150) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL DEFAULT 'user',
        reset_token VARCHAR(255),
        reset_token_expiry TIMESTAMP
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS validations (
        id SERIAL PRIMARY KEY,
        legal_entity_id INTEGER,
        item_type TEXT,
        description TEXT,
        quantity INTEGER,
        result TEXT,
        vendor_ids TEXT,
        rfq_file TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    # Migration: add vendor_ids column if not exists
    cursor.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name='validations' AND column_name='vendor_ids'
        ) THEN
            ALTER TABLE validations ADD COLUMN vendor_ids TEXT;
        END IF;
    END$$;
    """)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendors (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        language VARCHAR(10) NOT NULL DEFAULT 'en'
    )
    ''')
    # Insert default admin if not exists
    cursor.execute("SELECT * FROM users WHERE username=%s", ("admin",))
    if not cursor.fetchone():
        from passlib.hash import bcrypt
        hashed = bcrypt.hash("admin123")
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", ("admin", hashed, "admin"))
    conn.commit()
    cursor.close()
    conn.close()

init_db()
