import html
import asyncio, aiohttp
import re
import os


result_dict = {
}
pattern_re = r'<a\s+href="([^"]+)"\s+title="Категория:Животные по алфавиту">Следующая страница</a>'


async def find_link(session, base_url):
    """
    Асинхронная функция нахождения и преобразования ссылки на следующую страницу википедии
    """
    async with session.get(base_url) as response:
        text = await response.text()
        link_async = re.findall(pattern_re, text)
        full_link_async = html.unescape(f"https://ru.wikipedia.org{link_async[0]}")
        return full_link_async


async def path_link(session, link):
    """
    Асинхронная функция перехода по ссылке и поиска имен-ссылок на страницы с различными животными
    """
    async with session.get(link) as response:
        text = await response.text()
        lines_async = re.findall(r'<li><a href="/wiki.*', text)
        names_async = [re.findall(r'>([^<]+)<', line) for line in lines_async]
        return names_async


async def write_file(animals):
    """
    Асинхронная функция записи полученных данных в словарь
    """
    animals = list(map(lambda x: x[0], animals[1:])) + [animals[-2][0]]
    for animal in animals:
        if animal[0] not in result_dict:
            result_dict.setdefault(animal[0], 1)
        else:
            result_dict[animal[0]] += 1


async def all_links():
    """
    Основная асинхронная функция программы
    """
    async with aiohttp.ClientSession() as session:
        print(f'Выполняется асинхронный скрипт...')
        current_url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'  # дефолтный путь страницы на Вики
        first_page = True
        links = []
        step = 0

        async def path_write(url):
            """
            Для избежания дублирования кода, напишем дополнительную асинх.фунцию, вызывающую другие асинх.ф-ции
            """
            # Вызов асинхронной функции перехода на следующую страницу. Возвращаются найденные животные и сохр.в names
            names = await path_link(session=session, link=url)
            # Вызов функции записи в основной словарь
            await write_file(animals=names)

        while current_url:
            print(f'{step} страниц обработано')
            try:
                if first_page:  # Если первая страница раздела википедии - сразу вызываем вспомогательную асинх. ф-цию
                    await path_write(url=current_url)
                    first_page = False
                # Вызов асинхронной функции поиска ссылки на следующую страницу. Возвращается ссылка
                result_link = await find_link(session=session, base_url=current_url)
                # Вызов вспомогательной асинх. ф-ции
                await path_write(url=result_link)
                # Текущий путь (который кидаем в асинх. ф-цию на след итерации цикла) приравниваем к найденной ссылке
                current_url = result_link
            except IndexError:
                break
            else:
                step += 1

        print(f'ddd {links}')

if not os.path.isfile('beasts.csv'):
    asyncio.run(all_links())
    print(f'Скрипт выполнен! Искомый словарь: {result_dict}')
    result_dict = dict(sorted(result_dict.items()))

def make_file():
    with open('beasts.csv', 'w', encoding='utf-8') as beasts:
        for k, v in result_dict.items(): #добавить сортировку словаря и поставить тест на проверку наличия файла
            beasts.write(f'{k},{v}\n')
    print(f'Файл создан!')
    return True

def file_ok():
    return f'Файл уже создан'

assert os.path.isfile('beasts.csv') == False and make_file(), file_ok()