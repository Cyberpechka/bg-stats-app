# final_download.py
import requests
import json
import os
import time

def final_download():
    print("🎯 ПОСЛЕДНЯЯ ПОПЫТКА СКАЧАТЬ ИЗОБРАЖЕНИЯ...")
    
    with open('bg-stats-app/frontend/assets/data/tesera-collection.json', 'r', encoding='utf-8') as f:
        games = json.load(f)
    
    os.makedirs('bg-stats-app/frontend/assets/images/games', exist_ok=True)
    
    successful = 0
    failed = 0
    
    for i, game in enumerate(games):
        if game.get('imageUrl'):
            try:
                print(f'📥 {i+1}. {game["name"]}')
                
                # СУПЕР-ПРОСТОЙ запрос без лишних headers
                response = requests.get(game['imageUrl'], timeout=10)
                
                if response.status_code == 200 and len(response.content) > 10000:
                    filename = f"game_{game['id']}.jpg"
                    filepath = f"bg-stats-app/frontend/assets/images/games/{filename}"
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    game['imageUrl'] = f"assets/images/games/{filename}"
                    successful += 1
                    print(f'   ✅ Успешно: {len(response.content)} bytes')
                else:
                    game['imageUrl'] = ''
                    failed += 1
                    print(f'   ❌ Провал: статус {response.status_code} или мало данных')
                    
            except Exception as e:
                game['imageUrl'] = ''
                failed += 1
                print(f'   ❌ Ошибка: {e}')
        
        # Минимальная задержка
        time.sleep(0.3)
    
    # Сохраняем результат
    output_file = 'bg-stats-app/frontend/assets/data/tesera-collection-local.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(games, f, ensure_ascii=False, indent=2)
    
    print(f'\n🎯 ИТОГ: Успешно {successful}, Провалов {failed}')
    
    if successful < 50:  # Если скачалось меньше 50 изображений
        print('🚨 СКАЧИВАНИЕ ПРОВАЛЕНО! ПЕРЕХОДИМ НА ЗАГЛУШКИ...')
        # Автоматически создаем clean версию
        for game in games:
            game['imageUrl'] = ''
        
        clean_file = 'bg-stats-app/frontend/assets/data/tesera-collection-clean.json'
        with open(clean_file, 'w', encoding='utf-8') as f:
            json.dump(games, f, ensure_ascii=False, indent=2)
        print(f'✅ Создан файл с заглушками: {clean_file}')

if __name__ == '__main__':
    final_download()