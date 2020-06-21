from flask import Flask, flash, session, render_template, \
    url_for, jsonify, request, make_response, redirect, abort
from markupsafe import escape
from werkzeug.utils import secure_filename

#hooking with WSGI middleware
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

#middleware
app.wsgi_app = ProxyFix(app.wsgi_app)

# session secret key
app.secret_key = b'12345678'

@app.route('/',methods=['GET','POST'])
def home():
    if(request.method == 'POST'):
        f = request.files['file']
        if f:
            f.save('files/' + secure_filename(f.filename))
            flash('uploaded!!!!!')
            return '<h1>Uploaded the document</h1>'
    
    res = make_response(render_template('index.html',request_type=request.method,name="Arjun"))
    res.set_cookie('username','arjun')
    username = request.cookies.get('username')
    return res

@app.route('/none')
def redirect_demo():
    return redirect(url_for('about'))

@app.route('/abort')
def abort_demo():
    abort(401)
    print("this is never printed")

#defult page for page not found
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html',error=error),404 
    #404 to tell flash to set status code 404 by default is 200

@app.route('/user/<string:name>')
def user(name):
    return '<h2>Hey, {}</h2>'.format(escape(name))

@app.route('/about')
def about():
    return '<h1>About!</h1>'

@app.route('/userinfo')
def user_info():
    return jsonify({
        "name": "Arjun",
        "age": 21,
    })
    #also to_json()

#sessions on top of cookies
@app.route('/loginstatus', methods = ['GET', 'POST'])
def login_status():
    if request.method == 'POST':
        return redirect(url_for('logout'))
    if 'username' in session:
        return '''<h1>Logged in as {}</h1>
            <form method="post">
                <button type="submit">Logout</button>
            </form>
        '''.format(escape(session['username']))
    return '<h2>You are not logged in!!</h2>'

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('login_status'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_status'))

with app.test_request_context():
    url_for('static',filename='style.css')
    print(url_for('home'))
    print(url_for('user',name="arjun"))


if __name__ == '__main__':
    app.run(debug=True)