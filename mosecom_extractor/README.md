# Мосэкомониторинг - Python скрипт для извлечения данных

Этот Python скрипт извлекает данные о качестве воздуха с официального сайта Мосэкомониторинг (mosecom.mos.ru).

## Особенности

- Получение текущих данных о качестве воздуха с указанной станции
- Поддержка различных форматов вывода:
  - Короткие названия газов (по умолчанию)
  - Длинные названия газов
  - Данные только для определенного типа газа
- Поддержка различных единиц измерения:
  - % ПДК (по умолчанию)
  - мг/м³
- Извлечение исторических данных (ограничено веб-сайтом)
- Поддержка всех станций мониторинга Москвы

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```bash
python mosecom_extractor.py [ОПЦИИ] URL_СТАНЦИИ
```

### Опции

- `-h`, `--help`: Показать справку
- `-f {short,long}`, `--format {short,long}`: Формат вывода (short/long)
- `-g GAS_TYPE`, `--gas GAS_TYPE`: Получить данные только для определенного газа
- `-u {parts,mg/m3}`, `--unit {parts,mg/m3}`: Единица измерения (parts/mg/m3)
- `-d DATE`, `--date DATE`: Дата для исторических данных (в формате DD.MM.YYYY)

### Примеры

```bash
# Получить текущие данные в формате коротких названий (по умолчанию)
python mosecom_extractor.py https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/

# Получить текущие данные в формате длинных названий
python mosecom_extractor.py -f long https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/

# Получить данные только для NO2
python mosecom_extractor.py -g NO2 https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/

# Получить данные в мг/м³
python mosecom_extractor.py -u mg/m3 https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/

# Получить исторические данные за определенную дату
python mosecom_extractor.py -d 01.06.2026 https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/
```

## Поддерживаемые типы газов

- CO (Оксид углерода / Carbon Monoxide)
- NO2 (Диоксид азота / Nitrogen Dioxide)
- CH4 (Метан / Methane)
- PM10 (Взвешенные частицы PM10)
- NO (Оксид азота / Nitric Oxide)
- H2S (Сероводород / Hydrogen Sulfide)
- C6H5OH (Фенол / Phenol)

## Лицензия

Этот проект лицензирован по лицензии MIT.