from Crypto.Cipher import AES
import itertools
import string
import time

# Load the assignment ciphertext and nonce
with open("ciphertext", "rb") as f:
    ciphertext = f.read()

with open("nonce", "rb") as f:
    nonce = f.read()

# Define the target plaintext pattern if known (e.g., "[REDACTED(ha ha!)]")

# Optimized brute-force function with timing
def brute_force_aes(ciphertext, nonce):
    start_time = time.time()
    print("Brute-force attack started at:", time.ctime(start_time))
    
    target_pattern = b'[REDACTED'  # Known pattern in plaintext for validation
    
    # Generate 6-letter combinations only once
    for combo in itertools.product(string.ascii_uppercase, repeat=6):
        # Build the 24-byte key directly
        key_string = ''.join(combo) * 4  # Repeat the 6-char string 4 times
        key = key_string.encode('utf-8')  # Convert to bytes
        
        try:
            # Initialize cipher once per key and try to decrypt the ciphertext
            cipher_dec = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher_dec.decrypt(ciphertext)
            
            # Check for expected plaintext pattern for verification
            if target_pattern in plaintext:
                end_time = time.time()
                print("Key found:", key_string)
                print("Plaintext:", plaintext.decode())
                print("Brute-force attack ended at:", time.ctime(end_time))
                print("Total time taken:", end_time - start_time, "seconds")
                return key_string, plaintext.decode()
        
        except (ValueError, UnicodeDecodeError):
            # Skip if decryption fails (ValueError) or plaintext is not readable (UnicodeDecodeError)
            continue

    end_time = time.time()
    print("Key not found")
    print("Brute-force attack ended at:", time.ctime(end_time))
    print("Total time taken:", end_time - start_time, "seconds")
    return None

# Run the brute-force function
brute_force_aes(ciphertext, nonce)
