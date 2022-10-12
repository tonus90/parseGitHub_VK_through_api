"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список
репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

"""

import requests
from pathlib import Path
import json



class ScrapRepos:
    def __init__(self, start_url, headers, s_path):
        self.start_url = start_url
        self.headers = headers
        self.s_path = s_path #прокинем юрл пользователя, юзер агент, путь сохранения json

    def _get_response(self):
        response = requests.get(self.start_url, headers=self.headers)
        return response #получим ответ

    def _parse(self):
        data = self._get_response().json()
        return data #ответ превратим в dict

    def go(self):
        for repo in self._parse(): 
            repo_path = self.s_path.joinpath(f'{repo["name"]}.json') #назовем json по имени репо
            self._save(repo_path, repo)  


    def _save(self, file_path:Path, data:dict):
        file_path.write_text(json.dumps(data)) #метод для сохранения






if __name__ == '__main__':

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
    url = f'https://api.github.com/users/luchanos/repos' #выберем пользователя luchanos и получим его репо через апи
    p = Path('repos_luchanos')
    p.mkdir()

    repos_saver = ScrapRepos(url, headers, p)
    repos_saver.go() #в итоге получим папку repos_luchanos с его репозиториями в виде json
