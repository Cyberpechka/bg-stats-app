# tesera_parser_selenium.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import json
import time
import os
import re
from urllib.parse import urljoin
from datetime import datetime

def extract_year_from_text(text):
    """
    Извлекает год из текста вида 'Название игры, 2025'
    """
    if not text:
        return ''
    
    try:
        # Ищем 4-значное число (год) в конце строки или после запятой
        patterns = [
            r',\s*(\d{4})\s*$',           # , 2025 в конце
            r'\s+(\d{4})\s*$',            # пробел 2025 в конце
            r'\((\d{4})\)',               # (2025)
            r'\b(19|20)\d{2}\b',          # любое 4-значное число 19xx или 20xx
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.strip())
            if match:
                year = int(match.group(1))
                # Проверяем что это валидный год (1900-текущий год + 5)
                current_year = datetime.now().year
                if 1900 <= year <= current_year + 5:
                    return str(year)
        
        return ''
        
    except Exception as e:
        print(f'   ⚠️ Ошибка извлечения года из "{text}": {e}')
        return ''

def parse_tesera_collection():
    print('🎮 Запускаем парсинг коллекции Tesera с Selenium...')
    
    # Жестко задаем имя пользователя
    username = "Maksimuz"
    print(f'👤 Парсим коллекцию пользователя: {username}')
    
    # Настройки Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Фоновый режим
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = None
    try:
        # Запускаем браузер
        print('🚀 Запускаем Chrome браузер...')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f'https://tesera.ru/user/{username}/games/owns/')
        
        print('⏳ Ждем загрузки игр...')
        
        # Ждем появления игр (до 15 секунд)
        wait = WebDriverWait(driver, 15)
        
        try:
            # Ждем появления хотя бы одной игры
            game_items = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.c_game_item'))
            )
            print(f'✅ Найдено игр на первой странице: {len(game_items)}')
        except:
            print('❌ Игры не найдены, пробуем альтернативный селектор...')
            # Пробуем другой селектор
            game_items = driver.find_elements(By.CSS_SELECTOR, '[class*="game"]')
            print(f'🔍 Альтернативных элементов найдено: {len(game_items)}')
        
        # Пробуем загрузить ВСЕ игры через многократную прокрутку
        print('🔄 Пробуем загрузить все игры...')
        max_attempts = 10  # Максимум 10 попыток (до 300 игр)
        previous_count = len(game_items)
        
        for attempt in range(max_attempts):
            try:
                # Ищем кнопку "Загрузить ещё"
                load_more_selector = '#collection-own-pages a, .feed_pages a, a[onclick*="pageNextLoad"], a[onclick*="apiListOwn"]'
                load_more_buttons = driver.find_elements(By.CSS_SELECTOR, load_more_selector)
                
                load_more_button = None
                for button in load_more_buttons:
                    if 'Загрузить ещё' in button.text or 'Load more' in button.text:
                        load_more_button = button
                        break
                
                if load_more_button:
                    print(f'📥 Попытка {attempt + 1}: Нажимаем "Загрузить ещё"...')
                    
                    # Прокручиваем к кнопке и кликаем
                    driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", load_more_button)
                    
                    # Ждем загрузки новых игр
                    time.sleep(3)
                    
                    # Проверяем, добавились ли новые игры
                    current_items = driver.find_elements(By.CSS_SELECTOR, '.c_game_item')
                    print(f'   📊 Сейчас игр: {len(current_items)}')
                    
                    # Если количество не изменилось, выходим
                    if len(current_items) <= previous_count:
                        print('   ✅ Все игры загружены')
                        break
                    
                    previous_count = len(current_items)
                    game_items = current_items
                    
                else:
                    print('   ✅ Кнопка "Загрузить ещё" не найдена - все игры загружены')
                    break
                    
            except Exception as e:
                print(f'   ❌ Ошибка при загрузке: {e}')
                break
        
        # После загрузки всех игр, собираем полный список
        print('📦 Собираем полный список игр...')
        all_game_elements = driver.find_elements(By.CSS_SELECTOR, '.c_game_item')
        print(f'🎯 Всего игр загружено: {len(all_game_elements)}')
        
        all_games_basic = []
        for i, item in enumerate(all_game_elements):
            try:
                title_elem = item.find_element(By.CSS_SELECTOR, '.c_game_title a')
                img_elem = item.find_element(By.CSS_SELECTOR, '.c_game_img2')
                
                game = {
                    'name': title_elem.text.strip(),
                    'url': title_elem.get_attribute('href'),
                    'imageUrl': img_elem.get_attribute('src'),
                    'addedDate': item.get_attribute('data-cdate') or ''
                }
                
                # Пробуем найти рейтинг
                try:
                    rating_elem = item.find_element(By.CSS_SELECTOR, '.c_game_rating span')
                    game['personalRating'] = rating_elem.text.strip()
                except:
                    game['personalRating'] = None
                
                all_games_basic.append(game)
                if i < 5 or i >= len(all_game_elements) - 5:  # Показываем первые и последние 5
                    print(f'   🎯 {i+1}. {game["name"]}')
                elif i == 5:
                    print(f'   ... и еще {len(all_game_elements) - 10} игр ...')
                
            except Exception as e:
                print(f'   ❌ Ошибка парсинга игры {i+1}: {e}')
                continue
        
        print(f'🎯 Всего игр в коллекции: {len(all_games_basic)}')
        
        if not all_games_basic:
            print('❌ Игры не найдены. Сохраняем HTML для диагностики...')
            with open('tesera_debug.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print('💾 HTML сохранен в tesera_debug.html')
        
        # Закрываем браузер
        driver.quit()
        
        if not all_games_basic:
            return []
        
        # Теперь парсим детальную информацию обычными запросами
        print('🔍 Парсим детальную информацию для каждой игры...')
        detailed_games = []
        
        for i, game in enumerate(all_games_basic):
            print(f'📖 [{i+1}/{len(all_games_basic)}] Детали: {game["name"]}')
            
            try:
                session = requests.Session()
                session.headers.update({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                game_url = game['url']
                if not game_url.startswith('http'):
                    game_url = urljoin('https://tesera.ru', game_url)
                
                game_response = session.get(game_url)
                game_response.raise_for_status()
                
                game_soup = BeautifulSoup(game_response.text, 'html.parser')
                
                # Основная информация
                name = game_soup.select_one('h1 span[itemprop="name"]')
                name = name.text.strip() if name else game['name']
                
                # Год издания - ИСПРАВЛЕННЫЙ ПАРСИНГ
                year = ''
                # Ищем второй h1 (обычно там год)
                h1_elements = game_soup.find_all('h1')
                if len(h1_elements) > 1:
                    year_text = h1_elements[1].get_text().strip()
                    year = extract_year_from_text(year_text)
                    print(f'   📅 Найден текст: "{year_text}" -> Год: {year}')
                
                # Если не нашли во втором h1, ищем в других местах
                if not year:
                    # Ищем в мета-тегах
                    year_meta = game_soup.select_one('meta[itemprop="datePublished"]')
                    if year_meta:
                        year_text = year_meta.get('content', '')
                        year = extract_year_from_text(year_text)
                
                # Игроки
                players_meta = game_soup.select_one('meta[itemprop="numberOfPlayers"]')
                players = players_meta['content'] if players_meta else ''
                
                # Время партии
                time_li = game_soup.find('li', string=lambda x: x and 'мин' in str(x))
                duration = time_li.text.strip() if time_li else ''
                
                # Возраст
                age_li = game_soup.find('li', string=lambda x: x and 'лет' in str(x))
                age = age_li.text.strip() if age_li else ''
                
                # Рейтинг
                rating_elem = game_soup.select_one('.bigrating')
                rating = rating_elem.text.strip() if rating_elem else ''
                
                # Авторы
                authors = []
                author_elem = game_soup.find('td', string='автор:')
                if author_elem:
                    author_links = author_elem.find_next_sibling('td').select('a')
                    authors = [a.text.strip() for a in author_links]
                
                # Издатели
                publishers = []
                publisher_elem = game_soup.find('td', string='издатель:')
                if publisher_elem:
                    publisher_links = publisher_elem.find_next_sibling('td').select('a')
                    publishers = [a.text.strip() for a in publisher_links]
                
                game_details = {
                    'id': i + 1,
                    'name': name,
                    'players': players,
                    'duration': duration,
                    'year': year,
                    'age': age,
                    'rating': rating,
                    'authors': authors,
                    'publishers': publishers,
                    'teseraUrl': game_url,
                    'teseraId': game_url.split('/')[-2] if '/' in game_url else '',
                    'parsedAt': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Объединяем информацию
                full_game_info = {**game, **game_details}
                detailed_games.append(full_game_info)
                
                print(f'   ✅ Игроки: {players}, Время: {duration}, Год: {year}')
                
            except Exception as e:
                print(f'   ❌ Ошибка: {e}')
                game['id'] = i + 1
                detailed_games.append(game)
            
            # Задержка между запросами
            time.sleep(1)
            
            # Сохраняем промежуточный результат каждые 10 игр
            if (i + 1) % 10 == 0:
                print(f'💾 Сохраняем промежуточный результат после {i + 1} игр...')
                with open(f'tesera_partial_{i+1}.json', 'w', encoding='utf-8') as f:
                    json.dump(detailed_games, f, ensure_ascii=False, indent=2)
        
        # Сохраняем финальный результат
        output_file = 'tesera_complete_collection.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(detailed_games, f, ensure_ascii=False, indent=2)
        
        print(f'\n🎉 ПАРСИНГ ЗАВЕРШЕН!')
        print(f'📊 Обработано игр: {len(detailed_games)}')
        print(f'💾 Результат сохранен в: {output_file}')
        
        return detailed_games
        
    except Exception as e:
        print(f'❌ Критическая ошибка: {e}')
        if driver:
            driver.quit()
        return []

def main():
    print('🚀 Запуск парсера Tesera для пользователя Maksimuz')
    print('=' * 50)
    
    start_time = time.time()
    results = parse_tesera_collection()
    end_time = time.time()
    
    print('=' * 50)
    print(f'⏱ Затрачено времени: {round(end_time - start_time, 2)} секунд')
    print(f'📦 Получено игр: {len(results)}')
    
    if results:
        print('🎯 Пример первой игры:')
        first_game = results[0]
        print(f'   Название: {first_game.get("name")}')
        print(f'   Игроки: {first_game.get("players")}')
        print(f'   Время: {first_game.get("duration")}')
        print(f'   Год: {first_game.get("year")}')

if __name__ == '__main__':
    main()