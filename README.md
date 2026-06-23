# Мосэкомониторинг - Данные качества воздуха

[![GitHub](https://img.shields.io/github/license/p1ne/mosecom)](https://github.com/p1ne/mosecom)
[![GitHub stars](https://img.shields.io/github/stars/p1ne/mosecom)](https://github.com/p1ne/mosecom)

Этот репозиторий содержит инструменты для получения и обработки данных о качестве воздуха с официального сайта Мосэкомониторинг (mosecom.mos.ru).

## Содержание

1. [Python скрипт](mosecom_extractor/README.md) - Автономный скрипт для извлечения данных
2. [Интеграция для Home Assistant](custom_components/mosecom/README.md) - Интеграция с Home Assistant для мониторинга качества воздуха в реальном времени

## Особенности

- Получение текущих данных о качестве воздуха с официальных станций мониторинга
- Поддержка различных форматов вывода (короткие/длинные названия, определенный тип газа)
- Поддержка различных единиц измерения (части, мг/м³)
- Извлечение исторических данных (ограничено веб-сайтом)
- Интеграция с Home Assistant для непрерывного мониторинга
- Автоматическое обнаружение типов газов для каждой станции
- Поддержка всех станций мониторинга Москвы

## Установка

### Python скрипт

Для использования Python скрипта требуется Python 3.6+:

```bash
cd mosecom_extractor
pip install -r requirements.txt
python mosecom_extractor.py --help
```

### Интеграция для Home Assistant

Интеграция доступна через HACS (Home Assistant Community Store) или может быть установлена вручную:

1. Скопируйте папку `custom_components/mosecom` в директорию `custom_components` вашего Home Assistant
2. Перезапустите Home Assistant
3. Перейдите в Настройки → Устройства и службы → Добавить интеграцию
4. Найдите "Moscow Air Quality Monitoring" и следуйте инструкциям настройки

## Репозиторий

GitHub: https://github.com/p1ne/mosecom

## Лицензия

Этот проект лицензирован по лицензии MIT - подробности см. в файле [LICENSE](LICENSE).