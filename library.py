import sqlite3
from author import Author
from book import Book
from colors import greenText, yellowText, redText, blueText

class Library:
    def __init__(self):
        self.authors = dict()
        self.books = dict()
        self.isDataLoad = False

        dbFile = 'library.sqlite'
        self.db = sqlite3.connect(dbFile)
        self.cursor = self.db.cursor()

    def clean(self):
        self.authors = dict()
        self.books = dict()

    def PrintData(self):

        try:
            self.cursor.execute('SELECT id, name FROM Authors')
            results = self.cursor.fetchall()
            for row in results:
                authorId = row[0]
                authorName = row[1]
                yellowText("Author id: " + str(authorId) + ", name: " + authorName)

            self.cursor.execute('SELECT * FROM Books')
            results = self.cursor.fetchall()
            for row in results:
                bookId = row[0]
                author_id = row[1]
                bookTitle = row[2]
                bookGenre = row[3]
                bookPages = row[4]
                blueText(
                    "Book id: " + str(bookId) + ", author id: " + str(author_id) + ", title: " + bookTitle +
                    ", genre: " + str(bookGenre) + ", pages: " + str(bookPages))

        except:
            redText("Data recieving ERROR ")


    def loadFromDB(self):
        self.clean()

        self.cursor.execute('SELECT * FROM Authors')
        results = self.cursor.fetchall()
        for row in results:
            authorId = row[0]
            authorName = row[1]
            author = Author(authorId, authorName)
            self.authors[authorId] = author

        self.cursor.execute('SELECT * FROM Books')
        results = self.cursor.fetchall()
        for row in results:
            bookId = row[0]
            author_id = row[1]
            bookTitle = row[2]
            bookGenre = row[3]
            bookPages = row[4]
            book = Book(bookId, author_id, bookTitle, bookGenre, bookPages)
            self.books[bookId] = book

        self.isDataLoad = True
        self.PrintData()


    def addAuthor(self, newAuthor):
        if not self.isDataLoad:
            self.loadFromDB()
        if len(self.authors) == 0:
            key = 0
        else:
            key = max(self.authors.keys()) + 1
        newAuthor.id = key
        self.authors[key] = newAuthor

        try:
            self.cursor.execute('INSERT INTO Authors (id, name) VALUES (?, ?)', (newAuthor.id, newAuthor.name))
            self.db.commit()
            greenText('Author added')
        except:
            redText("Author adding ERROR")
            self.db.rollback()


    def addBook(self, newBook):
        if not self.isDataLoad:
            self.loadFromDB()
        if len(self.books) == 0:
            key = 0
        else:
            key = max(self.books.keys()) + 1
        newBook.id = key
        self.books[key] = newBook

        try:
            self.cursor.execute('INSERT INTO Books (id, author_id, title, genre, pages) VALUES (?, ?, ?, ?, ?)',
                (newBook.id, newBook.authorId, newBook.title, newBook.genre, newBook.pages))
            self.db.commit()
            greenText('Book added')
        except:
            redText('Book adding ERROR')
            self.db.rollback()


    def editAuthor(self, authorId):
        if not self.isDataLoad:
            self.loadFromDB()
        if self.getAuthor(authorId, False):
            greenText('Enter new author name: ')
            authorName = input()
            self.authors[authorId].name = authorName

            try:
                self.cursor.execute("UPDATE Authors SET name = '" + authorName + "' WHERE id = " + str(authorId))
                self.db.commit()
                greenText('Author edited')
            except:
                redText('Author editing ERROR')
                self.db.rollback()
        else:
            redText('Author does not exist')


    def editBook(self, bookId):
        if not self.isDataLoad:
            self.loadFromDB()
        if self.getBook(bookId, False):
            book_copy = self.books[bookId]
            greenText("What do you want to edit \n" +
                      "1. Book title \n" +
                      "2. Book genre \n" +
                      "3. Book pages number")

            choice = int(input())
            if choice == 1:
                greenText('Enter new title: ')
                bookTitle = input()
                book_copy.title = bookTitle
                sql_part = "title = '" + bookTitle + "'"
            elif choice == 2:
                greenText('Enter new genre: ')
                bookGenre = input()
                book_copy.genre = bookGenre
                sql_part = "genre = '" + bookGenre + "'"
            elif choice == 3:
                greenText('Enter new number of pages: ');
                bookPages = input()
                book_copy.pages = bookPages
                sql_part = "pages = '" + str(bookPages) + "'"
            else:
                redText('Unknown command')
                return
            self.books[bookId] = book_copy
            try:
                self.cursor.execute("UPDATE Books SET " + sql_part + " WHERE id = " + str(bookId))
                self.db.commit()
                greenText('Book edited')
            except:
                redText('Book editing ERROR')
                self.db.rollback()
        else:
            redText('Book does not exist')


    def deleteAuthor(self, authorId):
        if not self.isDataLoad:
            self.loadFromDB()
        if self.getAuthor(authorId, False):
            booksIdSet = set()
            for bookId in self.books.keys():
                if self.books[bookId].authorId == authorId:
                    booksIdSet.add(bookId)

            for bookId in booksIdSet:
                self.deleteBook(self.books[bookId].id)
            del self.authors[authorId]

            try:
                self.cursor.execute('DELETE FROM Authors WHERE id = ?', (authorId,))
                self.db.commit()
                greenText('Author deleted')
            except:
                redText('Author deleting ERROR')
                self.db.rollback()
        else:
            redText('Author does not exist')


    def deleteBook(self, bookId):
        if not self.isDataLoad:
            self.loadFromDB()
        if self.getBook(bookId, False):
            del self.books[bookId]
            try:
                self.cursor.execute('DELETE FROM Books WHERE id = ?', (bookId,))
                self.db.commit()
                greenText('Book deleted')
            except:
                print('Book deleting ERROR')
                self.db.rollback()
        else:
            redText('Book does not exist')


    def getAuthor(self, authorId, boolToPrint):
        try:
            self.cursor.execute('SELECT * FROM Authors WHERE id = ?', (authorId,))
            results = self.cursor.fetchall()
            if len(results) == 0:
                redText('Incorrect id')
            for row in results:
                authorId = row[0]
                authorName = row[1]
                if boolToPrint:
                    yellowText('Author id: ' + str(authorId) + ', name: ' + authorName)
                return True
        except:
            redText('Author getting ERROR')
            self.db.rollback()
            return False


    def getBook(self, bookId, boolToPrint):
        try:
            self.cursor.execute('SELECT * FROM Books WHERE id = ?', (bookId,))
            results = self.cursor.fetchall()
            if len(results) == 0:
                redText('Incorrect id')
            for row in results:
                bookId = row[0]
                author_id = row[1]
                bookTitle = row[2]
                bookGenre = row[3]
                bookPages = row[4]
                if boolToPrint:
                    blueText("Book id: " + str(bookId) + ", author id: " + str(
                        author_id) + ", title: " + bookTitle +
                                ", genre: " + bookGenre + ", pages: " + str(bookPages))
                return True
        except:
            redText('Book getting ERROR')
            self.db.rollback()
            return False


    def printAllAuthors(self):
        self.cursor.execute('SELECT id, name FROM Authors')
        results = self.cursor.fetchall()
        if len(results) == 0:
            redText("No authors in DB")

        for row in results:
            authorId = row[0]
            authorName = row[1]
            yellowText("Author id: " + str(authorId) + ", name: " + authorName)


    def printAllBooksOfAuthor(self, authorId):
        if self.getAuthor(authorId, True):
            self.cursor.execute('SELECT * FROM Books WHERE author_id = ?', (authorId,))
            results = self.cursor.fetchall()
            if len(results) == 0:
                redText("No books of this author in DB")
            for row in results:
                bookId = row[0]
                author_id = row[1]
                bookTitle = row[2]
                bookGenre = row[3]
                bookPages = row[4]
                blueText("Book id: " + str(bookId) + ", author id: " + str(
                    author_id) + ", title: " + bookTitle +
                            ", genre: " + bookGenre + ", pages: " + str(bookPages))
        else:
            redText('Author does not exist')
