from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import csv
import time

# Настройки для Chrome
options = Options()
options.add_argument('start-maximized')

# Инициализация драйвера
try:
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.wildberries.ru/")
except Exception as e:
    print(f"Ошибка при инициализации драйвера: {e}")
    exit()

# Ожидание загрузки главной страницы
time.sleep(2)

# Поиск поля ввода и выполнение поиска
try:
    search_input = driver.find_element(By.ID, "searchInput")
    search_input.send_keys("Камеры видеонаблюдения")
    search_input.send_keys(Keys.ENTER)
except Exception as e:
    print(f"Ошибка при поиске: {e}")
    driver.quit()
    exit()

# Сбор карточек товаров
products = []
previous_count = 0

while True:
    try:
        wait = WebDriverWait(driver, 30)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@id]")))

        # Если количество карточек не изменилось, выходим из цикла
        current_count = len(cards)
        if current_count == previous_count:
            break
        previous_count = current_count
        print(len(cards))

        # Прокрутка страницы вниз
        driver.execute_script("window.scrollBy(0, 2000)")
        time.sleep(1)
    except Exception as e:
        print(f"Ошибка при сборе карточек: {e}")
        break

# Получение HTML-кода страницы
try:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение данных о товарах
    for product in soup.find_all(class_='product-card'):
        try:
            name = product.find(class_='product-card__name').text.strip()

            # Извлечение цен со скидкой
            price_container = product.find(class_='product-card__price price')
            price_with_discount = price_container.find('ins', class_='price__lower-price').text.strip() if price_container.find('ins', class_='price__lower-price') else "Нет скидки"

            # Получение URL товара
            link = product.find('a', class_='product-card__link')
            url = link['href'] if link else "Нет URL"

            products.append({
                "product_name": name,
                "price_with_discount": price_with_discount,
                "url": url
            })
            print(name, price_with_discount, url)
        except Exception as e:
            print(f"Ошибка при извлечении данных о товаре: {e}")
except Exception as e:
    print(f"Ошибка при парсинге страницы: {e}")

# Сохранение данных в JSON
try:
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
except Exception as e:
    print(f"Ошибка при сохранении данных в JSON: {e}")

# Сохранение данных в CSV
try:
    with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product_name','price_with_discount', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for product in products:
            writer.writerow(product)
except Exception as e:
    print(f"Ошибка при сохранении данных в CSV: {e}")

# Закрытие драйвера
try:
    driver.quit()
except Exception as e:
    print(f"Ошибка при закрытии драйвера: {e}")










