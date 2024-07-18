from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
backend_url = "http://backend:5000/posts"  # URL of the backend API

@app.route('/')
def index():
    response = requests.get(backend_url)
    if response.status_code == 200:
        posts = response.json()
    else:
        posts = []
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        scale_value = 'your_scale_value_here'  # Determine the appropriate value for your shard key field

        new_post = {
            'title': title,
            'content': content,
            'scale': scale_value
        }

        response = requests.post(backend_url, json=new_post)
        if response.status_code == 201:
            return redirect(url_for('index'))
        else:
            return "Error creating post", response.status_code
    return render_template('create_post.html')

@app.route('/edit_post/<string:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post_url = f"{backend_url}/{post_id}"
    if request.method == 'POST':
        updated_post = {
            'title': request.form['title'],
            'content': request.form['content']
        }
        response = requests.put(post_url, json=updated_post)
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
            return "Error updating post", response.status_code
    else:
        response = requests.get(post_url)
        if response.status_code == 200:
            post = response.json()
        else:
            post = None
        return render_template('edit_post.html', post=post)

@app.route('/delete_post/<string:post_id>', methods=['POST'])
def delete_post(post_id):
    post_url = f"{backend_url}/{post_id}"
    response = requests.delete(post_url)
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return "Error deleting post", response.status_code

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
