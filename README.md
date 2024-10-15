Сначала копируйте данный проект в любое удобное место:

```
git clone https://github.com/KnightOfMelons/RESTful-API-Blog.git
```

Затем собираем проект с помощью Docker Compose: 

```
docker-compose up --build
```

Проект доступен будет по этому адресу:

```
http://localhost:5000
```

Затем можете зайти в Postman и опробовать эти команды (подготовил заранее, также не забудьте поставить методы POST/GET/DELETE и так далее):

POST http://localhost:5000/posts, а затем в Body пишите подобное (можете написать свои значения), чтобы добавить пост:

```
{
  "title": "My title example",
  "content": "This is the text for content example."
}
```

GET http://localhost:5000/posts и можете посмотреть все посты, которые только есть, вот пример:

```
[
    {
        "id": 2,
        "title": "Hi",
        "content": "This post has a very short title.",
        "likes": 0
    },
    {
        "id": 3,
        "title": "Hi",
        "content": "This post has a very short title.",
        "likes": 0
    },
    ....
```

GET http://localhost:5000/posts/1 и можно будет посмотреть подробнее про сам пост (в конце меняйте цифру для того поста,
какой хотите найти), выводиться будет содержание, заголовок, id и количество лайков:

```
{
    "content": "This post has a very short title.",
    "id": 1,
    "likes": 10,
    "title": "Hi"
}
```

PUT http://localhost:5000/posts/1 и можно будет изменить содержимое определенного поста, но в Body также нужно указать,
например:

```
{
  "title": "TEST TEST",
  "content": "TEST TEXT TEST."
}
```

DELETE http://localhost:5000/posts/2 и можно будет удалить пост под номером 2.
Можете потом также вбить GET http://localhost:5000/posts и посмотреть на количество
элементов.

POST http://localhost:5000/posts/3/like и можно будет поставить лайк посту. Выводиться будет количество лайков и id
поста (можно прям несколько раз запрос отправить, чтобы увеличить количество лайков):

```
{
    "likes": 4,
    "message": "Post liked"
}
```

DELETE http://localhost:5000/posts/3/like и можете убрать лайк с поста (также можно несколько раз отправить запрос):

```
{
    "likes": 2,
    "message": "Like removed"
}
```

Чтобы проверить все тесты - просто запускаете test_app.py

<hr>

Если вдруг не получилось что-то с Docker, то можете сделать всё вручную:

```
git clone https://github.com/KnightOfMelons/RESTful-API-Blog.git
```

Затем создайте свою базу данных в PostgresSQL (назовите её, например, bd_for_junior_blog) и вставьте адрес сюда:
```
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI',
                                                  'postgresql://ЛОГИН:ПАРОЛЬ@localhost:5432'
                                                  '/bd_for_junior_blog')
```

Затем просто запускаете main.py и переходите по адресу:
```
http://127.0.0.1:5000
```

Затем проводите все те же манипуляции, что и в прошлый раз с Postman