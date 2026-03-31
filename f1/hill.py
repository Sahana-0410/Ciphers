def gcd(a, b):
    """ Calculate the greatest common divisor using the Euclidean algorithm. """
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """ Calculate the modular inverse of a under modulo m using Extended Euclidean Algorithm. """
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def matrix_mod_inv(matrix, mod):
    """ Calculate the inverse of a 2x2 matrix under modulo. """
    det = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % mod
    inv_det = mod_inverse(det, mod)
    if inv_det is None:
        raise ValueError("Matrix is not invertible.")
    
    # Calculate inverse matrix
    inv_matrix = [
        [matrix[1][1] * inv_det % mod, -matrix[0][1] * inv_det % mod],
        [-matrix[1][0] * inv_det % mod, matrix[0][0] * inv_det % mod]
    ]
    
    # Convert negative values to positive under modulo
    for i in range(2):
        for j in range(2):
            inv_matrix[i][j] = inv_matrix[i][j] % mod
            
    return inv_matrix

def hill_cipher(plaintext, key_matrix):
    n = len(key_matrix)
    result_encrypted = ""
    result_decrypted = ""

    # Pad plaintext
    while len(plaintext) % n != 0:
        plaintext += 'x'  # Padding with 'x'

    print("\n--- Encryption Steps ---")
    for i in range(0, len(plaintext), n):
        block = [ord(ch) - ord('a') for ch in plaintext[i:i+n]]
        encrypted_block = [0] * n
        for j in range(n):
            for k in range(n):
                encrypted_block[j] += key_matrix[j][k] * block[k]
            encrypted_block[j] %= 26
        encrypted_text = ''.join(chr(value + ord('a')) for value in encrypted_block)
        result_encrypted += encrypted_text
        print(f"Processing block: {plaintext[i:i+n]} -> {block} -> Encrypted: {encrypted_text}")

    print(f"Final Hill Cipher Encrypted Output: {result_encrypted}")

    # Decryption
    print("\n--- Decryption Steps ---")
    key_matrix_inv = matrix_mod_inv(key_matrix, 26)
    
    for i in range(0, len(result_encrypted), n):
        block = [ord(ch) - ord('a') for ch in result_encrypted[i:i+n]]
        decrypted_block = [0] * n
        for j in range(n):
            for k in range(n):
                decrypted_block[j] += key_matrix_inv[j][k] * block[k]
            decrypted_block[j] %= 26
        decrypted_text = ''.join(chr(value + ord('a')) for value in decrypted_block)
        result_decrypted += decrypted_text
        print(f"Processing block: {result_encrypted[i:i+n]} -> {block} -> Decrypted: {decrypted_text}")

    print(f"Final Hill Cipher Decrypted Output: {result_decrypted}\n")
    return result_encrypted, result_decrypted

# Input
text = input("Enter the plaintext for Hill Cipher: ")
order = int(input("Enter the order of the key matrix (e.g., '2' for a 2x2 matrix): "))
print(f"Enter the {order}x{order} key matrix (enter it as space-separated values for each row):")

key_matrix = []
for i in range(order):
    row_values = list(map(int, input(f"Row {i + 1}: ").split()))
    key_matrix.append(row_values)

hill_cipher(text, key_matrix)
