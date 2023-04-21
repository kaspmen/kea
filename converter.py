
def conv_hex_to_dec(xyzfoo):
    xyzfoo_str = str(xyzfoo)
    xyzfoo_chunks = [xyzfoo_str[i:i+8][:2] for i in range(0, len(xyzfoo_str), 8)]

    idMaterials = []
    try:
        for hex_num in xyzfoo_chunks:

            if hex_num.startswith('0'):
                hex_num = hex_num[1:]
            idMaterials.append(int(hex_num, 16))
    except ValueError:
        print(f"Error: {hex_num} is not a valid hexadecimal number")

    # print(idMaterials)
    return idMaterials