def hexa_bin(block):
    hexa_block = []
    for i in range(len(block)):
        hex_row = []
        for j in range(len(block[i])):
            value = 0
            if block[i][j]:
                if i == 0 or not block[i - 1][j]:
                    value += 1
                if i == len(block) - 1 or not block[i + 1][j]:
                    value += 4
                if j == 0 or not block[i][j - 1]:
                    value += 8
                if j == len(block[i]) - 1 or not block[i][j + 1]:
                    value += 2
            hex_row.append(value)
        hexa_block.append(hex_row)
    return hexa_block


def bin_hexa(block):
    bin_block = []
    for i in range(len(block)):
        bin_row = []
        for j in range(len(block[i])):
            bin_row.append(block[i][j] > 0)
        bin_block.append(bin_row)
    return bin_block
