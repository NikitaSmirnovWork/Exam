import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARY_FILE = os.path.join(BASE_DIR, "library.json")

class Book:
    instances = []
    total_books = 0

    def __init__(self, id, title, author, genre, year, description, is_read=False, is_favorite=False):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.description = description
        self.is_read = is_read
        self.is_favorite = is_favorite
        Book.instances.append(self)
        Book.total_books += 1
        # self.rating = 0

    def describe(self):
        return f"{self.id} - {self.title} by {self.author} ({self.year})"

    def __str__(self):
        return self.describe()

'''
def all_books():
    while True:
        print("\nВсе книги:")
        for obj in Book.instances:
            print(obj)
        
        print("\nВыберите действие:")
        print("1 - Добавить книгу в библиотеку.")
        print("2 - Выбрать книгу.")
        print("3 - Поиск книги по фильтру.")
        print("4 - Назад в главное меню.")

        choice = input()

        if choice == "1":
            add_book()
        elif choice == "2":
            select_book()
        elif choice == "3":
            search_books()
        elif choice == "4":
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")'''
    
def all_books():
    f_genre = None
    f_read = None
    sort_key = None
    sort_reverse = False

    while True:
        books = Book.instances[:]
        if f_genre:
            books = [b for b in books if f_genre.lower() in b.genre.lower()]
        if f_read is not None:
            books = [b for b in books if b.is_read == f_read]
        if sort_key:
            books = sorted(books, key=lambda b: getattr(b, sort_key), reverse=sort_reverse)

        print("\nВсе книги:")
        if not books:
            print("   << пусто >>")
        else:
            for i, book in enumerate(books, start=1):
                print(f"{i}. {book}")
        
        print("\nВыберите действие:")
        print("1 - Добавить книгу")
        print("2 - Выбрать книгу")
        print("3 - Поиск по фильтру")
        print("4 - Сортировка")
        print("5 - Фильтрация")
        print("6 - Сбросить всё")
        print("7 - Назад в главное меню")

        choice = input().strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            select_book()
        elif choice == "3":
            search_books()
        elif choice == "4":
            print("Сортировать по (название/автор/год):")
            field = input().lower()
            if field in ["название", "автор", "год"]:
                m = {"название": "title", "автор": "author", "год": "year"}
                sort_key = m[field]
                rev = input("По возрастанию? (да/нет): ").lower()
                sort_reverse = (rev != "да")
            else:
                print("Непонятный критерий, сортировка не изменилась.")
        elif choice == "5":
            genre = input("Жанр (оставьте пустым, если не надо): ")
            read = input("Статус (прочитана/не прочитана/любая): ").lower()
            f_genre = genre if genre else None
            if read == "прочитана":
                f_read = True
            elif read == "не прочитана":
                f_read = False
            else:
                f_read = None
        elif choice == "6":
            f_genre = None
            f_read = None
            sort_key = None
            sort_reverse = False
            print("Фильтры и сортировка сброшены.")
        elif choice == "7":
            break
        else:
            print("Неверный выбор. Попробуйте ещё раз.")

def save_to_file(filename=LIBRARY_FILE):
    data = []
    for book in Book.instances:
        data.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "year": book.year,
            "description": book.description,
            "is_read": book.is_read,
            "is_favorite": book.is_favorite,
            # "rating": book.rating
        })
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(">> Библиотека сохранена в файл.")

def load_from_file(filename=LIBRARY_FILE):
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден. Начинаем с пустой библиотеки.")
        return
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён или пуст. Начинаем с пустой библиотеки.")
        return
    Book.instances.clear()
    Book.total_books = 0
    for item in data:
        Book(
            id=item["id"],
            title=item["title"],
            author=item["author"],
            genre=item["genre"],
            year=item["year"],
            description=item["description"],
            is_read=item["is_read"],
            is_favorite=item["is_favorite"]
        )
    print(">> Библиотека загружена из файла.")

def first_list():
    while True:
        print("\n" + "="*40)
        print("   Новосибирская Библиотека")
        print("="*40)
        print("1 - Все книги")
        print("2 - Избранные книги")
        print("3 - Сохранить библиотеку")
        print("4 - Загрузить библиотеку")
        print("5 - Выход")
        print("-"*40)
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == "1":
            all_books()
        elif choice == "2":
            favorite_books()
        elif choice == "3":
            save_to_file()
        elif choice == "4":
            load_from_file()
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

def add_book():
    if Book.instances:
        new_id = max(book.id for book in Book.instances) + 1
    else:
        new_id = 1
    title = input("Название: ").strip()
    author = input("Автор: ").strip()
    genre = input("Жанр: ").strip()
    year = input("Год издания: ").strip()
    description = input("Описание: ").strip()
    
    if not title or not author or not genre or not year or not description:
        print("Ошибка: нужно заполнить все поля! Книга не добавлена.")
        return
    
    new_book = Book(new_id, title, author, genre, year, description)
    print(f"Книга '{new_book.title}' успешно добавлена!")

def select_book():
    if not Book.instances:
        print("В библиотеке пока нет книг.")
        return

    print("\nСписок книг:")
    for idx, book in enumerate(Book.instances, start=1):
        print(f"{idx}. {book}")

    try:
        ch = int(input("Введите номер книги: ")) - 1
    except ValueError:
        print("Это не число.")
        return

    if 0 <= ch < len(Book.instances):
        book = Book.instances[ch]
        manage_selected_book(book)
    else:
        print("Нет такой книги.")

def manage_selected_book(book):
    while True:
        print(f"\n--- {book} ---")
        print("1 - Редактировать")
        print("2 - Переключить статус (прочитана/не прочитана)")
        print("3 - Переключить избранное")
        print("4 - Назад")

        cmd = input()

        if cmd == "1":
            if edit_book(book):
                break
        elif cmd == "2":
            book.is_read = not book.is_read
            status = "прочитана" if book.is_read else "не прочитана"
            print(f"Статус изменён на '{status}'.")
        elif cmd == "3":
            book.is_favorite = not book.is_favorite
            fav = "добавлена в" if book.is_favorite else "удалена из"
            print(f"Книга {fav} избранного.")
        elif cmd == "4":
            break
        else:
            print("Неизвестная команда.")

def edit_book(book):
    code = input("Введите секретный код для редактирования: ")
    if code != "TBank":
        print("Неверный код! Доступ запрещён.")
        return False
    
    while True:
        print(f"\nРедактирование: {book}")
        print("1 - Название")
        print("2 - Автор")
        print("3 - Жанр")
        print("4 - Год")
        print("5 - Описание")
        print("6 - Удалить книгу")
        print("7 - Назад")

        ch = input()

        if ch == "1":
            new_val = input("Новое название: ").strip()
            if new_val:
                book.title = new_val
                print("Название обновлено.")
            else:
                print("Пустое название недопустимо.")
        elif ch == "2":
            new_val = input("Новый автор: ").strip()
            if new_val:
                book.author = new_val
                print("Автор обновлён.")
            else:
                print("Пусто.")
        elif ch == "3":
            new_val = input("Новый жанр: ").strip()
            if new_val:
                book.genre = new_val
                print("Жанр обновлён.")
            else:
                print("Пусто.")
        elif ch == "4":
            new_val = input("Новый год: ").strip()
            if new_val:
                book.year = new_val
                print("Год обновлён.")
            else:
                print("Пусто.")
        elif ch == "5":
            new_val = input("Новое описание: ").strip()
            if new_val:
                book.description = new_val
                print("Описание обновлено.")
            else:
                print("Пусто.")
        elif ch == "6":
            Book.instances.remove(book)
            Book.total_books -= 1
            print(f"Книга '{book.title}' удалена.")
            return True
        elif ch == "7":
            break
        else:
            print("Неверный пункт.")
    return False

def search_books():
    term = input("Название или автор (можно часть): ").lower()
    genre = input("Жанр (оставьте пустым, если не важно): ").lower()
    year = input("Год (оставьте пустым, если не важно): ")
    read = input("Только прочитанные? (да/нет): ").lower()

    results = Book.instances[:]

    if term:
        results = [b for b in results if term in b.title.lower() or term in b.author.lower()]
    if genre:
        results = [b for b in results if genre in b.genre.lower()]
    if year:
        results = [b for b in results if b.year == year]
    if read == 'да':
        results = [b for b in results if b.is_read]

    if results:
        print("\nНайденные книги:")
        for i, b in enumerate(results, 1):
            print(f"{i}. {b}")
    else:
        print("Ничего не найдено.")

def favorite_books():
    while True:
        favs = [book for book in Book.instances if book.is_favorite]
        if not favs:
            print("\nВ избранном пусто.")
            input("Нажмите Enter, чтобы вернуться...")
            return

        print("\n--- Избранное ---")
        for idx, book in enumerate(favs, 1):
            print(f"{idx}. {book}")

        print("\n0 - Назад")
        print("Введите номер книги для выбора:")

        try:
            choice = int(input())
        except ValueError:
            print("Введите число.")
            continue

        if choice == 0:
            break
        elif 1 <= choice <= len(favs):
            book = favs[choice - 1]
            manage_selected_book(book)
        else:
            print("Нет такой книги.")

load_from_file()
first_list()
