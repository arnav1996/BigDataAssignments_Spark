from __future__ import print_function

import sys
from operator import add
from pyspark import SparkContext
from csv import reader

if __name__ == "__main__":
    sc = SparkContext()
    lines = sc.textFile(sys.argv[1], 1) #WILL READ OPEN_VIOLATIONS.CSV
    lines = lines.mapPartitions(lambda x: reader(x))

    req_col = lines.map(lambda line: (line[2],line[12]))
    initial = req_col.map(lambda x: (x[0], float(x[1])))
    sum_with_freq = initial.combineByKey(lambda value: (value, 1), lambda x, value: (x[0] + value, x[1] + 1), lambda x, y: (x[0] + y[0], x[1] + y[1]))
    
    average = sum_with_freq.map(lambda c:"%s\t%.2f, %.2f" %(c[0],c[1][0],c[1][0]/c[1][1]))
    average.saveAsTextFile("task3.out")

    sc.stop()
