cd import_txt
:: Convert all xlsx files to json
excel2json.py --auto
:: Grab used character in json, save them to font/chars.txt
get_chars.py
:: Read translated texts, generate the text patch
import_txt.py
cd ..

cd font
:: Generate new font
gen.py
cd ..

cd images
:: Generate new tex
import_imgs.py
cd ..

cd manual
:: Generate pdf manual
gen.py
cd ..

md patch
md patch\Content
md patch\Content\manual
md patch\PackedContent
md patch\PackedContent\fonts

move import_txt\strings.csv  patch\Content
move font\*.packedfont       patch\PackedContent\fonts
move manual\digital_en_1.pdf patch\Content\manual\digital_cn_1.pdf