# Evolution Server
## Требования
- [Python ~3.10.4](https://www.python.org/downloads/)
- [PostgreSQL ~14.4](https://www.postgresql.org/download/)
- [PostGIS ~3.2](https://postgis.net/install/)
- Переменных среды(/.env или):
  - DB_NAME \- Название базы данных 
  - DB_USER \- Имя пользователя
  - DB_PASSWORD \- Пароль пользователя
  - DB_HOST \- Адрес базы данных
  - DB_PORT \- Порт базы данных

## Установка
1. Добавить в переменные среды:
    - DB_NAME \- Название базы данных 
    - DB_USER \- Имя пользователя
    - DB_PASSWORD \- Пароль пользователя
    - DB_HOST \- Адрес базы данных
    - DB_PORT \- Порт базы данных 
2. Добавить в базу данных типы из /SQLtype.sql
3. Установить Python библиотеки из /requirements.txt
    

## Запуск
    main.py

## Роли пользователей
- NO_REGISTRATION - Информации об пользователе нет в системе
- USER - стандартный набор возможностей
- ADMIN - максимальный набор возможностей




## API методы
- Обработка информация об пользователях
  - /users
  - /authentication
  - /nickName
  - /user.image
  
- Обработка информации об медитациях 
  - /meditation
  - /meditation.audio

    
### Уникальные типы данных
#### Перечисления
##### UserCategory(string)
- "NULL"
- "BLOGGER"
- "COMMUNITY"
- "ORGANIZATION"
- "EDITOR"
- "WRITER"
- "GARDENER"
- "FLOWER_MAN"
- "PHOTOGRAPHER"


##### UserGender(string)
- "MALE" 
- "FEMALE" 
- "OTHER" 


##### UserRole(string)
- "USER"
- "ADMIN"

##### TypeMeditation(String):
- "relaxation"
- "breathingPractices"
- "directionalVisualizations"
- "dancePsychotechnics"
- "DMD"

##### CountDayMeditation(string):
- "2-3days" 
- "4-5days" 
- "6-""7days"
##### TimeMeditation(string):
- "lessThan15minutes"
- "moreThan15AndLessThan60Minutes"
- "moreThan60Minutes"

#### Интерфейсы
##### MeditationPreferences
    
| Название       | Обязательный | Тип                |
|----------------|--------------|--------------------|
| typeMeditation | да           | TypeMeditation[]   |
| countDay       | да           | CountDayMeditation |
| time           | да           | TimeMeditation     |


#### Типы
##### Translate = {[index in language]?: string}
> Тип представят из себя объект(словарь), где в качестве ключа используется дву символьное обозначения естественного языка, а в качестве значения перевод 
### Параметры методов

#### /users
 - **GET**. Не требует авторизации. Не требует права администратора.
    > Возвращает информацию обо всех пользователях или конкретном

| Параметр                 | Обязательно | Описание                                                                                          |
|--------------------------|:-----------:|:--------------------------------------------------------------------------------------------------|
| /<user_id: string>       |     нет     | Вернуть информацию по конкретному пользователю, если user_id не задан вернет список пользователей |
| is_minimum_data: boolean |     нет     | Если true вернет краткую информацию об пользователе                                               |

- **POST**. Требует авторизации. Не требует права администратора. Authorization-Token должен принадлежать пользователю
    > Регистрирует пользователя в системе, если он не найден. Для этого необходимо передать в заголовке "Authorization" токен авторизации Firebase Auth. Данные принимаются в виде form-data

*Заголовок*

| Название      |     Тип      | Обязательно | Описание                       |
|---------------|:------------:|:-----------:|:-------------------------------|
| Authorization |    string    |     да      | Токен авторизации пользователя |

*Тело*:

| Название    |     Тип      | Обязательно | Описание                                          |
|-------------|:------------:|:-----------:|:--------------------------------------------------|
| nickname    |    string    |     да      | Уникальное имя пользователя                       |
| birthday    |   ISO-8601   |     да      | Дата рождения пользователя                        |
| status      |    string    |     нет     | Текстовое сообщение в профиле пользователя        |
| gender      |  UserGender  |     нет     | Пол пользователя                                  |
| category    | UserCategory |     нет     | Категория пользователя                            |
| image       |     file     |     нет     | Изображение пользователя                          |
| displayName |    string    |     нет     | Имя пользователя которое будет везде отображаться |

- **PUT**. Требует авторизации. Требует права администратора.
    > Обновляет данные пользователя на приведенные в теле. Данные принимаются в виде form-data
    
*Параметры*

| Название           | Обязательно | Описание                                                |
|--------------------|:-----------:|:--------------------------------------------------------|
| /<user_id: string> |     да      | id пользователя информацию которого необходимо обновить |

*Тело*:

| Параметр    |         Тип         | Описание                                          |
|-------------|:-------------------:|:--------------------------------------------------|
| nickname    |       string        | Уникальное имя пользователя                       |
| role        |      UserRole       | Роль пользователя                                 |
| birthday    |      ISO-8601       | Дата рождения пользователя                        |
| status      |       string        | Текстовое сообщение в профиле пользователя        |
| gender      |     UserGender      | Пол пользователя                                  |
| category    |    UserCategory     | Категория пользователя                            |
| image       |        file         | Изображение пользователя                          |
| displayName |       string        | Имя пользователя которое будет везде отображаться |

- **PATCH** Требует авторизации. Не требует права администратора.
    > Обновляет данные пользователя в системе, если он найден. Для этого необходимо передать в заголовке "Authorization" токен авторизации Firebase Auth. Данные принимаются в виде form-data


*Заголовок*

| Название      |     Тип      | Обязательно | Описание                       |
|---------------|:------------:|:-----------:|:-------------------------------|
| Authorization |    string    |     да      | Токен авторизации пользователя |

*Тело*:

| Название    |     Тип      | Обязательно | Описание                                          |
|-------------|:------------:|:-----------:|:--------------------------------------------------|
| nickname    |    string    |     да      | Уникальное имя пользователя                       |
| birthday    |   ISO-8601   |     да      | Дата рождения пользователя                        |
| status      |    string    |     нет     | Текстовое сообщение в профиле пользователя        |
| gender      |  UserGender  |     нет     | Пол пользователя                                  |
| category    | UserCategory |     нет     | Категория пользователя                            |
| image       |     file     |     нет     | Изображение пользователя                          |
| displayName |    string    |     нет     | Имя пользователя которое будет везде отображаться |

#### /authentication
 - **GET**. Требует авторизации. Не требует права администратора.
    > Возвращает данные пользователя на основании токена
   > 
*Заголовок*

| Название      |     Тип      | Обязательно | Описание                       |
|---------------|:------------:|:-----------:|:-------------------------------|
| Authorization |    string    |     да      | Токен авторизации пользователя |


### /user.image
 - **GET**. Не требует авторизации. Не требует права администратора.
 > Возвращает изображение запрошенного пользователя 

 *Параметры*

| Название           | Обязательно | Описание                                                |
|--------------------|:-----------:|:--------------------------------------------------------|
| /<user_id: string> |     да      | id пользователя информацию которого необходимо обновить |

### /nickname
- **GET**. Не требует авторизации. Не требует права администратора.
> Возвращает информацию об пользователях у которых совпадают nickname

 *Параметры*

| Название                 | Обязательно | Описание                                                      |
|--------------------------|:-----------:|:--------------------------------------------------------------|
| /<nickname: string>      |     да      | Nickname пользователя информацию которого необходимо получить |
| is_minimum_data: boolean |     нет     | Если true вернет краткую информацию об пользователе           |
| is_strong: boolean       |     нет     | Если true поиск будет иметь строгое совпадение                |


### /meditation
- **GET**. Не требует авторизации. Не требует права администратора.
    > Возвращает информацию обо всех, конкретных или по параметрам медитации. Если запрос имеет одновременно preferences=true и
popularToDay=true, то вернуть информацию обе медитациях одновременно

*Заголовок*

| Название        |  Тип   | Обязательно | Описание                                                                                   |
|-----------------|:------:|:-----------:|:-------------------------------------------------------------------------------------------|
| Authorization   | string |     нет     | Токен авторизации пользователя                                                             |
| Accept-Language | string |     да      | Дву символьное обозначения естественного языка на котором вернуть информацию об медитациях |

 *Параметры*

| Параметр                                        | Обязательно | Описание                                                                                                                      |
|-------------------------------------------------|:-----------:|:------------------------------------------------------------------------------------------------------------------------------|
| /<meditation_id: string>                        |     нет     | Вернуть информацию по конкретной медитации, если meditation_id не задан вернет список пользователей                           |
| is_minimum_data: boolean                        |     нет     | Если true вернет краткую информацию об медитации                                                                              |
| preferences:  MeditationPreferences or 'random' |     нет     | Вернет информацию об медитацию которая подходит под параметры, или случайную                                                  |
| getIsNotListened: boolean                       |     нет     | Если true то вернет исключит из рекомендаций медитации которые были уже просушены. *Так же необходимо передать Authorization* |
| popularToDay: boolean                           |     нет     | Вернет информацию об медитацию которая в текущие сутки является самой прослушиваемой                                          |

- **POST**. Требует авторизации. Требует права администратора.
    > Добавляет информацию об медитации. Данные принимаются в виде form-data. Чтобы загрузить аудиозаписи на разных языках, необходимо каждый чтобы поле в котором будет находиться аудио запись имело шаблон названия audio_language, где language - дву символьное обозначения естественного языка

*Заголовок*

| Название      |     Тип      | Обязательно | Описание                       |
|---------------|:------------:|:-----------:|:-------------------------------|
| Authorization |    string    |     да      | Токен авторизации пользователя |


 В данном случаем данные будут загружены и создаться новая медитация

*Тело*:

| Название       |      Тип       | Обязательно | Описание                                       |
|----------------|:--------------:|:-----------:|:-----------------------------------------------|
| name           |   Translate    |     да      | Название медитации                             |
| description    |   Translate    |     да      | Описание медитации                             |
| image          |      File      |     да      | изображение медитации                          |
| TypeMeditation | TypeMeditation |     да      | Тип медитации                                  |
| audio          |      file      |     да      | Аудио запись медитации                         |
| isSubscribe    |    boolean     |     нет     | Чтобы прослушать медитацию необходима подписка |

**или**
В данном случае данные будут загружены и привязанные к определенной медитации

*Параметры*

| Параметр                 | Обязательно | Описание                                              |
|--------------------------|:-----------:|:------------------------------------------------------|
| /<meditation_id: string> |     да      | В какой медитации будет привязанная данная информация |

*Тело*:

| Название                                                                      |    Тип    | Обязательно | Описание               |
|-------------------------------------------------------------------------------|:---------:|:-----------:|:-----------------------|
| name                                                                          | Translate |     да      | Название медитации     |
| description                                                                   | Translate |     да      | Описание медитации     |
| audio_language, где language - дву символьное обозначения естественного языка |   file    |     да      | Аудио запись медитации |


- **PATCH** Требует авторизации. Требует права администратора.
    > Обновляет данные об медитации в системе, если он найден.  Данные принимаются в виде form-data


*Заголовок*

| Название      |     Тип      | Обязательно | Описание                       |
|---------------|:------------:|:-----------:|:-------------------------------|
| Authorization |    string    |     да      | Токен авторизации пользователя |

*Тело*:

| Название       |      Тип       | Обязательно | Описание                                       |
|----------------|:--------------:|:-----------:|:-----------------------------------------------|
| name           |   Translate    |     да      | Название медитации                             |
| description    |   Translate    |     да      | Описание медитации                             |
| image          |      File      |     да      | изображение медитации                          |
| TypeMeditation | TypeMeditation |     да      | Тип медитации                                  |
| isSubscribe    |    boolean     |     нет     | Чтобы прослушать медитацию необходима подписка |


### /meditation.audio
- **GET**. Не требует авторизации. Не требует права администратора.
    > Возвращает аудио запись конкретной медитации на конкретном языке.

*Заголовок*

| Название        |  Тип   | Обязательно | Описание                                                                                   |
|-----------------|:------:|:-----------:|:-------------------------------------------------------------------------------------------|
| Authorization   | string |     нет     | Токен авторизации пользователя                                                             |
| Accept-Language | string |     да      | Дву символьное обозначения естественного языка на котором вернуть информацию об медитациях |

*Параметры*

| Параметр                                        | Обязательно | Описание                                                                                                                      |
|-------------------------------------------------|:-----------:|:------------------------------------------------------------------------------------------------------------------------------|
| /<meditation_id: string>                        |     нет     | Вернуть информацию по конкретной медитации, если meditation_id не задан вернет список пользователей                           |
