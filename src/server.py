from flask import Flask, request
from flask_restful import Api
from api.hello_world import HelloWorld
from api.library import Library

app = Flask(__name__)
api = Api(app)

api.add_resource(HelloWorld, '/hello-world')
api.add_resource(Library, '/')

@app.route('/users/create', methods=['POST'])
def add_user():
    data = request.get_json()
    
    return Library.add_user(
        data['username'],
        data['password'],
        data['first_name'],
        data['middle_name'],
        data['last_name'],
        data['email'],
        data['phone']
    )[1]

@app.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    return Library.login(
        data['username'],
        data['password']
    )[1]

@app.route('/users')
def list_all_users():
    head = request.headers
    return Library.get_all_users(
        head['session']
    )

@app.route('/books')
def list_all_books():
    head = request.headers
    return Library.get_all_books(
        head['session']
    )

@app.route('/authors')
def list_all_authors():
    head = request.headers
    return Library.get_all_authors(
        head['session']
    )

@app.route('/books/genre/<genre>')
def list_books_by_genre(genre):
    head = request.headers
    return Library.search_by_genre(
        head['session'], genre
    )

@app.route('/books/author/<author_id>')
def list_books_by_author_id(author_id):
    head = request.headers
    return Library.search_by_author_id(
        head['session'], author_id
    )

@app.route('/users/logout', methods=['PUT'])
def logout():
    head = request.headers
    return Library.logout(
        head['session']
    )[0]

@app.route('/users/checkouts', methods=['GET'])
def list_checkouts():
    head = request.headers
    return Library.list_all_checkouts(
        head['session']
    )

@app.route('/users/delete/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    head = request.headers
    return Library.remove_user(
        head['session'], user_id
    )[1]

@app.route('/users/edit-username', methods=['PUT'])
def change_username():
    head = request.headers
    data = request.get_json()
    
    return Library.change_username(
        head['session'],
        data['new_username']
    )[1]

@app.route('/users/change-password', methods=['PUT'])
def change_password():
    head = request.headers
    data = request.get_json()
    
    return Library.change_password(
        head['session'],
        data['new_password']
    )[1]

@app.route('/users/borrow-book', methods=['POST'])
def checkout_book():
    head = request.headers
    data = request.get_json()
    
    return Library.checkout_book(
        head['session'],
        data['book_copy_id'],
        data['current_date']
    )[1]

@app.route('/users/reserve-book', methods=['POST'])
def reserve_book():
    head = request.headers
    data = request.get_json()
    
    return Library.reserve_book(
        head['session'],
        data['book_id']
    )[1]

@app.route('/books/return-book', methods=['PUT'])
def return_book():
    head = request.headers
    data = request.get_json()
    
    return Library.return_book(
        head['session'],
        data['return_date'],
        data['checked_out_id'],
        data['book_copy_id']
    )[1]

if __name__ == '__main__':
    app.run(debug=True)
