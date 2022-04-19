from .api import AddBooks, ViewBooks, DeleteBook

book_routes = [
    (AddBooks, '/add/books'),
    (ViewBooks, '/view/books'),
    (DeleteBook, '/delete/book/<book_id>')
]
