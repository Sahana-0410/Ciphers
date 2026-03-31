def vigenere_cipher(plaintext, key):
    encrypted = ""
    decrypted = ""
    key_length = len(key)
    key_as_int = [ord(i) - ord('a') for i in key.lower() if i.isalpha()]
    plaintext_int = [ord(i) - ord('a') for i in plaintext.lower() if i.isalpha()]

    print("\n--- Encryption Steps ---")
    for i in range(len(plaintext_int)):
        shift = key_as_int[i % key_length]

        # Encryption
        encrypted_char = (plaintext_int[i] + shift) % 26 + ord('a')
        encrypted += chr(encrypted_char)
        print(f"Encrypting '{plaintext[i]}' with key '{key[i % key_length]}' to '{chr(encrypted_char)}'")

    print(f"Final Vigenère Cipher Output: {encrypted}")

    print("\n--- Decryption Steps ---")
    for i in range(len(plaintext_int)):
        shift = key_as_int[i % key_length]

        # Decryption
        decrypted_char = (ord(encrypted[i]) - ord('a') - shift + 26) % 26 + ord('a')
        decrypted += chr(decrypted_char)
        print(f"Decrypting '{encrypted[i]}' with key '{key[i % key_length]}' to '{chr(decrypted_char)}'")

    print(f"Final Vigenère Decrypted Output: {decrypted}\n")
    return encrypted, decrypted

# Input
text = input("Enter the plaintext for Vigenère Cipher: ")
key = input("Enter the key: ")
vigenere_cipher(text, key)
