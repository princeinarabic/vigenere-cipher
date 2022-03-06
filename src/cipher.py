import sys
import math


eng_letter_freqs = {'A': 0.08167,'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228, 'G': 0.02015,
                    'H': 0.06094,'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 
                    'O': 0.07507,'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056, 'U': 0.02758,
                    'V': 0.00978,'W': 0.02360, 'X': 0.00150, 'Y': 0.01974, 'Z': 0.00074}


def chi_sq(expected, observed):
    return (observed - expected)**2 / expected

def letter_to_pos(letter):
    return ord(letter) - ord('A')

def pos_to_letter(pos):
    return chr(pos + ord('A'))


class Vigenere:
    def __init__(self, data, key):
        self.data = data.upper()
        self.key = key.upper()
        self.encrypted_message = ''
        self.decrypted_message = ''


    # an argument 'dir' is either +1 for encryption, or -1 for decryption.
    def encrypt_or_decrypt(self, dir):
        idx = 0
        for c in self.data:
            if 'A' <= c <= 'Z':
                number = (letter_to_pos(c) + dir * 
                          letter_to_pos(self.key[idx % len(self.key)])) % 26

                if dir == 1:
                    self.encrypted_message += pos_to_letter(number) 
                if dir == -1:
                    self.decrypted_message += pos_to_letter(number)
                idx += 1

            else:
                if dir == 1:
                    self.encrypted_message += c
                elif dir == -1:
                    self.decrypted_message += c


    def decrypt_with_every_possible_key(self, keys):
        smallest_stat = math.inf
        best_text = ''

        for k in keys:
            self.key = k
            self.encrypt_or_decrypt(-1)

            observed_freqs = self.string_frequency_analysis(self.decrypted_message)
            current_stat = 0
            for f in range(len(observed_freqs)):
                current_stat += chi_sq(eng_letter_freqs[pos_to_letter(f)], observed_freqs[f])
            
            if current_stat < smallest_stat:
                smallest_stat = current_stat
                best_text = self.decrypted_message
            
            self.decrypted_message = ''
            
        return best_text


    # shifts a given letter by the given shift value
    def decrypt_caesar_letter(self, letter, shift):
        return pos_to_letter((letter_to_pos(letter) + shift) % 26)     


    # this function will return a *letter* that will be one of the letters of the Vigenere cipher KEY 
    def suitable_key_for_caesar(self, observed_letter_frequencies):
        smallest_statistic = math.inf
        optimal_shift = 0

        for shift in range(26):  # testing all 26 possible shifts for a given string e.g "LOME" from LXFOPV MH OEIB
            current_statistic = 0
            for f in range(len(observed_letter_frequencies)):
                decrypted_caesar_letter = self.decrypt_caesar_letter(pos_to_letter(f), shift)
                current_statistic += chi_sq(eng_letter_freqs[decrypted_caesar_letter], observed_letter_frequencies[f])
            
            if current_statistic < smallest_statistic:
                smallest_statistic = current_statistic
                optimal_shift = shift
        
        return pos_to_letter((26 - optimal_shift) % 26)


    # this function returns a list of frequencies for each letter in the string 
    # the function evaluates one string at a time
    def string_frequency_analysis(self, str):
        letter_freq = [0] * 26
        for c in str:
            if 'A' <= c <= 'Z':
                letter_freq[letter_to_pos(c)] += 1            
        return letter_freq


    def form_letters_at_indices(self, key_len):
        letters_at_indices = [''] * key_len   
        idx = 0
        for c in self.data:
            if 'A' <= c <= 'Z':
                letters_at_indices[idx % key_len] += c
                idx += 1
        return letters_at_indices

    
    def decrypt_without_key(self):
        self.potential_keys = []  
        
        for key_len in range(1, 21):
            potential_key = ''
            letters_at_indices = self.form_letters_at_indices(key_len)      

            for cipher in letters_at_indices:  # looking at each string as a separate caesar cipher
                observed_letter_frequencies = self.string_frequency_analysis(cipher)
                potential_key += self.suitable_key_for_caesar(observed_letter_frequencies)

            self.potential_keys.append(potential_key)
            
        print(self.decrypt_with_every_possible_key(self.potential_keys))


    def output_encryption(self):
        print(self.encrypted_message.strip())

    def output_decryption(self):
        print(self.decrypted_message.strip())

    

def read_file_content(file):
    with open(file, 'r') as f: 
        return f.read()


def argument_error():
    print('usage: cipher.py <filename> <-e | -d> [key]')
    print('-e: encrypt')
    print('-d: decrypt')


def main():
    if len(sys.argv) < 3:
        argument_error()
        quit()
  
    file = sys.argv[1]
    task = sys.argv[2]

    key = ''
    if len(sys.argv) == 4:
        key = sys.argv[3]

    file_content = read_file_content(file)
    v = Vigenere(file_content, key)

    if task == '-e':
        if key == '':
            argument_error()
            print('Specify the [key]')
            quit()
        else:
            v.encrypt_or_decrypt(1)    
            v.output_encryption()

    if task == '-d':
        if key != '':
            v.encrypt_or_decrypt(-1)
            v.output_decryption()
        else:
            v.decrypt_without_key()


if __name__ == '__main__':
    main()