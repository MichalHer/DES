from des import DES
import sys
import numpy as np

def main(message_path, output_path, key, operation):
    with open(message_path, "r", encoding="utf-8") as f:
        msg = "".join(f.readlines())
        
    des = DES()
    
    if operation == "decryption":
        k = np.fromfile(key, dtype=int)
        des.set_key(k)
        decrypted_message = des.decrypt_message(msg)
        print("decrypted message:")
        print(decrypted_message)
            
    elif operation == "encryption":
        if key == None:
            k = des.create_key()
            k.tofile("key.deskey")
        else:
            k = np.fromfile(key, dtype=int)
            des.set_key(k)
        encrypted_message = des.encrypt_message(msg)
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(encrypted_message)
    
if __name__ == "__main__":
    input = None
    operation = None
    key = None
    output = "output.txt"
    
    
    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
DES encryption/decryption program.
usage: python main.py [option] ... [ -i input ] [ --encryption | --decryption ]
options and arguments:
-i --input      : Specifies input path
-o --output     : Specifies output path
-k --key        : Specifies key path
--encryption    : Message encryption
--decryption    : Message decryption
-h --help       : Displays help
""")
    
    for i, arg in enumerate(sys.argv):
        if arg in ["-i", "--input"]: input = sys.argv[i+1]
        if arg in ["-o", "--output"]: output = sys.argv[i+1]
        if arg in ["-k", "--key"]: key = sys.argv[i+1]
    
    if "--encryption" in sys.argv: operation = "encryption"
    if "--decryption" in sys.argv: operation = "decryption"
    
    if operation == None: 
        print("Operation (encryption/decryption) isn't specified.")
        exit()
    if input == None: 
        print("Input file isn't specified.")
        exit()
    if operation == "decryption" and key == None:
        print("Key isn't specified.")
        exit()
        
    main(input, output, key, operation)