# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 09:52:34 2022

@author: admin
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
import math

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

cols = ['x', 'y1', 'y2', 'y3', 'x4', 'y4', 'dy']

with open('homework2.dat', 'r') as hw2:
    next(hw2)
    data = list(csv.DictReader(hw2, fieldnames=cols, delimiter=" "))
    
    x, y1, y2, y3, x4, y4, dy = [], [], [], [], [], [], []
    for line in data:
        x.append(float(line['x'])) 
        y1.append(float(line['y1']))
        y2.append(float(line['y2']))
        y3.append(float(line['y3']))
        x4.append(float(line['x4']))
        y4.append(float(line['y4']))
        dy.append(float(line['dy']))
        
        
    int1, slope1 = np.polynomial.polynomial.polyfit(x, y1, 1, w= [1/i for i in dy], full=False)
    int2, slope2 = np.polynomial.polynomial.polyfit(x, y2, 1, w= [1/i for i in dy], full=False)
    int3, slope3 = np.polynomial.polynomial.polyfit(x, y3, 1, w= [1/i for i in dy], full=False)
    int4, slope4 = np.polynomial.polynomial.polyfit(x4, y4, 1, w= [1/i for i in dy], full=False)
    
    dx = np.arange(0,20,0.1)
    pred1, pred2, pred3, pred4 = [], [], [], []
    for i in dx:
        pred1.append(i*slope1 + int1)
        pred2.append(i*slope2 + int2)
        pred3.append(i*slope3 + int3)
        pred4.append(i*slope4 + int4)

    fig, ax = plt.subplots(2, 2, figsize=(10,7), constrained_layout=True)
    fig.suptitle("Homework 2: Equivalent Regressions", fontsize=18)
    
    ax[0][0].errorbar(x, y1, yerr = dy, fmt = 'o', capsize = 2, color='brown')
    ax[0][0].plot(dx, pred1)
    ax[0][0].set_ylabel('$y_1$', fontsize=14)
    ax[0][0].set_xlabel('$x_1$', fontsize=14)
    
    ax[0][1].errorbar(x, y2, yerr = dy, fmt = 'o', capsize = 2, color='blue')
    ax[0][1].plot(dx, pred2)
    ax[0][1].set_ylabel('$y_2$', fontsize=14)
    ax[0][1].set_xlabel('$x_2$', fontsize=14)

    ax[1][0].errorbar(x, y3, yerr = dy, fmt = 'o', capsize = 2, color='red')
    ax[1][0].plot(dx, pred3)
    ax[1][0].set_ylabel('$y_3$', fontsize=14)
    ax[1][0].set_xlabel('$x_3$', fontsize=14)

    ax[1][1].errorbar(x4, y4, yerr = dy, fmt = 'o', capsize = 2, color='green')
    ax[1][1].plot(dx, pred4)
    ax[1][1].set_ylabel('$y_4$', fontsize=14)
    ax[1][1].set_xlabel('$x_4$', fontsize=14)

                
    print("Weighted LSRL for \ny1: \nSlope= " + str(truncate(slope1, 3))
              + "\ty-intercept= " + str(truncate(int1, 3)) + "\ny2: \nSlope= " + str(truncate(slope2, 3))
              + "\ty-intercept= " + str(truncate(int2, 3)) + "\ny3: \nSlope= " + str(truncate(slope3, 3))
              + "\ty-intercept= " + str(truncate(int3, 3)) + "\ny4: \nSlope= " + str(truncate(slope4, 3))
              + "\ty-intercept= " + str(truncate(int4, 3)))
    
    plt.show()