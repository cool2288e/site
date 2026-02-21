import sqlite3

DB_NAME = "blog.db"
conn = sqlite3.connect(DB_NAME)
conn.row_factory = sqlite3.Row

# Додаємо розділи, які підходять для гри
# INSERT OR IGNORE означає: "якщо такий розділ вже є, не видавай помилку"
conn.executemany("""
            INSERT OR IGNORE INTO sections (name, slug)
            VALUES (?, ?)""",
                 [
                     ("Персонажі", "characters"),
                     ("Трейлер", "monsters"),
                     ("Локації", "locations"),
                     ("Теорії", "theories")
                 ],
                 )

conn.commit()
print("Готово! Розділи про Little Nightmares додано в базу.")
conn.close()