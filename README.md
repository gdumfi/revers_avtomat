# Установка необходимых зависимостей

Перед началом работы необходимо установить два инструмента:

1. **MiKTeX**
   Скачайте и установите с официального сайта:
   [https://miktex.org/download](https://miktex.org/download)

2. **FFmpeg**

   * Скачайте архив полной сборки по ссылке:
     [https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.1.1-full_build.7z](https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.1.1-full_build.7z)
   * Разархивируйте содержимое архива.
   * Переименуйте полученную папку в `FFmpeg`.
   * Добавьте путь к `FFmpeg` в системную переменную PATH, выполнив в командной строке от имени администратора:

     ```cmd
     setx /m PATH "C:\FFmpeg\bin;%PATH%"
     ```

После выполнения этих шагов можно переходить к запуску проекта.
