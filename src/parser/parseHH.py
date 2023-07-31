import csv
import time

from aiogram import Bot
from aiogram.types import CallbackQuery
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from src.configuration import conf


class ParseHH:
    def __init__(self, callback: CallbackQuery, name: str, price: int):
        self.callback = callback
        self.name = self.__refactor_name(name)
        self.price = price

    async def parse(self):
        bot: Bot = Bot(token=conf.bot.token)

        self.__create_csv()

        await bot.send_message(self.callback.from_user.id, text='Парсер запущен')

        user_agent = UserAgent()
        options = webdriver.FirefoxOptions()
        options.set_preference('general.useragent.override', user_agent.random)
        options.headless = True

        await bot.send_message(self.callback.from_user.id, text='Запуск селениума')
        driver = webdriver.Firefox(options=options)
        await bot.send_message(self.callback.from_user.id, text='Селениум запущен')

        try:
            url = await self.__get_url(0)
            driver.get(url=url)
            time.sleep(10)

            try:
                find_pages = driver.find_element(
                    By.CLASS_NAME, 'pager'
                ).find_elements(
                    By.CLASS_NAME, 'pager-item-not-in-short-range'
                )[-1].text

                pages = int(find_pages) - 1
            except Exception as _ex:
                pages = 1

            i = 0
            while True:
                await bot.send_message(self.callback.from_user.id,
                                       f'Парсится {i + 1}ая страница из {pages}')

                find_block = driver.find_elements(By.CLASS_NAME, 'vacancy-serp-item__layout')

                public_date_list = []
                count_link = 0
                await bot.send_message(self.callback.from_user.id,
                                       f'Собираю все даты размещения на странице, может занять какое-то время')
                while count_link <= len(find_block) - 1:
                    await bot.send_message(self.callback.from_user.id,
                                           f'Парсится {count_link + 1} ссылка из {len(find_block)}')
                    driver.get(url=url)

                    link_block = driver.find_elements(By.CLASS_NAME, 'serp-item__title')

                    find_links = link_block[count_link]

                    count_link += 1

                    url_company = find_links.get_attribute('href')

                    driver.get(url=url_company)

                    date = driver.find_element(By.CLASS_NAME, 'vacancy-creation-time-redesigned').text

                    public_date_list.append(date)

                await bot.send_message(self.callback.from_user.id,
                                       f'Сбор даты размещения завершен')
                count_list = 0
                for block in find_block:
                    await bot.send_message(self.callback.from_user.id,
                                           f'Собираю все остальные данные со страницы')
                    data = {
                        'price': None,
                        'company': None,
                        'name': None,
                        'public_date': None,
                    }

                    find_links = block.find_element(By.CLASS_NAME, 'serp-item__title')

                    name = find_links.text
                    price = block.find_element(By.CLASS_NAME, 'bloko-header-section-2').text
                    company_block = block.find_element(By.CLASS_NAME, 'vacancy-serp-item__info')
                    company_name = company_block.find_element(
                        By.CLASS_NAME, 'vacancy-serp-item__meta-info-company'
                    ).text
                    company_city = company_block.find_elements(
                        By.CLASS_NAME, 'bloko-text'
                    )[1].text

                    company = f'{company_name} {company_city}'

                    data['price'] = price
                    data['company'] = company
                    data['name'] = name
                    data['public_date'] = public_date_list[count_list]

                    count_list += 1

                    self.__save_csv(data)

                    await bot.send_message(
                        self.callback.from_user.id,
                        f'Цена: {data["price"]}\nКомпания: {data["company"]}\nНазвание: {data["name"]}\nДата размещения: {data["public_date"]}'
                    )

                if i + 1 == pages:
                    break
                else:
                    i += 1
                    url = await self.__get_url(i)
                    driver.get(url=url)

        except Exception as _ex:
            print(_ex)
        finally:
            driver.close()
            driver.quit()

        await bot.send_message(self.callback.from_user.id,
                               'Парсер завершен')

        return True

    async def __get_url(self, page):
        url = f'https://hh.ru/search/vacancy?search_field=name&enable_snippets=false&salary={str(self.price)}&only_with_salary=true&text={self.name}&no_magic=true&ored_clusters=true&page={str(page)}'
        return url

    @staticmethod
    def __refactor_name(url):
        name = url.replace(' ', '+')
        return name

    @staticmethod
    def __create_csv():
        with open('hh_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Вакансия', 'Дата размещения', 'Компания', 'Заработная плата'])

    @staticmethod
    def __save_csv(data):
        with open('hh_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    data['name'],
                    data['public_date'],
                    data['company'],
                    data['price'],
                ]
            )
