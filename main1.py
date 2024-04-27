from flask import Flask, jsonify, Response, request
from markupsafe import escape
from flask import render_template
import json

app = Flask(__name__)

def make_bold(funct_name):
    def wrapper():
        return "<b>"+funct_name()+"</b>"
    return wrapper

def make_emp(funct_name):
    def wrapper():
        return "<em>"+funct_name()+"</em>"
    return wrapper

def make_underline(funct_name):
    def wrapper():
        return "<u>"+funct_name()+"</u>"

    return wrapper

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/bye")
@make_bold
@make_emp
@make_underline
def good_bye():
    return "<p>Good Bye</p>"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/home/<name>')
def home():
    return render_template('home.html', name=name)


@app.route('/api/users')
def get_users():
    users = [{'id': 1, 'username': 'Alice'}, {'id': 2, 'username': 'Bob'}]
    return jsonify(users)

@app.route('/api/users2')
def get_users2():
    users = [{'id': 1, 'username': 'sweety'},
             {'id': 2, 'username': 'pandey'}]
    response = Response(
        response=json.dumps(users),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/square', methods=['GET'])
def squarenumber():
    # If method is GET, check if  number is entered
    # or user has just requested the page.
    # Calculate the square of number and pass it to
    # answermaths method
    if request.method == 'GET':
   # If 'num' is None, the user has requested page the first time
        if(request.args.get('num') == None):
            return render_template('squarenum.html')
          # If user clicks on Submit button without
          # entering number display error
        elif(request.args.get('num') == ''):
            return "<html><body> <h1>Invalid number</h1></body></html>"
        else:
          # User has entered a number
          # Fetch the number from args attribute of
          # request accessing its 'id' from HTML
            number = request.args.get('num')
            sq = int(number) * int(number)
            # pass the result to the answer HTML
            # page using Jinja2 template
            return render_template('answer.html',
                                   squareofnum=sq, num=number)


# @app.route('/login', methods=['POST'])
# def login():
#     error = None
#     if request.method == 'POST':
        
#     return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run(debug=True)
