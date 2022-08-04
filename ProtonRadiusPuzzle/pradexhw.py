# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 09:12:02 2022

@author: admin
"""

"""
Reading the pradex.dat file to plot the data contained 
according to the function of the proton radius. 
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.optimize import minimize

col_names =  ["Q2", "G_E", "dG_E"] # Originally ["Q^2[fm^-2]", "G_E", "dG_E (sigma)"]  
# Need to use explicit column names so "(sigma)" isn't counted as an entire new field
# becuase the delimiter is just a space (" ")

with open('pradex.dat', 'r') as pradex:
    next(pradex)     # To skip the column names and get straight to the data values
    data = list(csv.DictReader(pradex, fieldnames = col_names, delimiter=" "))
    # created a list so we can access individual elements when needed

    # Separate the columns into their own lists so we can graph them
    Q2_list = []
    GE_list = []
    GE_error = []
    weight = []
    for line in data:
        Q2_list.append(float(line['Q2']))     # Need float to add error bars
        GE_list.append(float(line['G_E']))
        GE_error.append(float(line['dG_E']))

    print(GE_error)
    wQ2_list = []
    wGE_list = []
    for i in range(len(GE_error)):
        # wQ2_list.append(Q2_list[i])
        # wGE_list.append(GE_list[i])
        w = 1/GE_error[i]
        for d in range(0, int(w), 1):
            wQ2_list.append(Q2_list[i])
            wGE_list.append(GE_list[i])
    print(Q2_list, GE_list)
    
    fig, ([ax1, ax2], [ax3, ax4]) = plt.subplots(2, 2, figsize=(10,6), sharex='col', sharey='row', constrained_layout=True)
    fig.supxlabel(r"$Q^2~\left[\mathrm{fm}^{-2}\right]$", fontsize=14)
    fig.supylabel(r"$G_E~\left[\mathrm{Q}^2\right]$", fontsize=14)
    fig.suptitle("Regressions on L. Hand Data", fontsize=18)
    
    # Constructing and plotting linear regression for the weighted one
    regw = stats.linregress(wQ2_list, wGE_list)
    x = np.arange(0, 3, 0.1)     # also used later
    y = x*regw.slope + regw.intercept
    ax2.plot(x, y, color='blue', label = "Brute Force Weighted")
    ax2.legend(fontsize=12)
    
    # Unweighted regression
    reg = stats.linregress(Q2_list, GE_list)
    y = x*reg.slope + reg.intercept
    ax1.plot(x, y, color='red', label='Unweighted')
    ax1.legend(fontsize=12)
    
    
    # Plot the figure with error bars    
    ax1.scatter(Q2_list, GE_list, color='black')
    ax2.scatter(Q2_list, GE_list, color='black')
    ax3.scatter(Q2_list, GE_list, color='black')
    ax4.scatter(Q2_list, GE_list, color='black')
    ax1.errorbar(Q2_list, GE_list, yerr = GE_error, fmt = 'o', capsize = 2, color='black')
    ax2.errorbar(Q2_list, GE_list, yerr = GE_error, fmt = 'o', capsize = 2, color='black')
    ax3.errorbar(Q2_list, GE_list, yerr = GE_error, fmt = 'o', capsize = 2, color='black')
    ax4.errorbar(Q2_list, GE_list, yerr = GE_error, fmt = 'o', capsize = 2, color='black')
    

    """
    Now I also want to try doing this with an acutal weighted least squares algorithm,
    so I'm gonna try that
    """
    
    # This gets the slope and intercept from a REAL weighted least squares function YAY!!!
    wIntercept, wSlope = np.polynomial.polynomial.polyfit(Q2_list, GE_list, 1, w = [1.0 / dG for dG in GE_error], full=False)
    y = x*wSlope + wIntercept
    ax3.plot(x, y, color='orange', label='Weighted LSRL')
    ax3.legend(fontsize=12)

    # Trying a Quadratic Fit
    wIntercept, w1, w2 = np.polynomial.polynomial.polyfit(Q2_list, GE_list, 2, w = [1.0 / dG for dG in GE_error], full=False)
    y2 = w2*(x**2) + x*w1 + wIntercept
    ax4.plot(x, y2, color='green', label='Weighted Quadratic')
    ax4.legend(fontsize=12)
    
    # Derivative of the quadratic fit at Q^2 = 0 (to get slope)
    # deriv(y2) = 2*w2*x + w1
    # x = 0, so
    derivq0 = w1
    
    r = np.sqrt(-6*w1)
    print(r)
    
    plt.show()
    
    