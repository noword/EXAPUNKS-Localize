cd import_txt
:: Convert all xlsx files to json
excel2json.py
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

md patch\Content patch\PackedContent\fonts

move import_txt\strings.csv patch\Content
move font\*.packedfont patch\PackedContent\fonts