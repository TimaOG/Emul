binary_instruction = ((6 << 28) | (2 << 25) | (3 << 22) | (4 << 19) | (25))
print(format(binary_instruction, '032b'))
print('')
#00011011111010000000000000011001
dec1 = (binary_instruction & 0b11110000000000000000000000000000) >> 28
print(dec1)
dec2 = (binary_instruction & 0b00001110000000000000000000000000) >> 25
print(dec2)
dec3 = (binary_instruction & 0b00000001110000000000000000000000) >> 22
print(dec3)
dec4 = (binary_instruction & 0b00000000001110000000000000000000) >> 19
print(dec4)
dec5 = (binary_instruction & 0b00000000000001111111111111111111)
print(dec5)