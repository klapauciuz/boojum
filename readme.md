# Сервис рекомендаций Boojum

![screenshot-127.0.0.1 5000 2015-06-13 01-43-17.png](https://bitbucket.org/repo/BpxjaA/images/280684537-screenshot-127.0.0.1%205000%202015-06-13%2001-43-17.png)
![screenshot-127.0.0.1 5000 2015-06-13 01-42-59.png](https://bitbucket.org/repo/BpxjaA/images/1616929476-screenshot-127.0.0.1%205000%202015-06-13%2001-42-59.png)
![screenshot-127.0.0.1 5000 2015-06-13 01-54-20.png](https://bitbucket.org/repo/BpxjaA/images/1360912581-screenshot-127.0.0.1%205000%202015-06-13%2001-54-20.png)

### После каждого пула затираем бд
```
#!mongo
use boojom
db.dropDatabase()
```
регистрируем юзера, добавляем пару тегов и объектов из вики или ластфм(оттуда текст моет парситься заметно долго после клика на submit)

## Зависимости

flask
pymongo
bson.json_util
werkzeug
faker


## Сгенерисровать временные данные базы для тесирования (осторожно, сначала стирает базу тегов и объектов)

python fixtures.py