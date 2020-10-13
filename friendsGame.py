import os
import sqlite3
from sqlite3 import Error


conn = sqlite3.connect(r"C:\Users\Artic\PycharmProjects\friends\pythonsqlite.db")
print(sqlite3.version)
c = conn.cursor()
# c.execute('''CREATE TABLE quotes(season, episode, character, quote)''')
dirPath = r"C:\Users\Artic\Desktop\friendsQuotes"
directory = os.fsencode(dirPath)
'''
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    folderPath = dirPath + "\\" + filename
    if filename[2] == "0":
        season = 10
        episode = filename[5] + filename[6]
    else:
        season = int(filename[1])
        episode = filename[4] + filename[5]
    with open(folderPath, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if ":" in line:
            splitLine = line.split(":")
            character = splitLine[0]
            quote = splitLine[1]
            c.execute("insert into quotes values (?, ?, ?, ?)", (season, episode, character, quote))
'''
#c.execute("drop table quotes")
# Save (commit) the changes
# conn.commit
# Clean up a lot of the naming issues
# c.execute("UPDATE quotes SET character = replace(character, 'CHAN', 'Chandler') WHERE character='CHAN'")
# Problems with grave symbols
# c.execute("update quotes set quote = replace(quote, '’', '''')")
# conn.commit()
# c.execute("update quotes set quote = replace(quote, '…', '...')")
# conn.commit()
# c.execute("select * from quotes order by season, episode")
# c.execute("SELECT DISTINCT character from quotes where character='JACOBLIN'")
# c.execute("SELECT *, row_number() OVER (ORDER BY season, episode) FROM quote;")
print(*c.fetchall())
c.execute("SELECT COUNT(1) FROM quotes WHERE character LIKE '%Joey%' and season = 2 and episode = '03'")
print(*c.fetchall())
c.execute("SELECT * FROM (SELECT * FROM quotes WHERE character LIKE '%Joey%' and season = 2 and episode = '03' ORDER BY season, episode) LIMIT 10,20;")
# c.execute("SELECT * FROM quotes WHERE season = 6 and episode = '23' ORDER BY season, episode LIMIT 10, 10;")
# c.execute("SELECT DISTINCT character from quotes WHERE NOT character like '%Joey%' AND NOT character like '%Chandler%' AND NOT character like '%Chandler%' AND NOT character like '%Monica%' AND NOT character like '%Ross%' AND NOT character like '%Rachel%' AND NOT character like '%Phoebe%' AND season=2")
# case insensitive query
# c.execute("select distinct character from quotes where character like '%Joey%'")
print(*c.fetchall(), sep='\n')
# print (c.fetchall())
