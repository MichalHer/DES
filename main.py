from des import DES

with open("message.txt", "r", encoding='utf-8') as f:
    msg = "".join(f.readlines())

des = DES()
key = des.create_key()
encrypted_message = des.encrypt_message(msg)
decrypted_message = des.decrypt_message(encrypted_message)

with open("decrypted_message.txt", "w", encoding='utf-8') as f:
    f.writelines(decrypted_message)
    
with open("encrypted_message.txt", "w", encoding='utf-8') as f:
    f.writelines(encrypted_message)