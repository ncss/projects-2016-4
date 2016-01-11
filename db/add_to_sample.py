import sqlite3

con = sqlite3.connect('database.db')
oldfile = open('sample.sql')
old = oldfile.readlines()
oldfile.close()

for line in con.iterdump():
    if line.startswith('INSERT') and line not in old:
        old.append(line + '\n')

f = open('sample.sql', 'w')
f.write(''.join(old))
f.close()