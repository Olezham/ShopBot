from flask import Flask, render_template, redirect, request, url_for

import uuid

app = Flask(__name__)

def generate_uid():
    return str(uuid.uuid4())

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/add-article-page', methods=['GET', 'POST'])
def add_article_page():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        file = request.files['formFile']
        
        try:
            file.save('/image' + generate_uid())
        except Exception as ex:
            print('Something wrong with file saving:')
            print(ex)
        add_article(title, price, description, file)
        print('Article seccsessfuly created')
        return redirect(url_for('/'))

    return render_template('add-article.html')

if __name__ == '__main__':
    app.run(debug=True)




 