import random
import time
import string
import time
import os
import requests
from selenium.webdriver.common.by import By
from browser import Driver_Chrom
from push_to_google_sheets import GoogleSheet
import random
import schedule
from other import create_dicts
import pyautogui as pyautogui
from browser import Driver_Chrom
import keyboard
import time

class ParserLerua:

    def __init__(self):
        self.xpathReviewBotten = "//span[contains(text(), 'Отзывы')]"
        self.xpathSendBotten = "//span[contains(text(), 'Отправить')]"

        self.xpath_write_review_botten = "//span[contains(text(), 'Написать отзыв')]"
        self.xpath_total_score = "//div[@data-qa = 'rating-form-total-score_mf-pdp']/div/label[5]"
        self.xpath_price = "//div[@data-qa = 'rating-form-by-price-score_mf-pdp']/div/label[5]"
        self.xpath_quality = "//div[@data-qa = 'rating-form-by-quality-score_mf-pdp']/div/label[5]"
        self.xpath_review = "//div[@data-testid= 'wrapperTextareaTestId']/textarea"
        # self.xpath_review = "//span[@data-testid='radio-label'][3;4;5]"
        self.xpatName = "//h3[contains(text(), 'Ваши данные')]//following::div[1]/div/div/input"
        self.xpatEmail = "//h3[contains(text(), 'Ваши данные')]//following::div[1]//following::div[1]/div/div/input"
        self.spreadsheet_id = "1vjDNkkWOjRpg88Uu4Cr2X_LR8BNgodFw9HPxtFhStfQ"
        self.API = 'https://www.1secmail.com/api/v1/'
        self.domain_list = ["1secmail.com", "1secmail.org", "1secmail.net"]
        self.domain = random.choice(self.domain_list)

    def switch_language(self):
        # Задержка для плавного переключения
        time.sleep(1)

        # Симуляция нажатия Command + Space (или Control + Space)
        pyautogui.hotkey('command', 'space')

    def filter_bmp_characters(self, text):
        return ''.join(c for c in text if ord(c) <= 0xFFFF)

    def parser_page(self, text="", url="") -> None:
        driver = Driver_Chrom().loadChromTest(headless=False)
        driver.get(url)
        time.sleep(3)
        self.payload(text)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)
        try:
            name = self.filter_bmp_characters(self.generate_russian_name())
            username = self.generate_username()
            email = f'{username}@{self.domain}'
            reviewBotten = driver.find_element(By.XPATH, self.xpathReviewBotten)
            reviewBotten.click()
            time.sleep(2)
            write_review_botten = driver.find_element(By.XPATH, self.xpath_write_review_botten)
            write_review_botten.click()
            time.sleep(2)

            total_score_field = driver.find_element(By.XPATH, self.xpath_total_score)
            total_score_field.click()
            time.sleep(1)
            price_field = driver.find_element(By.XPATH, self.xpath_price)
            price_field.click()
            time.sleep(1)
            quality_field = driver.find_element(By.XPATH, self.xpath_quality)
            quality_field.click()
            time.sleep(1)
            comment_field = driver.find_elements(By.XPATH, self.xpath_review)[0]
            comment_field.send_keys(text)
            name_field = driver.find_element(By.XPATH, self.xpatName)
            name_field.send_keys(name)
            email_field = driver.find_element(By.XPATH, self.xpatEmail)
            email_field.send_keys(email)
            time.sleep(2)
            sendBotten = driver.find_element(By.XPATH, self.xpathSendBotten)
            sendBotten.click()
            time.sleep(7)


        except:
                return

    def generate_word(self):
        # Списки популярных слов для большей реалистичности
        adjectives = [
            "quick", "lazy", "sleepy", "noisy", "hungry", "happy", "sad", "bright", "dark", "silent",
            "brave", "clever", "gentle", "rough", "tiny", "huge", "fierce", "calm", "proud", "shy",
            "bored", "excited", "furious", "glad", "mad", "pleased", "relieved", "scared", "thrilled", "worried",
            "bashful", "cheerful", "delighted", "disgusted", "eager", "frightened", "grumpy", "hopeful", "jealous",
            "joyful",
            "lonely", "miserable", "optimistic", "pessimistic", "serene", "startled", "tense", "trusting", "upset",
            "weary",
            "zealous", "adorable", "adventurous", "aggressive", "alert", "ambitious", "annoyed", "anxious", "arrogant",
            "attentive",
            "beautiful", "bewildered", "blushing", "bored", "brave", "busy", "calm", "careful", "careless", "charming",
            "cheerful", "clumsy", "comfortable", "confused", "cooperative", "courageous", "cowardly", "crazy",
            "curious", "dangerous",
            "defeated", "defiant", "delightful", "determined", "diligent", "disgusted", "distinct", "doubtful", "eager",
            "efficient",
            "elegant", "embarrassed", "enchanting", "encouraging", "energetic", "enthusiastic", "envious", "evil",
            "exuberant", "fair",
            "faithful", "famous", "fancy", "fantastic", "fierce", "friendly", "funny", "gentle", "gifted", "glamorous",
            "gloomy", "graceful", "grateful", "grotesque", "grumpy", "handsome", "happy", "healthy", "helpful",
            "hilarious",
            "homeless", "hungry", "hurt", "important", "impossible", "innocent", "inquisitive", "jolly", "joyous",
            "kind",
            "lazy", "lively", "lonely", "lovely", "lucky", "magnificent", "mysterious", "nervous", "nice", "obedient",
            "obnoxious", "odd", "outrageous", "outstanding", "peaceful", "perfect", "pleasant", "poor", "powerful",
            "precious",
            "proud", "puzzled", "quaint", "real", "relieved", "repulsive", "rich", "scary", "selfish", "shiny",
            "shy", "silly", "sleepy", "smiling", "smoggy", "sore", "sparkling", "splendid", "spotless", "stormy",
            "strange", "stupid", "successful", "super", "talented", "tame", "tender", "tense", "terrible", "thankful",
            "thoughtful", "thoughtless", "tired", "tough", "troubled", "ugliest", "uninterested", "unsightly",
            "unusual", "victorious",
            "vivacious", "wandering", "weary", "wicked", "witty", "worried", "wrong", "youthful", "zealous", "zesty",
            "alluring", "bustling", "dazzling", "elated", "fantabulous", "gleaming", "harmonious", "inspirational",
            "jubilant", "kooky",
            "luminous", "melodic", "noble", "opulent", "picturesque", "quixotic", "resplendent", "serendipitous",
            "tranquil", "ubiquitous",
            "vibrant", "whimsical", "yummy", "zany", "admirable", "brisk", "chipper", "dainty", "effervescent",
            "felicitous",
            "giddy", "heartwarming", "idyllic", "jovial", "kindhearted", "lighthearted", "mirthful", "nonchalant",
            "optimistic", "peaceable",
            "quaint", "radiant", "sanguine", "thriving", "uplifting", "vivid", "winsome", "youthful", "zesty", "zippy",
            "animated", "buoyant", "charming", "delightful", "exuberant", "flamboyant", "graceful", "hilarious",
            "ingenious", "jolly"
        ]

        nouns = [
            "fox", "dog", "cat", "mouse", "bear", "lion", "tiger", "wolf", "rabbit", "squirrel",
            "ant", "bat", "beetle", "bison", "boar", "buffalo", "camel", "chameleon", "cheetah", "chimpanzee",
            "cougar", "coyote", "crab", "deer", "dolphin", "donkey", "eagle", "eel", "elephant", "elk",
            "ferret", "flamingo", "frog", "giraffe", "goat", "goose", "gorilla", "hamster", "hawk", "hedgehog",
            "hippopotamus", "hornet", "horse", "hyena", "jackal", "jaguar", "jellyfish", "kangaroo", "koala", "lemur",
            "leopard", "lynx", "macaw", "mandrill", "meerkat", "mink", "mole", "mongoose", "monkey", "moose",
            "narwhal", "newt", "octopus", "okapi", "opossum", "orangutan", "oryx", "ostrich", "otter", "owl",
            "panther", "parrot", "peacock", "pelican", "penguin", "pig", "platypus", "porcupine", "quail", "quokka",
            "rabbit", "raccoon", "ram", "raven", "reindeer", "rhinoceros", "rooster", "salamander", "seal", "shark",
            "sheep", "skunk", "sloth", "snail", "snake", "sparrow", "spider", "squid", "stork", "swan",
            "tapir", "tarsier", "termite", "toad", "turkey", "turtle", "viper", "vulture", "wallaby", "walrus",
            "warthog", "weasel", "whale", "wolverine", "wombat", "woodpecker", "yak", "zebra", "baboon", "beaver",
            "bobcat", "caribou", "cassowary", "caterpillar", "cockatoo", "cougar", "crane", "crow", "cuckoo", "dingo",
            "dodo", "duck", "emu", "ermine", "falcon", "finch", "firefly", "gazelle", "gerbil", "gibbon",
            "gnu", "goose", "guinea pig", "heron", "hummingbird", "ibis", "iguana", "impala", "jackrabbit", "kudu",
            "lemur", "lizard", "locust", "loon", "loris", "macaque", "marmot", "mole", "moth", "myna",
            "ocelot", "orca", "parakeet", "peafowl", "pelican", "penguin", "pheasant", "piglet", "pigeon", "pony",
            "puma", "python", "quoll", "rat", "reptile", "rook", "sardine", "scorpion", "serval", "shearwater",
            "shrew", "shrike", "silkworm", "sparrow", "squid", "starling", "stingray", "stoat", "swallow", "swift",
            "tenrec", "tern", "titmouse", "toucan", "troodon", "vicuna", "vole", "wasp", "weaver", "whippet",
            "wren", "yabby", "zebu", "zorilla", "alpaca", "barracuda", "basilisk", "bonobo", "bushbaby", "capuchin",
            "chinchilla", "coati", "cormorant", "dormouse", "echidna", "frigatebird", "gecko", "grackle", "harrier",
            "hoatzin",
            "ibex", "javelina", "kinkajou", "kiwi", "lemur", "llama", "lynx", "manatee", "mastiff", "mockingbird",
            "ocelot", "oryx", "panda", "peccary", "pronghorn", "puffin", "puku", "quagga", "quokka", "quetzal",
            "sable", "saiga", "sapsucker", "seagull", "sheldrake", "silverfish", "siskin", "snowy owl", "solenodon",
            "sparrowhawk",
            "tarantula", "tiger", "tortoise", "toucan", "treefrog", "trout", "uakari", "urial", "viper", "vole",
            "walrus", "weevil", "wombat", "woodcock", "woolly bear", "xerus", "yak", "yellowhammer", "zander", "zebu",
            "zebra finch", "zorilla", "aardvark", "abyssinian", "agouti", "akita", "albatross", "alligator", "anaconda",
            "anemone"
        ]

        return random.choice(adjectives) + random.choice(nouns)

    def generate_russian_name(self):
        first_names_male = [
            "Александр", "Сергей", "Дмитрий", "Андрей", "Алексей", "Иван", "Михаил", "Николай", "Евгений", "Владимир",
            "Павел", "Роман", "Юрий", "Виктор", "Олег", "Игорь", "Максим", "Владислав", "Георгий", "Анатолий",
            "Константин", "Аркадий", "Василий", "Григорий", "Степан", "Фёдор", "Ярослав", "Борис", "Леонид", "Эдуард",
            "Артем", "Вячеслав", "Геннадий", "Егор", "Руслан", "Петр", "Станислав", "Денис", "Тимофей", "Лев",
            "Антон", "Кирилл", "Виталий", "Илья", "Захар", "Валерий", "Арсений", "Никита", "Викентий", "Вадим",
            "Филипп", "Глеб", "Семен", "Ростислав", "Гавриил", "Тихон", "Даниил", "Лука", "Савелий", "Юлиан",
            "Родион", "Назар", "Игнатий", "Эмиль", "Савва", "Святослав", "Елисей", "Матвей", "Леонтий", "Платон",
            "Яков", "Марсель", "Афанасий", "Валентин", "Артур", "Гордей", "Макар", "Лаврентий", "Мирослав", "Прохор",
            "Ян", "Ефим", "Марат", "Тарас", "Сила", "Евсей", "Рустам", "Вениамин", "Герман", "Адриан",
            "Арсен", "Богдан", "Вильям", "Игнат", "Емельян", "Ермолай", "Мартин", "Самуил", "Фома", "Валерий",
            "Дамир", "Геннадий", "Альберт", "Бронислав", "Вилен", "Генрих", "Давид", "Иннокентий", "Ким", "Лазарь",
            "Моисей", "Петр", "Роберт", "Серафим", "Тимур", "Ульян", "Феликс", "Эдуард", "Юлий", "Яромир",
            "Альфред", "Василиск", "Гай", "Данила", "Ефрем", "Зиновий", "Ипполит", "Карл", "Леонард", "Мирон",
            "Нестор", "Остап", "Панкратий", "Ратибор", "Соломон", "Тимофей", "Феодор", "Харитон", "Эммануил",
            "Ювеналий",
            "Яромил", "Август", "Агафон", "Аким", "Альфред", "Боримир", "Велимир", "Галактион", "Евграф", "Захарий",
            "Изяслав", "Куприян", "Леокадий", "Мирослав", "Никифор", "Орест", "Порфирий", "Родион", "Святополк",
            "Трифон",
            "Устин", "Феоктист", "Христофор", "Эдгар", "Юстиниан", "Яромир", "Алексей", "Бажен", "Велеслав", "Геннадий",
            "Евдоким", "Захарий", "Измаил", "Касьян", "Леонард", "Мефодий", "Никодим", "Осип", "Прохор", "Родион",
            "Светозар", "Тимон", "Феоктист", "Харлампий", "Эльдар", "Юлий", "Яромир", "Андроник", "Боголеп", "Викентий",
            "Герасим", "Елисей", "Захар", "Игнат", "Каллистрат", "Лев", "Милан", "Никита", "Онисим", "Потап",
            "Ростислав", "Сильвестр", "Тихон", "Феофан", "Христофор", "Эммануил", "Юлиан", "Якуб", "Аверкий",
            "Болеслав",
            "Викторин", "Григорий", "Епифаний", "Зиновий", "Иван", "Климент", "Леон", "Марк", "Никандр", "Остромир",
            "Рюрик", "Спиридон", "Терентий", "Ферапонт", "Харитон", "Эдуард", "Юст", "Ярослав", "Адам", "Богдан",
            "Велимир", "Горислав", "Ефрем", "Иероним", "Константин", "Леон", "Мечислав", "Никифор", "Овидий",
            "Пантелеймон",
            "Селиван", "Тимур", "Фидель", "Хрисанф", "Эраст", "Ювеналий", "Ярослав", "Александр", "Бронислав",
            "Виталий",
            "Герман", "Ефрем", "Илиодор", "Лев", "Мирослав", "Никон", "Олег", "Платон", "Серафим", "Трофим",
            "Фока", "Харитон", "Эмиль", "Юрий", "Яромир", "Аввакум", "Бенедикт", "Виктор", "Герасим", "Елизар",
            "Игнатий", "Леон", "Мефодий", "Никодим", "Онуфрий", "Родион", "Сильван", "Тимофей", "Феодосий", "Харлампий",
            "Эльдар", "Юлиан", "Ян", "Агапит", "Валентин", "Гордий", "Евтихий", "Иосиф", "Леонард", "Милан",
            "Николай", "Осип", "Прохор", "Светозар", "Тит", "Фома", "Христофор", "Эммануил", "Юстиниан", "Ярослав",
            "Александр", "Борис", "Василий", "Геннадий", "Евгений", "Игорь", "Лазарь", "Мстислав", "Нестор", "Онуфрий",
            "Ростислав", "Савва", "Тимур", "Филипп", "Харлампий", "Эраст", "Юрий", "Яков", "Августин", "Болеслав",
            "Викентий", "Гедеон", "Евсей", "Илларион", "Леонтий", "Мартын", "Никифор", "Панкрат", "Светослав",
            "Тихомир",
            "Феофан", "Харитон", "Эльдар", "Юлиан", "Ян", "Андрон", "Богдан", "Владимир", "Григорий", "Елисей",
            "Исаак", "Леонард", "Мефодий", "Никодим", "Овидий", "Порфирий", "Севастьян", "Терентий", "Феоктист",
            "Харлампий",
            "Эдвард", "Юлиан", "Яромир", "Агей", "Валерий", "Гордей", "Епифаний", "Иосиф", "Леонид", "Милан",
            "Никита", "Остромир", "Роман", "Сила", "Тимон", "Федор", "Христофор", "Эмиль", "Юрий", "Ярослав"
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

    def schedule_tasks(self):
        # Очистка текущего расписания
        schedule.clear()

        # Определение времени запуска в пределах дня (10-15 раз)
        times_to_run = random.randint(4, 7)
        start_time = 570

        for _ in range(times_to_run):
            interval_minutes = random.randint(2, 10)
            start_time += interval_minutes

            # Конвертация в часы и минуты
            hours, minutes = divmod(start_time, 60)
            # Планирование задачи
            schedule.every().day.at(f'{hours:02}:{minutes:02}').do(self.main)
            print(f"Запланировано на {hours:02}:{minutes:02}")

    def run_scheduler(self):
        # Первичное расписание задач
        self.schedule_tasks()

        while True:
            # Проверка и выполнение запланированных задач
            schedule.run_pending()
            time.sleep(1)
            # Ежедневное обновление расписания в полночь
            if time.localtime().tm_hour == 0 and time.localtime().tm_min == 0:
                self.schedule_tasks()

    def generate_username(self):
        name = string.ascii_lowercase + string.digits
        username = ''.join(random.choice(name) for i in range(10))

        return username

    def check_mail(self, mail=''):
        req_link = f'{self.API}?action=getMessages&login={mail.split("@")[0]}&domain={mail.split("@")[1]}'
        r = requests.get(req_link).json()
        length = len(r)

        if length == 0:
            print('[INFO] На почте пока нет новых сообщений. Проверка происходит автоматически каждые 5 секунд!')
        else:
            id_list = []

            for i in r:
                for k, v in i.items():
                    if k == 'id':
                        id_list.append(v)

            print(f'[+] У вас {length} входящих! Почта обновляется автоматически каждые 5 секунд!')

            current_dir = os.getcwd()
            final_dir = os.path.join(current_dir, 'all_mails')

            if not os.path.exists(final_dir):
                os.makedirs(final_dir)

            for i in id_list:
                read_msg = f'{self.API}?action=readMessage&login={mail.split("@")[0]}&domain={mail.split("@")[1]}&id={i}'
                r = requests.get(read_msg).json()
                print(content)
                sender = r.get('from')
                subject = r.get('subject')
                date = r.get('date')
                content = r.get('textBody')

                mail_file_path = os.path.join(final_dir, f'{i}.txt')

                with open(mail_file_path, 'w') as file:
                    file.write(f'Sender: {sender}\nTo: {mail}\nSubject: {subject}\nDate: {date}\nContent: {content}')

    def delete_mail(self, mail=''):
        url = 'https://www.1secmail.com/mailbox'

        data = {
            'action': 'deleteMailbox',
            'login': mail.split('@')[0],
            'domain': mail.split('@')[1]
        }

        r = requests.post(url, data=data)
        print(f'[X] Почтовый адрес {mail} - удален!\n')

    def payload(self, text):
        # Эмулируем нажатие на адресную строку браузера
        # Сначала перемещаем мышь на координаты адресной строки
        pyautogui.moveTo(340, 40)  # Координаты адресной строки могут варьироваться

        # Нажимаем на адресную строку
        pyautogui.click()

        # Выделяем текущий адрес (Ctrl+A или Command+A на macOS)
        # pyautogui.hotkey('ctrl', 'a')  # для Windows/Linux
        pyautogui.hotkey('command', 'a')  # для macOS

        # Вводим новый URL
        pyautogui.typewrite("https://lemanapro.ru/product/drel-akkumulyatornaya-hammer-acd12cs-12v-1x15ach-li-ion-98268237/#reviews-form")

        # Нажимаем Enter для перехода
        pyautogui.press('enter')
        time.sleep(5)

    def main(self):
        responce = GoogleSheet().get_current_orders(spreadsheet_id=self.spreadsheet_id)

        items_list = create_dicts(["Код", "Модель", "Ссылка"], responce["responce1"]['values'])
        comments_list = create_dicts(["Код", "Отзыв", "Номер строки", "Использовано"], filter(lambda x: x[1] != "" and x[3] == 'FALSE', responce["responce2"]['values']))
        code = items_list[0]["Код"]
        url = items_list[0]["Ссылка"]
        comment = list(filter(lambda x: x["Код"] == code, comments_list))
        for item in items_list:
            code = item["Код"]
            url = item["Ссылка"]
            comment = list(filter(lambda x: x["Код"] == code, comments_list))
            print(comment)
            if len(comment) > 0:
                for item in comment:
                    text = self.filter_bmp_characters(item["Отзыв"])
                    row = item["Номер строки"]
                    self.parser_page(text, url)
                    GoogleSheet().get_update_values(self.spreadsheet_id, True, f'Отзывы!D{row}')


if __name__ == "__main__":
    ParserLerua().main()
    # ParserVI().run_scheduler()