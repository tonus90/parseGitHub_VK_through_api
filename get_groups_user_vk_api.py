
"""
2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию.
Ответ сервера записать в файл.
Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide).
Сделайте запрос, чтобы получить список всех сообществ на которые вы подписаны.

"""

import requests
from pathlib import Path
import json
import token

class ScrapGroupsVk:
    params = {
        'user_id': 139099730, #id user
        'extended': 1,
        'v': 5.52,
        'access_token': token.token,
    } #параметры для вызова api

    def __init__(self, start_url, headers, s_path):
        self.start_url = start_url
        self.headers = headers
        self.s_path = s_path #url api, headers, папку куда будем сохранять

    def _get_response(self):
        response = requests.get(self.start_url, headers=self.headers, params=self.params)
        return response #получим ответ от сервера

    def _parse(self):
        data = self._get_response().json() #превратим ответ в dict
        print(data['response']['count'])
        groups = data['response']['items'] #вытащим группы в виде списка
        return groups

    def go(self):
        for group in self._parse(): #вытаскиваем по одной группе
            try:
                group_path = self.s_path.joinpath(f'{group["screen_name"]}.json') #создаем путь к файлу папка/название файла по screen name группы
                self._save(group_path, group) #сохраняем по пути в виде json словарь с группой
            except UnicodeEncodeError as err:
                print(err)
                pass

    def _save(self, file_path:Path, data:dict): #метод для сохранения
        file_path.write_text(json.dumps(data, ensure_ascii=False))

if __name__ == '__main__':

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
    url = 'https://api.vk.com/method/groups.get'
    p = Path('vk_user_groups')
    p.mkdir() #создадим папку

    groups_saver = ScrapGroupsVk(url, headers, p) #объект
    groups_saver.go() #запускаем методом go и получим папку с сохраненными группами данного пользователя, каждая группа - отдельный json






