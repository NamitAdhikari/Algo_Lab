def knapSackDynamic (cap, wt, val, n):
    table = [[0 for x in range(cap + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for j in range(cap + 1):

            if i == 0 or j == 0:
                table[i][j] = 0

            elif wt[i-1] <= j:
                table[i][j] = max(val[i-1] + table[i-1][j-wt[i-1]],  table[i-1][j])

            else:
                table[i][j] = table[i-1][j]

    return table[n][cap]




if __name__ == "__main__":

    # val = [50,100,150,200]
    # wt = [8,16,32,40]
    # W = 64

    # val = [60, 100, 120]
    # wt = [10, 20, 30]
    # W = 50

    # wt = [15, 10, 2, 4]
    # val = [30, 25, 2, 6]
    # W = 37

    wt = [10,20,30]
    val = [60,100,120]
    cap = 50

    n = len(val)

    print(f"Max Value is (Dynamic) : {knapSackDynamic(cap, wt, val, n)}")
