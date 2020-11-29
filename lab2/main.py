from random import sample
from time import time
from insert import insertionSort
from merge import mergeSort
import matplotlib.pyplot as plt

def runInsert(n):
    data = sample(range(n+1), n)

    start_time = time()*1000
    insertionSort(data)
    end_time = time()*1000

    time_taken_insertion = end_time - start_time
    print(f"\nTime taken for insertion sort of {n} data = {time_taken_insertion} ms")

    return time_taken_insertion

def runMerge(n):
    data = sample(range(n+1), n)

    start_time = time()*1000
    mergeSort(data, 0, len(data) - 1)
    end_time = time()*1000

    time_taken_merge = end_time - start_time
    print(f"Time taken for merge sort of {n} data = {time_taken_merge} ms")

    return time_taken_merge


if __name__ == "__main__":

    inpSize = []
    execTimeInsert = []
    execTimeMerge = []

    i = 100000
    # for i in range(0, 25001, 5000):
    inpSize.append(i)
    execTimeInsert.append(runInsert(i))
    execTimeMerge.append(runMerge(i))

    plt.xlabel("Input Size")
    plt.ylabel("Execution Time")
    plt.plot(inpSize, execTimeInsert, label="Insertion Sort")
    plt.plot(inpSize, execTimeMerge, label="Merge Sort")
    plt.legend()
    plt.show()
