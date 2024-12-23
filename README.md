# Steroids

## Описание

**Steroids** – это 2D-игра на Python с использованием библиотеки Pygame. Игрок управляет космическим кораблем, уничтожая вражеские планеты и избегая столкновений. Игра включает динамическое движение объектов, стрельбу, эффекты взрывов и звуковое сопровождение.

---

## Установка

1. Убедитесь, что у вас установлен Python (версия ≥3.8).
2. Установите Pygame командой:
   ```bash
   pip install pygame
   ```
3. Скачайте или клонируйте репозиторий с игрой.
4. Убедитесь, что все изображения находятся в папке `images`, а звуковые файлы — в папке `sounds`.

---

## Структура проекта

* **main.py** — основной файл игры.
* **images/** — папка с графическими ресурсами (корабли, планеты, фон, взрывы).
* **sounds/** — папка с аудиофайлами (музыка и эффекты).

---

## Как играть

1. Запустите игру командой:
   ```bash
   python main.py
   ```
2. На экране появится меню. Нажмите любую клавишу, чтобы начать игру.
3. Управление:
   * ▶◀ (влево/вправо) — поворот корабля.
   * ▲▼ (вверх/вниз) — ускорение и торможение.
   * `Пробел` — выстрел.
4. Цель игры — уничтожать вражеские планеты и избегать столкновений.

---

## Основные особенности

* **Графика** :
  * Космический фон и реалистичные спрайты.
  * Визуальные эффекты взрывов.
* **Физика** :
  * Плавное движение и повороты корабля.
  * Имитация инерции.
* **Звук** :
  * Звуковые эффекты стрельбы и взрывов.
  * Фоновая музыка из вселенной Star Wars.
* **Сложность** :
  * Постепенное увеличение скорости врагов.
  * Ограниченное количество жизней.

---

## Требования

* Python ≥3.8
* Pygame ≥2.0

---

## Содержание папки `images`

* `Space_1.png` — фон игры.
* `xwing_fly.png` и `xwing-png-6101995.png` — изображения космического корабля игрока.
* `regularExplosion*.png` и `sonicExplosion*.png` — анимации взрывов.
* `Planet*.png` — изображения планет.

## Содержание папки `sounds`

* `blast-101soundboards (mp3cut.net).mp3` — звук выстрела.
* `expl3.wav` и `expl6.wav` — звуки взрывов.
* `Victory Celebration.mp3` — фоновая музыка.
