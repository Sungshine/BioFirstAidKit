def find_kmers(string, k):
    kmers = []
    n = len(string) #5000000, k=11,

    for i in range(0, n - k + 1):
        kmers.append(string[i:i + k])

    return kmers