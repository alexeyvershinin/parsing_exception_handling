import fake_useragent
import requests
from bs4 import BeautifulSoup
import time


def test_request(url, retry=5):
    """
    Функцию обрабатывает ошибки при парсинге сайтов
    :param url: str
    :param retry: int
    :return:
    """
    ua = fake_useragent.UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    try:
        # выводим в консоль url и status_code
        response = requests.get(url=url, headers=headers)
        print(f"[+] {url} {response.status_code}")
    except Exception as ex:
        time.sleep(3)
        if retry:
            # выводим в консоль оставшееся количество попыток и url с которым возникла проблема
            print(f"[INFO] retry={retry} => {url}")
            return test_request(url, retry=(retry - 1))
        else:
            raise
    else:
        return response


def main():
    # читаем файл с url
    with open("books_urls.txt") as file:
        books_urls = file.read().splitlines()
    # для каждого url вызываем функцию тестирования
    for book_url in books_urls:
        try:
            r = test_request(url=book_url)
            # получим и выведем в консоль заголовок страницы
            soup = BeautifulSoup(r.text, "lxml")
            print(f"{soup.title.text}\n{'-' * 20}")
        except Exception as ex:
            continue


if __name__ == "__main__":
    main()

