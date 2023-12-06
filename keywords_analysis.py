#import os
import pandas as pd
#import random
#import newspaper
#from newspaper import Article, fulltext, Config, ArticleException
#import time
import numpy as np
#import requests
import re
#import concurrent.futures
#from concurrent.futures import ThreadPoolExecutor
#from time import sleep
#import threading

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.tokenize import RegexpTokenizer
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams



acumulated_dataframes = pd.read_excel(r'C:\github_repos\mars_quater_report\project\mars_acumulated_synthesio_plus_intermedia_21042023_content.xlsx') # cambiar por la ruta del archivo
print(acumulated_dataframes.shape)
acumulated_dataframes.head()

def define_stopwords():
    sw_es=stopwords.words('spanish')
    sw_pt=stopwords.words('portuguese')
    sw_en=stopwords.words('english')
    sw_es_title=[word.title() for word in sw_es]
    sw_pt_title=[word.title() for word in sw_pt]
    sw_en_title=[word.title() for word in sw_en]
    return sw_es, sw_pt, sw_en, sw_es_title, sw_pt_title, sw_en_title


stopwords_result = define_stopwords()
sw_es, sw_pt, sw_en, sw_es_title, sw_pt_title, sw_en_title = [stopwords_result[i] for i in range(0,6)]
sw_total = sw_es + sw_pt + sw_en +  sw_es_title +  sw_pt_title + sw_en_title

def get_mayusculas(texto):
    texto=str(texto)
    palabras_importantes=[]
    mayusculas=(r"([A-Z][a-zÁ-ÿ0-9]{1,20}\s?\,?\.?\s?)")
    texto=re.sub('[^\w\s]',' ',texto)
    texto=re.sub('[0-9]+', '', texto)  
    tokenizer=RegexpTokenizer(r'\w+')
    texto=tokenizer.tokenize(texto)
    texto=[word for word in texto if word not in sw_pt]
    texto=[word for word in texto if word not in sw_es]
    texto=[word for word in texto if word not in sw_en]
    texto=[word for word in texto if word not in sw_pt_title]
    texto=[word for word in texto if word not in sw_es_title]
    texto=[word for word in texto if word not in sw_en_title]
    tokens=[word.strip() for word in texto if word is not None]
    tokens=[word.strip() for word in tokens if len(word)>1]
    palabras_importantes=[word for word in tokens if word.istitle()]
    palabras_importantes=[word for word in tokens if re.match(mayusculas, word)]
    return palabras_importantes

def clean_and_tokenize(texto):
    texto=str(texto).lower()
    texto=re.sub('[^\w\s]',' ',texto)
    tokenizer=RegexpTokenizer(r'\w+')
    texto=tokenizer.tokenize(texto)
    texto=[word for word in texto if word not in sw_pt]
    texto=[word for word in texto if word not in sw_es]
    tokens=[word.strip() for word in texto if word is not None]
    tokens=[word.strip() for word in tokens if len(word)>1]
    return tokens

def clean_text_wt(texto):
    clean_tokens=clean_and_tokenize(texto)
    texto = ' '.join(clean_tokens)
    return texto

def crear_dicc_keywords(df_keywords):
    df_keywords=df_keywords.fillna('exxxtract')
    area_dict = df_keywords.to_dict('list')
    for k,v in area_dict.items():
        nv=list(set(v))
        nv=[x for x in v if x != 'exxxtract']
        nv=list(set(nv))
        area_dict[k]=nv
    return area_dict

def tokenizar(texto):
    nuevo_texto = texto
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    regex = '[\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
    nuevo_texto = re.sub(regex , ' ', nuevo_texto)
    nuevo_texto = re.sub("\d+", ' ', nuevo_texto)
    nuevo_texto = re.sub("\\s+", ' ', nuevo_texto)
    nuevo_texto = nuevo_texto.split(sep = ' ')
    nuevo_texto = [token for token in nuevo_texto if len(token) > 1]
    nuevo_texto=[word for word in nuevo_texto if word not in sw_total]
    return(nuevo_texto)

def divide_en_ngramas(texto,n):
    if len(texto)>0:
        n_grams=[]
        enegramas = ngrams(texto.split(), n)
        for grams in enegramas:
            i=0
            division=''
            while i<n: 
                division=division+' '+grams[i]
                i+=1
            n_grams.append(division.lstrip())
    else:
        return ''
    return n_grams

def convert_to_words(lst, category_list_found):
    new_lst = []
    for item, item2 in zip(lst, category_list_found):
        if int(item) > 0:
            new_lst.append(item2.replace('_FOUND', ''))
    return new_lst

def find_single_word_in_tokenized_text(row, keyword):
    if len([x for x in row if x == keyword]) >= 1:
        return [x for x in row if x == keyword]
    else:
        return ''

def define_wnr():
    wnr = set(['AMLO','Andrés Manuel López Obrador','Andres Manuel Lopez Obrador',
               'Andres Manuel','Lopez Obrador','mañanera','Andrés Manuel','López Obrador', 'López',
               'PRESIDENTE ANDRÉS MANUEL LÓPEZ OBRADOR', 'manuel','obrador', "Obrador" ,
               'Scarlett' , 'Johansson', 'Scarlett Johansson'  "Anaya", "Monreal", "Chris" , 
               "Evans", "Chris Evans", "Noroña", "PAN", "MORENA", "PRI", "Acción", "Movimiento",
               "Ciudadano",  "MC", "PRD"  , "Peña Nieto", "Peña", "dictadura", "Ortega",'Alfaro',
               'Lozoya', 'Dune', 'vacuna', 'Buzz','Aburto', 'Colosio','Guevara',
               "Daniel Ortega", "votaciones" ,"Maya", "Gortari", "polarización", "Fox",  "VOX", 
               "Felipe Calderón", "Calderón",'calderón', 'Adele','Calamar','Salma Hayek', 'Hayek', 
               'François', 'Pinault', 'Pinal', 'cine' ,'Cine' ,'oro','Oro' 'Macron', 'Merkel', 'podcast',
                'Buffet', 'PODCAST','podcast','Podcast', 'Gatell', 'Ebrard', 'Nerea', 'Ocaña', 'Trevi','FGR', 'INE', 'Yuya',
                'Chumel', 'AIFA','CFE', 'Pemex', 'Coparmex', 'UIF', 'Pablo', 'Gómez','Bukele', 'Canelo',
                'Peniley', 'Krauze', 'sicario', 'Oxxo', 'DiCaprio', 'Natti', 'BioNTech', 'política', 'Cómics' , 'Wonder',
                'Clouthier', 'Nacif', 'Shabazz', 'Tatiana', 'Inegi', 'INEGI', 'déficit', 'balanza', 'eléctrica',
                'homicidio', 'violación', 'sexual', 'Viajar', 'película', 'cintas', 'Estatal', 'Federal' ,
                'muerte', 'murío', 'muere', 'fallecidos','muertos', 'criminales','prisiones','Sinaloa','Zacatecas', 
                'Ómicron','OMS','vacunas','Janssen', 'Sputnik' , 'Phizer', 'Astra' , 'ESCUCHA', 'OCDE', 'carbón', 'Checo',
                'Verstapen', 'Hamilton', 'Deezer', 'FIL', 'Zócalo', 'Cuba' , 'Noticias', 'Evo', 'Vladimir', 'Putin', 'guerra', 'Guerra',
                'Zelensky', 'War', 'war'])
    return  wnr
# Palabras no relacionadas
wnr = define_wnr() 

# Define macro dictionary
key_words = []
dic_keys = ['Competidores', 'MARS Incorporated', 'MARS Mexico', 'MARS Wrigley', 'TURIN', 'MARS Petcare', 
            'MARS Voceros', 'ELIMINAR', 'Agentes', 'Sustentabilidad', 'Reciclaje', 'Plásticos de un solo uso', 
            'Agricultura sustentable', 'Compromiso hídrico', 'Net Zero', 'Cadena de suministro sostenible', 
            'Reforestación', 'Cuidado de los océanos', 'Proyecto Coral Reef', 'Negocio', 'Innovación', 'Inversión', 
            'Liderazgo Pet food', 'Liderazgo Dulces', 'Liderazgo Chocolates', 'Mejor empresa para trabajar', 
            'Petfriendly', 'Empleo a Jóvenes', 'Prestaciones equitativas', 'Mindfulness', 'Wellbeing', 
            'Trabajo híbrido', 'Parenting', 'Diversidad e inclusión', 'Comunidad LGBT+', 'Empoderamiento de mujeres', 
            'Discapacidad', 'Oportunidad laboral a personas de la tercera edad', 'EXCLUSIONES']

#for keys in dic_keys:
#    if keys in dic_keywords:
#        for i in dic_keywords[keys]:
#            key_words.append(i)

#key_words = set(key_words + words_to_verify)

#print(len(key_words))


def func_wnr(words):
     mwlen = len(wnr.intersection(words))
     fwlen = len(key_words.intersection(words))
     if mwlen > 0 and fwlen == 0:
          return "not"
     elif mwlen == 0 and fwlen > 0:
          return "yes"
     elif mwlen > 0 and fwlen <=3:
          return "prob_not"
     elif mwlen > 0 and fwlen >3:
          return "prob_yes"
     else: 
          return "prob_not"

acumulated_dataframes['Capital Case Words Title'] = acumulated_dataframes['title'].apply(lambda row : get_mayusculas(str(row)))
acumulated_dataframes.head()

acumulated_dataframes['Capital Case Words Content'] = acumulated_dataframes['extracted_content'].apply(lambda row : get_mayusculas(str(row)))
acumulated_dataframes.head()

acumulated_dataframes['Clean Content']  = acumulated_dataframes['extracted_content'].apply(lambda row: clean_text_wt(row))
acumulated_dataframes.head()

df_notas = acumulated_dataframes.copy()
print(df_notas.shape)
df_notas.head(3)


print('Número de filas: {} \nNúmero de columnas: {} '.format(df_notas.shape[0],df_notas.shape[1]))
print('Nombres de las columnas en df_notas:{}'.format(df_notas.columns))


df_notas = df_notas.loc[:,~df_notas.columns.duplicated()]
print(df_notas.shape)
df_notas.head()


df_notas['TAM_CONTENTS'] = df_notas['extracted_content'].apply(lambda row: len(str(row)))
df_notas['Count_Size']    = np.where(df_notas['TAM_CONTENTS']>= 400,
                                   "Size >= 400",
                                    "Size < 400")
print(df_notas.shape)
df_notas.head()

ANALIZED = df_notas.fillna('')\
                   .replace('nan','')
print('Número de filas: {} \nNúmero de columnas: {} \nColumnas:{}'.format( ANALIZED.shape[0], ANALIZED.shape[1], ANALIZED.columns))


# Remove Duplicated Columns
ANALIZED = ANALIZED.loc[:,~ANALIZED.columns.duplicated()]
print(ANALIZED.shape)
ANALIZED.head()


df_keywords  = pd.read_excel(r"C:\github_repos\mars_quater_report\project\MARS_Keywords_Q1.xlsx")
print(df_keywords.shape)
df_keywords.head()


dic_keywords = crear_dicc_keywords(df_keywords)
dic_keywords

wnr = set(list(wnr) + dic_keywords['ELIMINAR'])
len(wnr)

ANALIZED['Full Content'] = ANALIZED['extracted_content']

ANALIZED['Tokenizar']   = ANALIZED['Full Content'].apply(lambda row: tokenizar(row))
print(ANALIZED.shape)
ANALIZED.head()


ANALIZED['CLEAN_Contents']  = ANALIZED['extracted_content'].apply(lambda row: clean_text_wt(row))


ANALIZED['1_GRAM_Contents'] = ANALIZED['CLEAN_Contents'].apply(lambda row: divide_en_ngramas(row,1))
ANALIZED.head()

ANALIZED = ANALIZED.copy() # esto es para que no me de un warning de que estoy modificando una copia de un dataframe

category_list_found = []
for k, v in dic_keywords.items():
    k = k.upper()
    ANALIZED[str(k)] = 0
    ANALIZED[str(k) + '_FOUND'] = 0
    renamed = []
    print(k)
    for keyword in v:
        keyword = keyword.lower().strip()
        ANALIZED[k + '_' + keyword] = 0
        if len(keyword.split(' ')) == 1:
            try:
                ANALIZED[k + '_' + keyword] = ANALIZED['1_GRAM_Contents'].apply(lambda row: find_single_word_in_tokenized_text(row, keyword))
            except AttributeError:
                ANALIZED[k + '_' + keyword] = ANALIZED['1_GRAM_Contents'].apply(str).apply(lambda row: find_single_word_in_tokenized_text(row, keyword))
        else:
            ANALIZED[k + '_' + keyword] = ANALIZED['CLEAN_Contents'].str.contains(str(keyword).lower())
        ANALIZED[k + '_' + keyword] = ANALIZED[k + '_' + keyword].apply(lambda x: str(x).replace("True", keyword))
        ANALIZED[k + '_' + keyword] = ANALIZED[k + '_' + keyword].apply(lambda x: str(x).replace("False", ""))
        renamed.append(k + '_' + keyword)
    ANALIZED[k] = ANALIZED[renamed].values.tolist()
    ANALIZED[k] = ANALIZED[k].apply(lambda row: list(set(row)))
    ANALIZED[k] = ANALIZED[k].apply(lambda row: [x for x in row if len(x) > 1])
    ANALIZED[k] = ANALIZED[k].apply(lambda row: '' if len(row) < 1 else row)
    ANALIZED[str(k) + '_FOUND'] = ANALIZED[k].apply(lambda row: len(row))
    if k == 'COMPETIDORES':
        continue
    else:
        ANALIZED = ANALIZED.drop(columns=renamed)
    category_list_found.append(str(k) + '_FOUND')

ANALIZED['Resumen_Categorias'] = ANALIZED[category_list_found].values.tolist()
ANALIZED['Resumen_Categorias'] = ANALIZED['Resumen_Categorias'].apply(lambda row: convert_to_words(row, category_list_found))
ANALIZED = ANALIZED.fillna('')
print(ANALIZED.shape)
ANALIZED.head()

ANALIZED['Mayusculas_Contents']  = ANALIZED['Full Content'].apply(lambda row : get_mayusculas(str(row)))
ANALIZED['Mayusculas_Title']     = ANALIZED['title'].apply(lambda row : get_mayusculas(row))
ANALIZED['Mayusculas_Contents'].head()


ANALIZED['Categor_poli']  = ANALIZED['Tokenizar'].apply(lambda row: func_wnr(row))
ANALIZED['Categor_poli'].value_counts()


ANALIZED['Categor_poli_title']  = ANALIZED['Mayusculas_Title'].apply(lambda row: func_wnr(row))
ANALIZED['Categor_poli_title'].value_counts()
ANALIZED.head()

ANALIZED.to_excel(r"C:\github_repos\mars_quater_report\project\mars_acumulated_synthesio_plus_intermedia_21042023_content_script_version.xlsx", index=False)