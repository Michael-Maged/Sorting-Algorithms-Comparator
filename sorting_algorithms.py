def insertionSort(arr):
    t = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        t += 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            t += 2
        arr[j + 1] = key
    return t

def bubbleSort(arr):
    t = 0
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            t += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                t += 1
    return t

def merge(arr, l, m, r, t):
    s1 = m - l + 1
    s2 = r - m
    L = arr[l:l + s1]
    R = arr[m + 1:m + 1 + s2]
    
    t += s1 + s2
    
    i, j, k = 0, 0, l
    while i < s1 and j < s2:
        t += 1
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < s1:
        arr[k] = L[i]
        i += 1
        k += 1
        t += 1

    while j < s2:
        arr[k] = R[j]
        j += 1
        k += 1
        t += 1
    
    return t

def mergeSortWrapper(arr, l, r, t):
    if l >= r:
        return t
    m = l + (r - l) // 2
    t = mergeSortWrapper(arr, l, m, t)
    t = mergeSortWrapper(arr, m + 1, r, t)
    t = merge(arr, l, m, r, t)
    
    return t

def mergeSort(arr):
    return mergeSortWrapper(arr, 0, len(arr) - 1, 0)

def partition(arr, l, h, t):
    x = arr[h]
    t += 1
    i = l - 1
    for j in range(l, h):
        t += 1
        if arr[j] <= x:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            t += 1
    arr[i + 1], arr[h] = arr[h], arr[i + 1]
    t += 1
    return i + 1, t

def quickSortWrapper(arr, l, h, t):
    if l < h:
        q, t = partition(arr, l, h, t)
        t = quickSortWrapper(arr, l, q - 1, t)
        t = quickSortWrapper(arr, q + 1, h, t)
    
    return t

def quickSort(arr):
    return quickSortWrapper(arr, 0, len(arr) - 1, 0)

def heapify(arr, n, i, t):
    l = 2 * i + 1
    r = 2 * i + 2
    largest = i
    if l < n and arr[l] > arr[i]:
        largest = l
        t += 1
    if r < n and arr[r] > arr[largest]:
        largest = r
        t += 1
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        t += 1
        t = heapify(arr, n, largest, t)
        
    return t

def heapSort(arr):
    n = len(arr)
    t = 0
    for i in range(n // 2 - 1, -1, -1):
        t = heapify(arr, n, i, t)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        t += 1
        t = heapify(arr, i, 0, t)
        
    return t

def selectionSort(arr):
    t = 0
    for i in range(len(arr) - 1):
        minIndex = i
        t += 1
        for j in range(i + 1, len(arr)):
            t += 1
            if arr[j] < arr[minIndex]:
                minIndex = j
                t += 1
        if minIndex != i:
            arr[i], arr[minIndex] = arr[minIndex], arr[i]
            t += 1
    return t
