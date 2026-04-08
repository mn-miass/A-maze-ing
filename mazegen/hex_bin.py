def bin_to_decimal(block):
    hexa_block = []
    for i in range(len(block)):
        hex_row = []
        for j in range(len(block[i])):
            value = 15
            if block[i][j]:
                if i != 0 and block[i - 1][j]:
                    value -= 1
                if i != len(block) - 1 and block[i + 1][j]:
                    value -= 4
                if j != 0 and block[i][j - 1]:
                    value -= 8
                if j != len(block[i]) and block[i][j + 1]:
                    value -= 2
            hex_row.append(value)
        hexa_block.append(hex_row)
    return hexa_block


def hexa_to_bin(block):
    bin_block = []
    for i in range(len(block)):
        bin_row = []
        for j in range(len(block[i])):
            bin_row.append(block[i][j] > 0)
        bin_block.append(bin_row)
    return bin_block

def decimal_to_hexa(block):
    hexa_block = []
    for i in range(len(block)):
        hexa_row = []
        for j in range(len(block[i])):
            if block[i][j] >= 0 and block[i][j] <= 9:
                hexa_row.append(block[i][j])
            elif block[i][j] == 10:
                hexa_row.append("A")
            elif block[i][j] == 11:
                hexa_row.append("B")
            elif block[i][j] == 12:
                hexa_row.append("C")
            elif block[i][j] == 13:
                hexa_row.append("D")
            elif block[i][j] == 14:
                hexa_row.append("E")
            elif block[i][j] == 15:
                hexa_row.append("F")
        hexa_block.append(hexa_row)
    return hexa_block
