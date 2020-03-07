[这里有中文版](README.zh.md)

This an unofficial localize project for game EXAPUNKS.

First at all, you should own this game, you can buy it on [steam](https://store.steampowered.com/app/716490/EXAPUNKS/) or [GOG](https://www.gog.com/game/exapunks) or whatever platforms.

# Prepare the environment
## 1. install [python](https://www.python.org/) 3 and some dependent libraries.

* install python from [https://www.python.org/downloads/](https://www.python.org/downloads/)

* install [pandas](https://pandas.pydata.org/)

    ```
    pip install pandas
    ```
* install [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
    ```
    pip install openpyxl
    ```
* install [Pillow](https://python-pillow.org/)
    ```
    pip install pillow
    ```

* install [python-lz4](https://github.com/python-lz4/python-lz4)
    ```
    pip install lz4
    ```

## 2. copy game files to localization working directory

* copy ``Content/descriptions/en/*`` to ``./export_txt/Content/descriptions/en/``
* copy ``Content/vignettes/*`` to ``./export_txt/Content/vignettes``
* copy ``PackedContent/fonts/*.packedfont`` to ``./font/fonts``
* copy ``PackedContent/*.tex`` to ``./images/PackedContent``
  
  ``Content\vignettes\nivas-3.csv`` miss a double quote at line 9, fix it by youself.
  
## 3. (Optional) install fonts
* install [Wen Quan Yi microhei](https://sourceforge.net/projects/wqy/files/wqy-microhei/0.2.0-beta/)
* install [Noto Sans Mono CJK](https://www.google.com/get/noto/help/cjk/)

# Translate the texts
There are three json files in directory ``import_txt``, they need be translated.

You could run ``json2excel.py`` to generate excel files from these json files, then edit them in M$ Excel or LibreOffice calc or whatever spreadsheet editor.

* ``EXAPUNKS_descriptions.json``

    Grabbed from Content/descriptions/*.txt

    All texts in this file need been traslated.

* ``EXAPUNKS_vignettes.json``

    Grabbed from Content/vignettes/*.csv

    All texts in this file need be translated.

* ``EXAPUNKS_exe.json``

    Grabbed from EXAPUNKS.exe

    **Not** all texts in this file need be translated. 
    
    Only translate the text you actually see in the game.

## How to use json2excel.py
generate EXAPUNKS_descriptions.xlsx from EXAPUNKS_descriptions.json
```
json2excel.py EXAPUNKS_descriptions.json EXAPUNKS_descriptions.xlsx
```
do the same thing
```
json2excel.py EXAPUNKS_descriptions.json
```
traverse current directory, generate .xlsx files from  all .json files.  
```
json2excel.py
```  

# Modify the textures
Run ``images/export_imgs.py`` 

It will traverse directory ``PackedContent``, convert all .tex files to .png into the directory ``out``.

Pick up the images what you want to modify. (No need for ``half``'s, we will generate them automatically.)

Put them all to the ``new`` dirctory, keep the some directory struct.

# Generate the localization patch
Run ``run.bat``, the localization patch will be generated in ``patch`` directory.

If you want to know more details about this procedure, see [details.md](details.md)

# Change game settings
Edit ``%USERPROFILE%\Documents\My Games\EXAPUNKS\xxxxxx\config.cfg``
```
Language = English
```
Change 'English' to 'Chinese | Japanese | French'

# Some screenshots
![](screenshot/screenshot_1.jpg)

![](screenshot/screenshot_2.jpg)

![](screenshot/screenshot_3.jpg)
