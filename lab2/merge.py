def mergeSort(data, p, r):
    if p < r:
        q = int((p+r-1)/2)

        mergeSort(data, p, q)
        mergeSort(data, q + 1, r)
        merge(data, p, q, r)


def merge(data, p, q, r):
    n1 = q - p + 1
    n2 = r - q

    L = [0] * (n1)
    R = [0] * (n2)

    for i in range(n1):
        L[i] = data[p + i]
    for j in range(n2):
        R[j] = data[q + j + 1]

    i = 0
    j = 0
    k = p

    while (i < n1 and j < n2):
        if (L[i] <= R[j]):
            data[k] = L[i]
            i += 1
        else:
            data[k] = R[j]
            j += 1
        k += 1

    while (i < n1):
        data[k] = L[i]
        i += 1
        k += 1

    while (j < n2):
        data[k] = R[j]
        j += 1
        k += 1


if __name__ == "__main__":
    data = []
    data = [int(x) for x in input("Enter elements to sort: ").split()]

    length = len(data)
    mergeSort(data, 0, length-1)

    print("The sorted elements are: ", end=" ")
    for x in data:
        print(x, end=" ")
