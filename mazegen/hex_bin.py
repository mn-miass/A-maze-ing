NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


def decimal_to_bin(block: list[list[int]]) -> list[list[int]]:
    """
    Converts a decimal grid to a binary grid (0 or 1).

    Args:
        block: 2D grid of integers.

    Returns:
        2D grid of 0s and 1s.
    """
    result = []
    for i in range(len(block)):
        row = []
        for j in range(len(block[i])):
            if block[i][j] > 0:
                row.append(1)
            else:
                row.append(0)
        result.append(row)
    return result


def decimal_to_hexa(block: list[list[int]]) -> list[list[str]]:
    """
    Converts a decimal grid to a hexadecimal character grid.

    Each value (0-15) maps to its hex character (0-9, A-F).

    Args:
        block: 2D grid of integers (0-15).

    Returns:
        2D grid of hex characters.
    """
    result = []
    for i in range(len(block)):
        row = []
        for j in range(len(block[i])):
            row.append(format(block[i][j], 'X'))
        result.append(row)
    return result
