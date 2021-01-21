from flask import Flask, render_template, request, redirect
import string

app = Flask(__name__)
app.config['DEBUG'] = True

def check_inputs(name, pwd, check, form_info):
    # Check the submitted username, password, and retyped password.
    valid_name = check_username(name, form_info)
    valid_password = check_password(pwd, form_info)
    valid_match = valid_password and check_confirm(check, pwd, form_info)

    # Return False if any of the checks fail.
    return valid_name and valid_password and valid_match

def check_username(name, form_info):
    return 3 <= len(name) <= 8 and ' ' not in name # Return False if incorrect length, or if spaces are present.

def check_password(pwd, form_info):
    special_char = letter = digit = False

    # Return False if incorrect length, or if spaces are present.
    if len(pwd) < 8 or ' ' in pwd:
        return False

    # Check if pwd contains a letter, number, and special symbol.
    for char in pwd:
        if char in string.ascii_letters:
            letter = True
        if char in string.digits:
            digit = True
        if char in ['%', '#', '&', '*']:
            special_char = True
    
    # Return False if missing any of the three.
    return letter and digit and special_char

def check_confirm(check, pwd, form_info):
    return check == pwd     # Return False if the retyped password doesn't match the first.

@app.route('/', methods=['GET', 'POST'])
def sign_up():
    inputs = {
        # Label: [type, name, placeholder]
        'Username': ['text', 'username', '3-8 characters, no spaces'],
        'Password': ['password', 'password','8 or more characters, no spaces'],
        'Confirm Password': ['password', 'confirm', 'Retype password']
    }
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        # If all of the input fields contain valid data, send the user to the success page.
        if check_inputs(username, password, confirm, inputs):
            return redirect('/success')

    tab_title = "Flask Project"
    page_title = "Improve Form UX"
    return render_template('register.html', tab_title=tab_title, page_title=page_title,
        inputs=inputs)

@app.route('/success', methods=['GET', 'POST'])
def success():
    tab_title = "Flask Project"
    page_title = "Success!"
    return render_template('success.html', tab_title=tab_title, page_title=page_title)

if __name__ == '__main__':
    app.run()