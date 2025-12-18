# tesera_bgg_ratings_scroll.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import json
import time
import re

def parse_tesera_bgg_ratings_with_scroll():
    print('🎮 Запускаем парсинг рейтингов BGG с автопрокруткой...')
    
    username = "Maksimuz"
    print(f'👤 Парсим рейтинги BGG для коллекции пользователя: {username}')
    
    # Настройки Chrome - БЕЗ headless для отладки
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # ЗАКОММЕНТИРУЕМ ДЛЯ ОТЛАДКИ
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
        
        # Ждем появления игр и фильтров
        wait = WebDriverWait(driver, 15)
        
        try:
            game_items = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.c_game_item'))
            )
            print(f'✅ Найдено игр на первой странице: {len(game_items)}')
        except:
            print('❌ Игры не найдены')
            return {}
        
        # МЕНЯЕМ СОРТИРОВКУ НА "РЕЙТИНГУ BGG"
        print('🔄 Меняем сортировку на "Рейтингу BGG"...')
        try:
            # Находим селектор сортировки
            sort_select = Select(driver.find_element(By.ID, 'f-sort'))
            # Выбираем "Рейтингу BGG"
            sort_select.select_by_value('ratinggeekbgg')
            print('✅ Сортировка изменена на "Рейтингу BGG"')
            
            # Ждем перезагрузки страницы с рейтингами
            time.sleep(5)
            
            # Проверяем, что рейтинги появились
            rating_elements = driver.find_elements(By.CSS_SELECTOR, '.c_game_rating_2 span')
            print(f'✅ Найдено игр с рейтингами BGG: {len(rating_elements)}')
            
        except Exception as e:
            print(f'❌ Не удалось изменить сортировку: {e}')
            return {}
        
        # ЗАГРУЖАЕМ ВСЕ ИГРЫ ЧЕРЕЗ АВТОПРОКРУТКУ
        print('🔄 Загружаем все игры через автопрокрутку...')
        max_scroll_attempts = 20
        previous_count = 0
        current_count = len(driver.find_elements(By.CSS_SELECTOR, '.c_game_item'))
        
        for attempt in range(max_scroll_attempts):
            print(f'📊 Попытка {attempt + 1}: сейчас {current_count} игр')
            
            if current_count == previous_count:
                print('✅ Количество игр не изменилось - все загружены')
                break
                
            previous_count = current_count
            
            # Прокручиваем до конца страницы
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Пробуем найти и нажать кнопку "Загрузить ещё" если есть
            try:
                load_more_buttons = driver.find_elements(By.XPATH, 
                    '//a[contains(text(), "Загрузить ещё") or contains(text(), "Load more")]')
                
                if load_more_buttons:
                    print(f'📥 Найдена кнопка "Загрузить ещё", нажимаем...')
                    driver.execute_script("arguments[0].click();", load_more_buttons[0])
                    time.sleep(3)
            except:
                pass
            
            # Обновляем счетчик
            current_count = len(driver.find_elements(By.CSS_SELECTOR, '.c_game_item'))
            
            # Если достигли максимума (240 игр), выходим
            if current_count >= 240:
                print('✅ Достигнуто максимальное количество игр (240)')
                break
        
        # ФИНАЛЬНЫЙ СБОР ДАННЫХ
        print('📦 Финальный сбор рейтингов BGG...')
        all_game_elements = driver.find_elements(By.CSS_SELECTOR, '.c_game_item')
        print(f'🎯 ВСЕГО игр после прокрутки: {len(all_game_elements)}')
        
        bgg_ratings = {}
        
        for i, item in enumerate(all_game_elements):
            try:
                # Извлекаем ПОЛНОЕ название из атрибута title
                title_elem = item.find_element(By.CSS_SELECTOR, '.c_game_title a')
                game_name = title_elem.get_attribute('title')
                
                # Если title пустой, берем из text
                if not game_name:
                    game_name = title_elem.text.strip()
                
                # Извлекаем рейтинг BGG
                rating_elem = item.find_element(By.CSS_SELECTOR, '.c_game_rating_2 span')
                rating_text = rating_elem.text.strip()
                
                # Парсим числовой рейтинг
                bgg_rating = None
                try:
                    bgg_rating = float(rating_text)
                except ValueError:
                    match = re.search(r'(\d+\.\d+|\d+)', rating_text)
                    if match:
                        bgg_rating = float(match.group(1))
                
                if bgg_rating:
                    bgg_ratings[game_name] = bgg_rating
                    if i < 5 or i >= len(all_game_elements) - 5:
                        print(f'   ✅ {i+1}. {game_name}: {bgg_rating}')
                else:
                    print(f'   ❌ {i+1}. {game_name}: рейтинг не распознан')
                    bgg_ratings[game_name] = None
                
            except Exception as e:
                print(f'   ⚠️ Ошибка парсинга игры {i+1}: {e}')
                continue
        
        print(f'📊 Успешно спарсено рейтингов: {len([r for r in bgg_ratings.values() if r is not None])}')
        print(f'❌ Игр без рейтинга: {len([r for r in bgg_ratings.values() if r is None])}')
        
        # Закрываем браузер
        driver.quit()
        
        return bgg_ratings
        
    except Exception as e:
        print(f'❌ Критическая ошибка: {e}')
        if driver:
            driver.quit()
        return {}

def save_ratings_to_json(ratings):
    """Сохраняем рейтинги в JSON файл"""
    output_file = 'bgg_ratings_complete.json'
    
    # Разделяем игры с рейтингом и без
    games_with_rating = {k: v for k, v in ratings.items() if v is not None}
    games_without_rating = {k: v for k, v in ratings.items() if v is None}
    
    # Сортируем по рейтингу (от высшего к низшему)
    sorted_with_rating = dict(sorted(
        games_with_rating.items(),
        key=lambda x: x[1],
        reverse=True
    ))
    
    # Объединяем
    final_ratings = {**sorted_with_rating, **games_without_rating}
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_ratings, f, ensure_ascii=False, indent=2, sort_keys=False)
    
    print(f'💾 Рейтинги сохранены в: {output_file}')
    return output_file

def main():
    print('🚀 Запуск парсера рейтингов BGG с автопрокруткой')
    print('=' * 60)
    
    start_time = time.time()
    bgg_ratings = parse_tesera_bgg_ratings_with_scroll()
    end_time = time.time()
    
    print('=' * 60)
    
    if bgg_ratings:
        output_file = save_ratings_to_json(bgg_ratings)
        
        # Статистика
        games_with_rating = len([r for r in bgg_ratings.values() if r is not None])
        total_games = len(bgg_ratings)
        
        print(f'📈 Статистика:')
        print(f'   Всего игр: {total_games}')
        print(f'   С рейтингом BGG: {games_with_rating}')
        print(f'   Без рейтинга: {total_games - games_with_rating}')
        if total_games > 0:
            print(f'   Процент покрытия: {(games_with_rating/total_games)*100:.1f}%')
        
        # Топ-10 игр по рейтингу
        top_games = [(k, v) for k, v in bgg_ratings.items() if v is not None]
        top_games.sort(key=lambda x: x[1], reverse=True)
        
        if top_games:
            print(f'🏆 Топ-10 игр по рейтингу BGG:')
            for i, (game, rating) in enumerate(top_games[:10]):
                print(f'   {i+1}. {game}: {rating}')
        
        print(f'⏱ Затрачено времени: {round(end_time - start_time, 2)} секунд')
        print(f'💾 Файл для использования: {output_file}')
        
    else:
        print('❌ Не удалось получить рейтинги')

if __name__ == '__main__':
    main()