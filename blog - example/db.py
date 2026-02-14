import sqlite3

DB_NAME = "blog.db"


# --- ПІДКЛЮЧЕННЯ ДО БД ---
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# --- СТВОРЕННЯ ТА НАПОВНЕННЯ БД ---
def init_db():
    with get_db() as db:
        # 1. Створюємо таблицю для категорій (наприклад: "Персонажі", "Монстри")
        db.execute("""
        CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            slug TEXT UNIQUE NOT NULL
        )
        """)

        # 2. Створюємо таблицю для постів
        db.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            image TEXT,
            section_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (section_id) REFERENCES sections(id)
        )
        """)

        # 3. АВТОМАТИЧНЕ НАПОВНЕННЯ (щоб база не була пустою)
        # Перевіряємо, чи є вже розділи, щоб не дублювати їх
        check = db.execute("SELECT count(*) FROM sections").fetchone()[0]

        if check == 0:
            print("База пуста. Додаю розділи про Little Nightmares...")

            # Додаємо розділи
            sections_data = [
                ("Персонажі", "characters"),
                ("Монстри", "monsters"),
                ("Локації", "locations"),
                ("Теорії", "theories")
            ]

            for name, slug in sections_data:
                db.execute("INSERT INTO sections (name, slug) VALUES (?, ?)", (name, slug))

            # Додаємо тестовий пост про Шосту (Six) у розділ "Персонажі" (id=1)
            db.execute("""
                INSERT INTO posts (text, image, section_id) 
                VALUES (?, ?, ?)
            """, (
                "Шоста (Six) — головна героїня гри Little Nightmares. Це маленька дівчинка у впізнаваному жовтому дощовику.",
                "six_raincoat.jpg",
                1
            ))

            db.commit()
            print("Готово! Розділи створено.")


# --- ФУНКЦІЇ ОТРИМАННЯ ДАНИХ (SELECT) ---

def get_blog_sections():
    with get_db() as db:
        return db.execute("SELECT * FROM sections").fetchall()


def get_section_by_slug(section_slug):
    with get_db() as db:
        return db.execute(
            "SELECT * FROM sections WHERE slug = ?",
            (section_slug,)
        ).fetchone()


def get_section_by_id(section_id):
    with get_db() as db:
        return db.execute(
            "SELECT * FROM sections WHERE id = ?",
            (section_id,)
        ).fetchone()


def get_section_posts(section_id):
    with get_db() as db:
        return db.execute("""
                SELECT * FROM posts
                WHERE section_id = ?
                ORDER BY created_at DESC
            """, (section_id,)).fetchall()


# --- ФУНКЦІЇ ЗАПИСУ ДАНИХ (INSERT) ---

def create_new_post(text, image, section_id):
    with get_db() as db:
        db.execute("""
                    INSERT INTO posts (text, image, section_id)
                    VALUES (?, ?, ?)
                """, (text, image, section_id))
        db.commit()


# --- ЗАПУСК ---
if __name__ == "__main__":
    init_db()