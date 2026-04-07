from shapes import Shapes

class GenerateNumber():
    def add_blocks(self, block_a, block_b):
        added_block = []
        for i in range(len(block_a)):
            row_block = []
            for j in range(len(block_a[i])):
                row_block.append(block_a[i][j])
            row_block.append(False)
            for j in range(len(block_b[i])):
                row_block.append(block_b[i][j])
            added_block.append(row_block)
        return added_block
    
