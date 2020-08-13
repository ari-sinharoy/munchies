'''
This is a word cloud generator
'''

import os
import re
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords 
import matplotlib.pyplot as plt
import PyPDF2

os.chdir(r'C:\Users\JJ\Desktop\Python_Codes\Word Cloud')

# load the pdf file


pdf_o = open('article_alz_org.pdf', 'rb') 
pdf_r = PyPDF2.PdfFileReader(pdf_o) 

# extract text and close the pdf file object  
pg_n = pdf_r.numPages 
pg_o = []
for x in range(pg_n):
    pg_x = pdf_r.getPage(x).extractText().replace('\n','')
    pg_o += [pg_x]
  
pdf_o.close() 


# flatten list
pg_j = [re.split('\s', re.sub(r'[^\w\s]', ' ', item)) for item in pg_o]
wd_l = [item.lower() for subl in pg_j for item in subl] 

# remove stop words
st_wd = set(stopwords.words('english')) 
wd_f = [wd for wd in wd_l if not ((wd in st_wd) or (len(wd)==1) or (wd==''))] 

# construct the frequency table
wd_uq = set(wd_f)  
wd_fr = [wd_f.count(x) for x in wd_uq]
wd_df = pd.DataFrame()
wd_df['words'] = list(wd_uq)
wd_df['frequency'] = wd_fr
wd_df = wd_df.sort_values(by = ['frequency'], ascending = False)
wd_df['frequency'] /= wd_df['frequency'].max()
wd_df['frequency'] *= 100
wd_df['frequency'] = wd_df['frequency'].astype(int)

clr = ['crimson','steelblue','gray']

a_area = np.mgrid[0:1.0:0.001, 0:1.0:0.0025].reshape(2,-1).T
#sel = np.random.randint(0,len(a_area))
cnt = 0
for m in range(2,500):
    h_dim = len(a_area)
    s_item = wd_df.iloc[m]
    s_wd = s_item.words
    s_hght = round(0.005*(0.2*s_item.frequency + 2)/2, 2)
    s_wdth = round(6*0.012*(len(s_item) + 4), 2)
    x,y = [-1.,-1.]
    while not all(q in a_area for q in [x,y]):
        sel = np.random.randint(0,h_dim)
        x,y = a_area[sel]
    a_rot = np.random.choice([0.,90.])
    if a_rot == 0:
        x1, y1, s_wdth1, s_hght1 = x, y, s_wdth, s_hght
    else:
        x1, y1, s_wdth1, s_hght1 = y, x, s_hght, s_wdth
    leb, rib, lwb, upb = x1 - s_wdth1, x1 + s_wdth1, y1 - s_hght1, y1 + s_hght1 
    leb, rib, lwb, upb = [0. if q < 0 else q for q in [leb, rib, lwb, upb]]    
    a_area = a_area[((a_area[:,0] < leb) | (a_area[:,0] > rib) | 
                     (a_area[:,1] < lwb) | (a_area[:,1] > upb))]
    cnt += 1
    if s_item.frequency > 20: 
        v_alpha = np.random.randint(90,100)/100
    else:
        v_alpha = np.random.randint(80,100)/100
    plt.text(x1, y1, s_wd, size = int(1.0*s_item.frequency + 4), 
             rotation=a_rot,
             ha="center", va="center",
             color = np.random.choice(clr), 
             alpha = v_alpha
             )
    plt.axis('off')
