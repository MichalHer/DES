import numpy
from . import tables
from .defines import CHUNK_SIZE, RANDOM_NUMBERS
from random import randint
from tqdm import tqdm

class DES:
    _key: numpy.array
    
    def encrypt_message(self, msg:str, reverse:bool=False) -> str:
        if not hasattr(self, "_key"): 
            raise Exception("Key is not setted!")
        
        chunks = self.__create_chunks(msg)
        encrypted_chunks = []
        middle_key = self.__apply_permutation(self._key, tables.key_permutation_pc1)
        keys = self.__make_key_set(middle_key)
        
        if reverse == True: keys = keys[::-1]
    
        
        for idx, chunk in enumerate(tqdm(chunks, desc="Encryption" if reverse == False else "Decryption")):
 
            initial_permutation = self.__apply_permutation(chunk, tables.initial_permutation)
      
            
            splitted_chunk = numpy.array_split(initial_permutation, 2)

            left_part = splitted_chunk[0].copy()
            right_part = splitted_chunk[1].copy()
            
            for round in range(16):

                key = keys[round]
                fiesteled_right_part = self.__apply_feistels(right_part, key)
                xored_left = numpy.logical_xor(left_part, fiesteled_right_part).astype(int)
                
                if round != 15:
                    left_part = right_part.copy()
                    right_part = xored_left.copy()
                else:
                    left_part = xored_left.copy()
                

                
                encrypted_chunk = numpy.concatenate([left_part, right_part], dtype='int')

                
            encrypted_chunk = self.__apply_permutation(encrypted_chunk, tables.final_permutation)

            encrypted_chunks.append(encrypted_chunk.copy())
        
        encrypted_chunks = numpy.array(encrypted_chunks)
        return self.__translate_chunks_to_text(encrypted_chunks)
            
    def __apply_feistels(self, chunk:numpy.array, key:numpy.array):
        expanded_chunk = self.__apply_permutation(chunk, tables.expansion_permutation)

        
        xored_chunk = numpy.logical_xor(expanded_chunk, key).astype(int)

        
        sbox_chunks = numpy.array_split(xored_chunk, len(tables.sboxes))

        sbox_chunks_after_sbox_processing = []

        
        for sbox, sbox_chunk in zip(tables.sboxes, sbox_chunks):


            post_process_chunk = self.__apply_sbox(sbox_chunk, sbox)

            sbox_chunks_after_sbox_processing.append(post_process_chunk.copy())
        

        chunk_after_sbox_processing = numpy.concatenate(sbox_chunks_after_sbox_processing)

        chunk_p_permutation = self.__apply_permutation(chunk_after_sbox_processing, tables.p_permutation)

        return chunk_p_permutation
    
    def decrypt_message(self, msg:str) -> str:
        return self.encrypt_message(msg, reverse=True)

    def __make_key_set(self, key:numpy.array) -> numpy.array:
        result = []
        for round in range(16):
            result.append(self.__prepare_key(key,round))
        return numpy.array(result)
    
    def __prepare_key(self, key:numpy.array, round:int) -> numpy.array:

        prepared_key=[]
        shift_positions = sum(tables.shift[:round+1])

        
        splitted_key = numpy.array(numpy.split(key, 2))

        
        for part in splitted_key:
            prepared_key.append(numpy.roll(part, -shift_positions).copy())
            
        prepared_key = numpy.concatenate(prepared_key)

        
        prepared_key = self.__apply_permutation(prepared_key, tables.key_permutation_pc2)

        return prepared_key
                                 
    def __apply_sbox(self, chunk:numpy.array, sbox:numpy.array) -> numpy.array:
        if len(chunk) != 6: raise Exception ("Chunk to sbox processing is invalid")
        
        row = int(f'{chunk[0]}{chunk[5]}',2)
        col = int(f'{"".join(str(x) for x in chunk[1:5])}',2)
        
        splitted_sbox = numpy.array_split(sbox,4)
        decimal_result = splitted_sbox[row][col]
        bin_result_string = bin(decimal_result).replace("0b", "").zfill(4)
        
        return numpy.array(list(bin_result_string), dtype="int")
    
    def __apply_permutation(self, chunk:numpy.array, permutation_table:numpy.array) -> numpy.array:
        returned_chunk = numpy.zeros(len(permutation_table), dtype="int")
        for idx, position in enumerate(permutation_table):
            returned_chunk[idx] = chunk[position]
        return returned_chunk
    
    def __create_chunks(self, message:str) -> numpy.array:
        random_numbers = (1 if RANDOM_NUMBERS == True else 0)
        text_binary = "".join(format(ord(i), '08b') for i in message)
        missing_end = len(text_binary)%CHUNK_SIZE
        if missing_end != 0:
            for _ in range(CHUNK_SIZE-missing_end): text_binary += str(randint(0,random_numbers))
        text_array = list(text_binary)
        text_array = numpy.array(text_array, dtype='int')
        return numpy.array(numpy.array_split(text_array,len(text_binary)/CHUNK_SIZE))
    
    def __translate_chunks_to_text(self, chunks:numpy.array) -> str:
        result = ""
        for chunk in chunks:
            letters = numpy.array_split(chunk, 8)
            for letter in letters:
                result += self.__binary_array_to_letter(letter)
        return result
                
    def __binary_array_to_letter(self, binary_array:numpy.array) -> str:
        binary_string = "".join([str(x) for x in binary_array])
        binary_int = int(binary_string,2)
        return chr(binary_int)

    def create_key(self) -> numpy.array:

        initial_array = numpy.random.randint(0,2, size=CHUNK_SIZE)
        self._key = initial_array

        return self._key
        
    def set_key(self, key:numpy.array):
        self._key = key