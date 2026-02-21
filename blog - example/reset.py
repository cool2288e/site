import os

if os.path.exists("blog.db"):
    os.remove("blog.db")
    print("✅ Супер! Стару базу даних успішно видалено. Тепер можна запускати main.py!")
else:
    print("Файлу blog.db вже немає, все чисто!")