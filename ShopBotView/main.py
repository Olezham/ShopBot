from flask import Flask, render_template, redirect, request, url_for, send_from_directory

import mysql 

import uuid

app = Flask(__name__)

def generate_uid():
    return str(uuid.uuid4())

@app.route('/')
def index():
    articles = mysql.get_all_articles()
    return render_template('index.html',articles=articles)

@app.route('/add-article-page', methods=['GET', 'POST'])
def add_article_page():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        file = request.files['formFile']
        file_name = f'{generate_uid()}.png'
        try:
            file.save(f'static/image/{file_name}')
        except Exception as ex:
            print('Something wrong with file saving:')
            print(ex)
        mysql.add_article(title, price, description, file_name)
        print('Article seccsessfuly created')
        return redirect(url_for('index'))

    return render_template('add-article.html')


@app.route('/image/<string:image>')
def imageAPI(image):
    return send_from_directory(directory='static/image',path=image)



@app.route('/del-article/<string:image>')
def del_article(image):
    mysql.delete_article(image)
    return redirect(url_for('index'))

    

if __name__ == '__main__':
    app.run(debug=True)




 