这是一个非官方的游戏汉化项目，游戏名称是EXAPUNKS。

首先，你需要拥有这个游戏。你可以在 [steam](https://store.steampowered.com/app/716490/EXAPUNKS/) 或 [GOG](https://www.gog.com/game/exapunks) 或任意平台上购买到此游戏。

# 准备环境
## 1. 安装 [python](https://www.python.org/) 3 及相关依赖库

* 安装 python [https://www.python.org/downloads/](https://www.python.org/downloads/)

* 安装 [pandas](https://pandas.pydata.org/)

    ```
    pip install pandas
    ```


* 安装 [Pillow](https://python-pillow.org/)
    ```
    pip install pillow
    ```

* 安装 [python-lz4](https://github.com/python-lz4/python-lz4)
    ```
    pip install lz4
    ```

## 2. 复制游戏文件到汉化工作目录

* 复制 ``Content/descriptions/en/*`` 到 ``./export_txt/Content/descriptions/en/``
* 复制 ``Content/vignettes/*`` 到 ``./export_txt/Content/vignettes``
* 复制 ``PackedContent/fonts/*`` 到 ``./font/fonts``
* 复制 ``PackedContent/*.tex`` 到 ``./images/PackedContent``

# 翻译文本
在import_txt目录下有 3 个json文件需要翻译。

你可以运行``json2excel.py`` 把 json 文件转成excel文件，然后在 M$ Excel 或 LibreOffice calc 或随便哪个电子表格器进行编辑翻译。

# 修改图片
运行 ``images/export_imgs.py`` 

这会遍历 ``PackedContent`` 目录, 把.tex转换成.png，并输出到 ``out`` 目录。

挑选你需要修改的图片。把它们放在 ``new`` 目录下, 注意保持同样的目录结构。

# 生成汉化补丁
运行 ``run.bat``, 汉化补丁会在 ``patch`` 目录下生成.

# 汉化截图
![](screenshot/screenshot_1.jpg)

![](screenshot/screenshot_2.jpg)

![](screenshot/screenshot_3.jpg)
