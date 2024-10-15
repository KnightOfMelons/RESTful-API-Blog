import unittest
from main import app, db  # Post
import json


class BlogTestCase(unittest.TestCase):
    # Эта штука будет запускаться перед каждым тестом
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        # Ниже сделал 'sqlite:///:memory:', чтобы БД SQLite уничтожилась после выполнения
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    # Эта будет запускаться ПОСЛЕ каждого теста
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Это тестирование на создание поста
    def test_create_post(self):
        response = self.app.post('/posts', json={
            'title': 'Test Post',
            'content': 'This is a test post'
        })
        # Тут проверяю на то, что статус ответа 201, то есть, что создано
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Test Post')
        self.assertEqual(data['content'], 'This is a test post')

    # Это тест на получение всех постов
    def test_get_posts(self):
        self.app.post('/posts', json={'title': 'First Post',
                                      'content': 'Content of the first post.'})
        response = self.app.get('/posts')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'First Post')

    # Получение поста по id его
    def test_get_single_post(self):
        self.app.post('/posts', json={'title': 'Single Post',
                                      'content': 'Content of the post.'})
        response = self.app.get('/posts/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Single Post')

    # Тестирование обновление поста
    def test_update_post(self):
        # тут сначала создается пост
        self.app.post('/posts', json={'title': 'Old Title',
                                      'content': 'Old content.'})
        # потом мы его обновляем
        response = self.app.put('/posts/1', json={'title': 'New Title',
                                                  'content': 'New content.'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'New Title')
        self.assertEqual(data['content'], 'New content.')

    # Тест на удаление поста
    def test_delete_post(self):
        # Сначала также создаем пост
        self.app.post('/posts', json={'title': 'To be deleted',
                                      'content': 'This post will be deleted soon.'})
        # Ну и тут удаляем пост
        response = self.app.delete('/posts/1')
        self.assertEqual(response.status_code, 204)  # 204 тут - это контента нет, но запрос успешен
        # Проверяется, что действительно удалён
        response = self.app.get('/posts/1')
        self.assertEqual(response.status_code, 404)

    # Добавление лайка
    def test_like_post(self):
        self.app.post('/posts', json={'title': 'Like me please',
                                      'content': 'Like this post.'})
        response = self.app.post('/posts/1/like')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['likes'], 1)  # тут имеется ввиду проверка, что лайков должно быть 1

    # Удаление лайка
    def test_unlike_post(self):
        self.app.post('/posts', json={'title': 'Unlike me',
                                      'content': 'This post will be unliked soon.'})
        # ну, как обычно, сначала лайкаем
        self.app.post('/posts/1/like')
        # затем удаляем лайк
        response = self.app.delete('/posts/1/like')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['likes'], 0)  # тут лайков не должно остаться


if __name__ == '__main__':
    unittest.main()

# должно быть в конце:
# Ran 7 tests in 0.097s
#
# OK
