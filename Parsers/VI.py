import time
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet
import random


class ParserVI():

    def __init__(self):
        self.xpathComment = '//span[contains(text(), "Мнение о товаре")]/../../..'
        self.xpathPerfecto = '//span[contains(text(), "Достоинства")]/../../..'
        self.xpathNG = '//span[contains(text(), "Недостатки")]/../../..'
        self.xpathStars = "//div[@class = 'stars']/div[5]"
        self.xpatName = '//span[contains(text(), "Имя")]/../../..'
        self.xpatEmail = '//span[contains(text(), "E-mail")]/../../..'
        self.button = '//span[contains(text(), "Отправить отзыв")]/..'

    def parser_page(self, url="https://petrovich.ru/product/1022102/#reviews", text="") -> None:
        driver = Driver_Chrom().loadChromTest(headless=False)
        driver.get(url)
        time.sleep(20)

        name = self.generate_russian_name()
        email = self.generate_random_email()

        email_field = driver.find_element(By.XPATH, self.xpatEmail)
        name_field = driver.find_element(By.XPATH, self.xpatName)
        comment_field = driver.find_element(By.XPATH, self.xpathComment)
        time.sleep(3)

        comment_field.send_keys(text)
        name_field.send_keys(name)
        email_field.send_keys(email)
        stars = driver.find_elements(By.XPATH, self.xpathStars)

        for star in stars:
            star.click()
            time.sleep(1)
        button = driver.find_element(By.XPATH, self.button)
        button.click()
        time.sleep(5)

    def generate_word(self):
        # Списки популярных слов для большей реалистичности
        adjectives = ["quick", "lazy", "sleepy", "noisy", "hungry", "happy", "sad", "bright", "dark", "silent"]
        nouns = ["fox", "dog", "cat", "mouse", "bear", "lion", "tiger", "wolf", "rabbit", "squirrel"]
        return random.choice(adjectives) + random.choice(nouns)

    def generate_random_email(self):
        domains = ["gmail.com", "mail.ru", "yandex.ru"]
        word = self.generate_word()
        number = random.randint(0, 99)
        domain = random.choice(domains)

        email = f"{word}{number}@{domain}"
        return email

    def generate_russian_name(self):
        first_names_male = [
            "Александр", "Сергей", "Дмитрий", "Андрей", "Алексей", "Иван", "Михаил", "Николай", "Евгений", "Владимир",
            "Павел", "Роман", "Юрий", "Виктор", "Олег", "Игорь", "Максим", "Владислав", "Георгий", "Анатолий"
        ]
        first_names_female = [
            "Анна", "Мария", "Екатерина", "Ольга", "Наталья", "Елена", "Ирина", "Татьяна", "Юлия", "Алина",
            "Светлана", "Ксения", "Валерия", "Дарья", "Полина", "Александра", "Вера", "Любовь", "Людмила", "Алёна"
        ]

        gender = random.choice(['male', 'female'])

        if gender == 'male':
            return random.choice(first_names_male)
        else:
            return random.choice(first_names_female)

    def main(self):
        responce = GoogleSheet().get_current_orders()
        for i in range(2, len(responce["responce2"]["values"])):
            url = responce["responce1"]['values'][0][2]
            text = responce["responce2"]['values'][i][1]

            self.parser_page(url, text)


if __name__ == "__main__":

    ParserVI().parser_page()
