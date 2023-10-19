from morse_decoder import Morse_Decoder
from morse_generator import Morse_Generator
import sounddevice as sd
import os
from scipy.io import wavfile


class Morse:
    def __init__(self, generator, decoder) :
        self.generator = generator
        self.decoder = decoder

    def add_letter(self, letter, symbole) :
        '''
        Add a letter to both of the generator and decorator
        '''
        self.generator.add_letter(letter, symbole)
        self.decoder.add_symbole(symbole, letter)

    def remove_letter(self, letter, symbole) :
        '''
        Remove a letter related to a symbole from both list
        '''
        self.generator.remove_letter(letter)
        self.generator.remove_letter(symbole)
    
    def generate(self, sentence) :
        '''
        Generate a morse code in wav file and read it
        '''
        self.generator.generate_file(sentence)

    def play_file(self) :
        """
        Play the morse sound file
        """
        samplerate, data = wavfile.read('morse.wav')    
        sd.play(data, samplerate)
        sd.wait()

    def print_phrase(self) :
        """
        Show the sentence in morse symbole
        """
        self.generator.print_phrase()

    def print_morse_phrase(self, sentence) :
        """
        Show the morse code in a sentence
        """
        self.decoder.decode_sentence(sentence)

    def decode(self, wav_file) :
        '''
        Decode the sentence stored in the wav file
        '''
        self.decoder.decode_file(wav_file)

if __name__ == '__main__' :
    morse = Morse(Morse_Generator(22050), Morse_Decoder())
    print("Ceci est une application de traduction morse <-> alphabète, que souhaitez-vous faire ?")
    while(True) :
        print("(1) Alphabète -> Morse")
        print("(2) Morse -> Alphabète")
        print("(3) Faire jouer le son en morse")        
        print("(quit) Quitter l'application")

        x = input("Entrez l'action souhaitée : ")
        if x == "1" :
            sentence = input("Entrez la phrase que vous souhaitez traduire : ")
            morse.generate(sentence)
            morse.print_phrase()
        elif x == "2" :
            print("Attention, les seuls symboles utilisables sont ceux de l'alphabète")
            print("Voici les symboles utilisables : ")
            print(". -> un bip court")
            print("_ -> un bip  long")
            print("  -> un espace entre lettres")
            print("- -> un espace entre mots")
            sentence = input("Entrez votre code morse : ")
            morse.print_morse_phrase(sentence)
        elif x == "3" :
            if os.path.exists("morse.wav") :
                morse.play_file()
            else : 
                print("Vous devez d'abord générer le fichier en demande de traduire une phrase")
        elif x == "quit" :
            break