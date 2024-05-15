# Бебрики


## Состав проекта
Проект состоит из четырех частей
* Модуль ML(detectors, verification);
* Модуль API;
* TG bot;

Папка bot - содержит в себе код слушающий telegram bota;

Файл main.py - запускет API и ML модуль

Перед любым действием:

* Запустите [init.sh](init.sh)

* установите python 3.10 или аналогичные;

* При помощи команды ```pip install -r requirements.txt``` устанавливаем необходимые зависимости.

* Если вы хотите использовать CUDA ```pip install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 --index-url https://download.pytorch.org/whl/cu121```

* В папку [weigts](weigts) нужно положить веса [Скачать](https://disk.yandex.com/d/c8ZYFJVHJCa9XA)

Для детекции доступны модели:
* yolov8l-face.pt
* yolov8m-face.pt
* yolov8n-face.pt

Для верификации доступны модели:
* adaface_ir18_casia.ckpt
* adaface_ir50_webface4m.ckpt
* adaface_ir101_webface4m.ckpt
* adaface_ir101_webface12m.ckpt

Настроить модели можно в [config.json](config.json)