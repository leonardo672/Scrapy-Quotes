# Анализ проекта: Quotes Scraper

## Обзор
Этот проект включает создание веб-скребка с использованием фреймворка Scrapy для сбора данных с сайта [quotes.toscrape.com](http://quotes.toscrape.com). Собранные данные включают цитаты, авторов и теги с нескольких страниц и сохраняются в файле JSON для анализа или других случаев использования.
## 1. Шаги, предпринятые в проекте (Что было сделано)
#### 1.1 Установка Python и PyCharm: Python был установлен на системе, а также среда разработки PyCharm для разработки проекта Scrapy.
#### 1.2 Создание нового проекта: В PyCharm был создан новый проект с именем quotes_scraper, в котором автоматически была настроена новая виртуальная среда.

### ![Screenshot (2191)](https://github.com/user-attachments/assets/7704cd0f-b605-4127-b29c-25af2974ddf0)

#### 1.3 Активация виртуальной среды: Виртуальная среда была активирована с помощью команды:
##### 
    .\Scripts\activate
##### (Эта команда предназначена для пользователей Windows.)
#### 1.4 Установка Scrapy: Scrapy был установлен, выполнив следующую команду:
##### 
    pip install scrapy
#### 1.5 Создание проекта Scrapy: Новый проект Scrapy был создан с помощью команды:
##### 
    scrapy startproject quotes_scraper
#### 1.6 Определил целевые страницы паука, установив start_urls на главную страницу.
##### В классе QuotesSpider я указал начальный URL для парсинга цитат. Это начальная страница сайта, с которой начинается сбор данных.
##### start_urls = [
    'http://quotes.toscrape.com/page/1/',  
]
#### 1.7 Добавил код для разбора цитат, авторов и тегов, используя CSS селекторы внутри метода parse.
##### В методе parse я использовал CSS селекторы для извлечения текста цитаты, имени автора и связанных тегов из каждого элемента на странице. Данные собираются в виде словаря и передаются с помощью yield.
##### 
    def parse(self, response):
      # Парсинг цитат
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").get(),
                'author': quote.css("small.author::text").get(),
                'tags': quote.css("div.tags a.tag::text").getall(),
            }
#### 1.8 Настроил паука для обработки пагинации, идентифицируя и следуя за кнопкой "Следующая страница" на каждой странице.
##### Я добавил код, который проверяет наличие ссылки на следующую страницу и, если она существует, переходит по этой ссылке, продолжая парсинг.
#####
    next_page = response.css("li.next a::attr(href)").get()
##### if next_page is not None:
    yield response.follow(next_page, self.parse)
#### 1.9 Определение моделей для собираемых данных
##### В файле items.py я определил модель для собираемых элементов, создавая класс QuotesScraperItem, который структурирует данные:
##### 
    class QuotesScraperItem(scrapy.Item):
        Text = scrapy.Field()    # Поле для текста цитаты
        Author = scrapy.Field()  # Поле для имени автора
        Tags = scrapy.Field()     # Поле для тегов цитаты
#### 1.10 После завершения разработки паука, я запустил команду для выполнения скрипта и сбора данных:
##### 
    scrapy crawl quotes
##### Мы запускаем команду scrapy crawl quotes перед созданием файла Quotes_Items.json, чтобы инициировать процесс веб-скрейпинга. По умолчанию Scrapy не создает файлы вывода автоматически; вместо этого выполняется логика скрейпинга, определенная в пауке. Чтобы сохранить собранные данные в файл, можно добавить опцию вывода (например, -o Quotes_Items.json) при запуске команды. Таким образом, данные собираются и одновременно сохраняются в указанный JSON-файл. Без запуска команды паук не выполнит скрейпинг и не создаст файл с результатами.

#### 1.11 Хранение данных:
##### Указал формат вывода как JSON с помощью:
##### 
    scrapy crawl quotes -o Quotes_Items.json

#### 1.12 Создал дополнительные выходные файлы в формате XML и CSV для анализа, чтобы обеспечить гибкость в использовании:
##### 
    scrapy crawl quotes -o Quotes_Items.xml 
    scrapy crawl quotes -o Quotes_Items.csv

## 2. Источники данных (Откуда были получены данные)
Данные были получены с публичного сайта [quotes.toscrape.com](http://quotes.toscrape.com), который предоставляет примеры цитат для тестирования приложений веб-скребка. Сайт включает несколько страниц с текстами цитат, именами авторов и связанными тегами, что позволяет обрабатывать пагинацию и собирать данные.

## 3. Процесс сбора данных (Как осуществлялся сбор)
Данные были собраны с помощью:
Определения CSS селекторов: Использовались CSS селекторы для извлечения конкретных элементов, таких как цитаты (span.text), авторы (span.author) и теги (.tag). Каждая цитата сохранялась как элемент, содержащий эти поля.
Обработки пагинации: Паука следил за кнопкой "Следующая страница", извлекая ее ссылку и рекурсивно вызывая метод parse, пока все страницы не были собраны.
Каждая цитата с соответствующим автором и тегами возвращалась как словарь (элемент Scrapy) и сохранялась в указанные форматы.

## 4. Выбор методов/инструментов (Почему был выбран тот или иной метод/инструмент, а не другой)
Почему Scrapy?
Эффективность: Scrapy предназначен для веб-скребка и автоматизирует многие аспекты (запросы, ответы и хранение данных).
Встроенная пагинация: Легко обрабатывает многопагинаторные запросы, что является ключевым для этого проекта.
Опции экспорта данных: Позволяет сохранять данные непосредственно в формате JSON, что идеально подходит для анализа.
Почему CSS селекторы?
Простота: CSS селекторы интуитивно понятны для структуры HTML этого сайта.
Производительность: CSS селекторы, как правило, быстрее, чем XPath, что делает их идеальными, когда они могут достигать того же результата.

## Заключение
Этот проект на основе Scrapy успешно собрал цитаты, авторов и теги с нескольких страниц сайта, используя пагинацию для захвата всего контента. Выбор Scrapy и CSS селекторов был обусловлен необходимостью использования эффективного инструмента для скребка и простотой CSS селекторов для структуры сайта.


