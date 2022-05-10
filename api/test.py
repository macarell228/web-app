from requests import delete, post, get

print(post('http://localhost:5000/api/v2/news').json())
print(post('http://localhost:5000/api/v2/news',
           json={'title': 'Заголовок',
                 'content': 'Текст новости',
                 'author_id': 1,
                 'seem_for': '1, 2, 3, 4, 5',
                 'date': '2022-05-7 13:08:21.06'}).json())

print(get('http://localhost:5000/api/v2/news').json())
print(get('http://localhost:5000/api/v2/news/1').json())

print(delete('http://localhost:5000/api/v2/news/999').json())
print(delete('http://localhost:5000/api/v2/news/1').json())
