# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import random

class Markov():
    """Generates and maintain the markov chains database"""
    
    def __init__(self, dbname):
        #try:
        #    os.unlink(dbname)
        #except OSError:
        #    pass
        
        self.conn = sqlite3.connect(dbname)
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS words(id integer primary key autoincrement, word1 text, word2 text, word3 text)')
        self.c.execute('CREATE INDEX IF NOT EXISTS mainindex on words(word1, word2, word3)')
        self.tablesize = self.c.execute("SELECT COUNT(*) FROM words").fetchone()[0]

    def fill_db(self, infile):
        """Fills in database with words"""
        infh = open(infile, 'r')
        for line in infh:
            line = line.decode('utf-8').split('" "')
            if line[2].startswith('radiochan@'):
                string = line[4][:-3].replace('\\"', '"').replace('\\n', ' ').replace('\\\\', '\\')
                self.add_words(string)

    def build_chain(self, length):
        """Returns string of required words count"""
        
        words = self.c.execute("SELECT word1, word2, word3 FROM words LIMIT 1 OFFSET ?", (random.randint(0, self.tablesize - 1),)).fetchone()
        result = ' '.join(words)
        for i in xrange(length):
            if not words[2]:
                break
            words = self.c.execute("SELECT word1, word2, word3 FROM words WHERE word1=? ORDER BY RANDOM() LIMIT 1", (words[2],)).fetchone()
            if not words:
                break
            result += ' ' + ' '.join(words[1:])
        return result

    def add_words(self, string):
        """Adds words to the database"""
        words = string.replace('\n', ' ').split()
        while len(words) < 3:
            words.append("")
            
        for i in xrange(len(words) - 3):
            self.c.execute("INSERT INTO words (word1, word2, word3) VALUES (?, ?, ?)", (words[i], words[i + 1], words[i + 2]))
            self.tablesize += 1
        self.conn.commit()

markov = Markov("default.sqlite")

def main(bot, text):
    global markov
    if text.startswith(bot.res) and text[len(bot.res)] in [',', ':', '>', ' ']:
        chain = markov.build_chain(random.randint(1, 10))
        return chain
    else:
        markov.add_words(text)

def info(bot):
    return('', 10, main)
