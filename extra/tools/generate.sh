#!/bin/bash
echo "MUST BE RUN ON A FRESH REV!"
rm en_EN.po
(
cd ../data/monsters
sed -i 's/genMonster(\"\([^"]*\)\"/genMonster\(_\(\"\1\"\)/g' */*.py */*/*.py */*/*/*.py
sed -i 's/genMonster(\(.*\), \"\([^"]*\)\"/genMonster(\1, _(\"\2\")/g' */*.py */*/*.py */*/*/*.py
)
xgettext --from-code=utf-8 --language=python -k_l:2 -k_lp:2,3 -k_lc:2c,3 -k_lcp:2c,3,4 -kl:1 -klp:1,2 -klc:1c,2 -klcp:1c,2,3 -klmessage:1  -klpmessage:1,2 -klcmessage:1c,2 -klcpmessage:1c,2,3 -o en_EN.po ../*.py ../{core,data}/*.py ../{core,data}/*/*.py ../{core,data}/*/*/*.py ../data/*/*/*/*.py

(
cd ../data/monsters
/usr/bin/hg revert .
)
export LC_CTYPE=en_US.UTF-8
# Append item stuff
python2 generate_items.py >> en_EN.po

# Important, otherwise non-English characters will display as fucked up in non-English translations. This can, for no reason be anything other than UTF9 in any translation.
sed -i 's/CHARSET/UTF-8/' en_EN.po

# Fix duplicates
msguniq en_EN.po -o en_EN.po
