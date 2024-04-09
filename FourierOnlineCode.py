from presentation import *
import numpy as np
import os
import matplotlib.pyplot as plt
import csv

file_path = 'C:\\Users\\abhig\\Desktop'

os.chdir(file_path)

file_name = 'AMLFourier-simplified-01-01.jpg'

time_table, x_table, y_table = create_close_loop(file_name)
plt.plot(x_table, y_table)
plt.show()

order = 190 # We need higher order approximation to get better approximation
coef = coef_list(time_table, x_table, y_table, order)
print(coef)

for i in range(len(coef)):
    freq = i - order
    freq = np.abs(freq)
    if freq == 0:
        continue
    else:
        x = freq*np.pi/(order + 1)
        sigma = np.sin(x)/x
        coef[i][0] *= sigma*sigma
        coef[i][1] *= sigma*sigma


space = np.linspace(0, tau, 300) # Did you know what tau is ? Check my previous video about it ! :D
x_DFT = [DFT(t, coef, order)[0] for t in space]
y_DFT = [DFT(t, coef, order)[1] for t in space]


fig, ax = plt.subplots(figsize=(5, 5))
ax.plot(x_DFT, y_DFT, 'r--')
ax.plot(x_table, y_table, 'k-')
ax.set_aspect('equal', 'datalim')
xmin, xmax = xlim()
ymin, ymax = ylim()
plt.show()

##
##anim = visualize(x_DFT, y_DFT, coef, order, space, [xmin, xmax, ymin, ymax])
##Writer = animation.writers['html']
##writer = Writer(fps=60)
##anim.save('komodo.html',writer=writer, dpi=150)

data = []

for i in range(len(coef)):
    amp = np.sqrt(coef[i][0]**2 + coef[i][1]**2)
    phase = np.arctan2(coef[i][1],coef[i][0])
    freq = i - order
    row = [amp, phase, freq]
    data.append(row)
    if i%10 == 0:
        print(i)

# opening the csv file in 'w+' mode 
file = open('aml3.csv', 'w+', newline ='') 
  
# writing the data into the file 
with file:     
    write = csv.writer(file) 
    write.writerows(data)
