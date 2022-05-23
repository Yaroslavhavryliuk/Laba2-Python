from colors import greenText, yellowText, redText, blueText
from author import Author
from book import Book
from library import Library

if __name__ == '__main__':

    library = Library()

    while True:
        while True:
            greenText('Choose the command:\n' +
                      '1. Load data from DB\n' +
                      '2. Add new author\n' +
                      '3. Add new book\n' +
                      '4. Edit author information\n' +
                      '5. Edit book information\n' +
                      '6. Delete author\n' +
                      '7. Delete book\n' +
                      '8. Find author\n' +
                      '9. Find book\n' +
                      '10. Print all authors\n' +
                      '11. Print all books of author\n' +
                      '12. Exit')
            chosen = int(input())
            if chosen == 1:
                library.loadFromDB()
            elif chosen == 2:
                greenText('Enter author name: ')
                authorName = input()
                newAuthor = Author(0, authorName)
                library.addAuthor(newAuthor)
            elif chosen == 3:
                greenText('Enter the author id: ')
                authorId = int(input())
                if library.getAuthor(authorId, False):
                    greenText('Enter the book title: ')
                    bookTitle = input()
                    greenText('Enter the book genre: ')
                    bookGenre = input()
                    greenText('Enter the book pages number: ')
                    bookPages = int(input())
                    newBook = Book(0, authorId, bookTitle, bookGenre, bookPages)
                    library.addBook(newBook)
            elif chosen == 4:
                greenText('Enter the author id: ')
                authorId = int(input())
                library.editAuthor(authorId)
            elif chosen == 5:
                greenText('Enter the book id: ')
                bookId = int(input())
                library.editBook(bookId)
            elif chosen == 6:
                greenText('Enter the author id: ')
                authorId = int(input())
                library.deleteAuthor(authorId)
            elif chosen == 7:
                greenText('Enter the book id: ')
                bookId = int(input())
                library.deleteBook(bookId)
            elif chosen == 8:
                greenText('Enter the author id: ')
                authorId = int(input())
                library.getAuthor(authorId, True)
            elif chosen == 9:
                greenText('Enter the book id: ')
                bookId = int(input())
                library.getBook(bookId, True)
            elif chosen == 10:
                library.printAllAuthors()
            elif chosen == 11:
                greenText('Enter the author id: ')
                authorId = int(input())
                library.printAllBooksOfAuthor(authorId)
            elif chosen == 12:
                exit()
            else:
                redText('Unknown command')

