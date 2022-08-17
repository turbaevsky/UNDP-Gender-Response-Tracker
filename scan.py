#!/usr/bin/python3

import pandas as pd
import spacy
import classy_classification
import sqlite3
import requests, datetime
import pdfplumber
from tqdm import tqdm
import logging
import os

logging.basicConfig(level=logging.DEBUG)

#con = sqlite3.connect('gender.db')
#cur = con.cursor()
#cur.execute("CREATE TABLE text (text text, class text)")
#cur.execute("CREATE TABLE nlp (doc text, class text)")
#con.commit()
#con.close()


nlp = spacy.load("en_core_web_sm", disable=['tagger','ner','parser'])
nlp.max_length = 3000000

df = pd.read_excel('Masterfile_NEW_UNDP-UNW Gender Dashboard-11-October-2021-final_lv.xlsx')

#con = sqlite3.connect('gender.db')
#cur = con.cursor()

for i in range(len(df)):
    try:
        logging.info(f'processing [{i}/{len(df)}]')
        src = df.iloc[i]['Sources'].split(';')
        cat = df.iloc[i]['Policy Measure Category'].replace(',','_').replace(' ','_')
        if src[0][-4:] == '.pdf':
            logging.debug(f'processing {src[0]}')
            pdf = requests.get(src[0], stream=True).content
            with open('temp.pdf','wb') as f:
                f.write(pdf)
            logging.debug(f'start processing')
            no = 0
            text = ''
            start = True
            with pdfplumber.open('temp.pdf') as pdf:
                while start:
                    try:
                        page = pdf.pages[no]
                        text += page.extract_text()
                        no += 1
                        #print('.', end='')
                    except Exception as e:
                        logging.debug(f'{e} during processing page {no}')
                        start = False
            logging.debug(f'done')

            try:
                os.mkdir(cat)
            except:
                pass

            os.chdir(cat)
            with open(f'{i}.txt', 'w') as f:
                f.write(text)
            logging.debug(f'saved')
            os.chdir('..')

            i#logging.debug('adding to DB...')
            #cur.execute("INSERT INTO text VALUES (?,?)", (text, cat))
            #con.commit()
            #logging.debug('done')
            #logging.info('starting NLP')
            #doc = nlp(text)
            #cur.execute("INSERT INTO nlp VALUES (?,?)", (doc, cat))
            #con.commit()
            #selection.append([pdf_reader('temp.pdf', nlp), cat])
            logging.info(f'done')
        else:
            logging.warning('no pdf found')
    except Exception as e:
        logging.warning(e)

con.close()
