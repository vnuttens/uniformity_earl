import os
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import csv
#--------------------------------------------------------------------------

# IN TE VULLEN
filename = "Calibration_20211105_134400.txt"    # file name met data
slice_begin = 35                                # enter first slice
slice_end = 109                                 # enter last slice
#--------------------------------------------------------------------------

# Initialisation
rows = []
a_conc = []
cov = []
suv_ratio = []
slice_number = []
if not os.path.exists('Verwerkte EARLS'):
  os.mkdir('Verwerkte EARLS')


#--------------------------------------------------------------------------

# reading txt file
with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile,delimiter = ' ')
        for row in csvreader:
                rows.append(row)

rows_relevant = rows[26:len(rows)-1]
for row in rows_relevant:
    row = list(filter(None, row))
    if int(row[0]) >= slice_begin and int(row[0]) <= slice_end:
        slice_number.append(int(row[0]))
        a_conc.append(float(row[1]))
        cov.append(float(row[3]))
        suv_ratio.append((float(row[2])-1)*100)


#--------------------------------------------------------------------------
# Making plot

fig1, ax1  = plt.subplots(1, 1, sharex=True,sharey=True)
x1 = np.linspace(slice_number[0], slice_number[-1], len(slice_number))

avg = sum(a_conc)/len(a_conc)
i=0
for conc in a_conc:
    a_conc[i] = (conc - avg) / avg*100
    i+=1

ax1.plot(slice_number,a_conc , color='blue',label='Afwijking tussen gem. van snede en gem. van totaal')
ax1.plot(slice_number,cov , color='green',label='CoV (= stdev(snede)/mean(snede))')
ax1.plot(slice_number,suv_ratio, color='blue',linestyle='--',label='SUV ratio')
ax1.axhline(10,color='red')
ax1.axhline(-10,color='red',label='Limieten')
ax1.axhline(0,color='black')

ax1.set_title('Uniformiteitstest PET')
ax1.set_ylabel('Afwijking [%]')
ax1.set_xlabel('Snede nummer')
ax1.legend(bbox_to_anchor=(0.5, -0.2, 0.5, 0.5))

fig1.savefig(os.path.join('Verwerkte EARLS',f'{filename}.pdf'))
