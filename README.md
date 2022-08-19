# Публикация комиксов
Скрипт загружает в группу ВКонтакте случайный комикс, а также авторскую подпись к нему из [xkcd.com](https://xkcd.com/)

### Как установить

Для работы скрипта необходимо:
- [зарегистрировать группу](https://vk.com/groups?tab=admin) ВКонтакте
- [создать приложение](https://vk.com/editapp?act=create) ВКонтакте (тип приложения `standalone`) 
- добавить переменные окружения (или файл .env в корне скрипта):

  ACCESS_TOKEN - ключ доступа пользователя. Для его получения необходимо использоваать процедуру [Implicit Flow](https://dev.vk.com/api/access-token/implicit-flow-user) с настройками доступа для приложения `photos, groups, wall и offline`.
  
  GROUP_ID - идентификатор группы, в которую будет оптправлен комикс. Узнать group_id группы можно [здесь](https://regvk.com/id/).


Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```bash
pip install -r requirements.txt
```

### Как использовать

Запустить main.py:
```bash
>python main.py
```
Комикс будет загружен в группу.

![image](https://user-images.githubusercontent.com/107745329/185541654-771702ca-dff2-4cb6-aa29-60a052f91e47.png)


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
