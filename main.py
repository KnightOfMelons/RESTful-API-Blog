from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789qwe123!@localhost:5432/bd_for_junior_blog'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)


with app.app_context():
    db.create_all()


# Это добавление поста
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    if not data or 'title' not in data or 'content' not in data:
        return abort(400, description="Invalid input")

    if not data['title'].strip() or not data['content'].strip():
        return abort(400, description="Title and content cannot be empty")

    new_post = Post(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'id': new_post.id,
                    'title': new_post.title,
                    'content': new_post.content}), 201


# Тут можно вывести все посты, которые только есть
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    posts_list = [{'id': post.id,
                   'title': post.title,
                   'content': post.content,
                   'likes': post.likes} for post in posts]

    return app.response_class(
        response=json.dumps(posts_list, ensure_ascii=False),  # ensure_ascii нужна для того, чтобы кириллица работала.
        status=200,
        mimetype='application/json'
    )


# Получение подробной информации о посте (после posts пишешь id его, типа: posts/3)
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'likes': post.likes})


# Для обновлении значений в посте (то есть в Postman в Body указываешь "title": "TEST TEST",
# а ещё "content": "TEST TEST TEST", только не забудь метод PUT выбрать)
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()

    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']

    db.session.commit()
    return jsonify({'id': post.id,
                    'title': post.title,
                    'content': post.content})


if __name__ == "__main__":
    app.run(debug=True)
