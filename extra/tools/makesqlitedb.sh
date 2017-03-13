# This file makes a sqlite db, from the latest SQL.

cp ../data/sql/latest_sql.sql ../database

# Add houses.
cat ../data/sql/houses.sql >> ../database

cat ../database |
grep -v ' KEY "' |
grep -v ' UNIQUE KEY "' |
grep -v ' PRIMARY KEY ' |
sed '/^SET/d' |
sed 's/ unsigned / /g' |
sed 's/ auto_increment/ primary key autoincrement/g' |
sed 's/ smallint([0-9]*) / integer /g' |
sed 's/ tinyint([0-9]*) / integer /g' |
sed 's/ int([0-9]*) / integer /g' |
sed 's/ character set [^ ]* / /g' |
sed 's/ enum([^)]*) / varchar(255) /g' |
sed 's/ on update [^,]*//g' |
sed 's/\\r\\n/\\n/g' |
sed 's/\\"/"/g' |
sed 's/ AUTO_INCREMENT=[0-9]*\b//' |
sed 's/ COMMENT .*$/,/g' |
sed 's/  UNIQUE KEY .*$//g' |
sed 's/ `id` integer NOT NULL AUTO_INCREMENT/ `id` integer primary key autoincrement/g' |
sed 's/,\\n\\n)/\)/g' |
perl -e 'local $/;$_=<>;s/,\n\)/\n\)/gs;print "begin;\n";print;print "commit;\n"' |
perl -pe '
if (/^(INSERT.+?)\(/) {
  $a=$1;
  s/\\'\''/'\'\''/g;
  s/\\n/\n/g;
  s/\),\(/\);\n$a\(/g;
}
' > ../database.sql
cat ../database.sql | sqlite3 ../database.db > ../database.err
ERRORS=`cat ../database.err | wc -l`
if [ $ERRORS == 0 ]; then
  echo "Conversion completed without error. Output file: ../database.db"
  #rm ../database.sql
  #rm ../database.err
else
  echo "There were errors during conversion.  Please review ../database.err and ../database.sql for details."
fi