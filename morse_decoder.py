import numpy as np
import sounddevice as sd
import soundfile as sf
import scipy.signal as scs
import scipy.io.wavfile as scw
import matplotlib.pyplot as plt
import wave
import struct

class Morse_Decoder :
    # échantillonage : ~22050
    # Un point tous les (fréquence d'échantillonage) : 1/22050
    # fréquence du signal : 440
    # Bip court : 200 ms
    # Bip long : 600 ms
    # Silence entre chaque symbole : 200 ms
    # Silence entre lettre : 600 ms
    # Silence entre mot : 1000 ms

    def __init__(self) :
        self.letters = {
            "._" : "A",
            "_..." : "B",
            "_._." : "C",
            "_.." : "D",
            "." : "E",
            ".._." : "F",
            "__." : "G",
            "...." : "H",
            ".." : "I",
            ".___" : "J",
            "_._" : "K",
            "._.." : "L",
            "__" : "M",
            "_." : "N",
            "___" : "O",
            ".__." : "P",
            "__._" : "Q",
            "._." : "R",
            "..." : "S",
            "_" : "T",
            ".._" : "U",
            "..._" : "V",
            ".__" : "W",
            "_.._" : "X",
            "_.__" : "Y",
            "__.." : "Z"
        }

    def decode_sentence(self, sentence) :
        """
        Decode the sybomles into a sentence
        """
        final_sentence = []
        tmp_sentence = ""

        # Analyse the sound received and translate it
        for symbole in sentence :
            if symbole == "-" :
                if tmp_sentence != "" :
                    try :
                        final_sentence.append(self.letters[tmp_sentence])
                    except KeyError as e:
                        print("Le symbole n'existe pas ", e)                 
                final_sentence.append(" ")
                tmp_sentence = ""
            elif symbole == " " :
                if tmp_sentence != "" :
                    try :
                        final_sentence.append(self.letters[tmp_sentence])
                    except KeyError as e:
                        print("Le symbole n'existe pas ", e)  
                tmp_sentence = ""
            else : 
                tmp_sentence += symbole
        if tmp_sentence != "" :
            try :
                final_sentence.append(self.letters[tmp_sentence])
            except KeyError as e:
                print("Le symbole n'existe pas ", e)  

        # Construct the final string message
        final_message = ""
        for letter in final_sentence :
            final_message += letter

        
        return final_message.lower().capitalize()

    def decode_file(self, wav_file) :
        """
        Decode the sentence from the received file
        """
        
        # Saut de 1 dans le tableau
        # Si la valeur est > ~0.6, place un indice à i        0.6 = delta
        # Checker tous les 60 points si le threshold est dépassé
        # Tous les 60 points -> 22050/440 : si un threshold est dépassé on est toujours dans un son
        # Sinon on est dans un silence
        # T = (différence des indices * 1/22050) => durée du bip (à faire attention -> +- 10%)
        # Selon les normes mises en places

        # Pour le silence pareil, mais il faut checker si x ==> 1

        Fs, x = scw.read(wav_file) # Fs non-utilisé

        # Normalisé
        x = x / np.max(np.abs(x))
        x = x*x

        plt.figure()
        plt.plot(x)
        plt.show()

        start_sound_index = 0
        start_blank_index = 0

        sentence = ""

        for i in range(12, len(x), 25) :
            if x[i] > 0 :
                if start_sound_index == 0 :
                    start_sound_index = i
                # Compte le temps de silence
                if start_blank_index != 0 :
                    T = ((i - start_blank_index) * 1/22050) * 1000 # Temps d'un son
                    if T >= 550 and T <= 850 :
                        sentence += " " # Espace entre lettres
                    elif T >= 1000 and T <= 2000 :
                        sentence += "-" # Espace entre mots
                    start_blank_index = 0
            elif x[i] <= 0 :                
                if start_blank_index == 0 :
                    start_blank_index = i
                # Compte le temps de son
                if start_sound_index != 0 :
                    T = ((i - start_sound_index) * 1/22050) * 1000 # Temps d'un son
                    if T <= 200 + 200*10/100 and T >= 200 - 200*10/100 :
                        sentence += "."
                    elif T <= 600 + 600*10/100 and T >= 600 - 600*10/100 :
                        sentence += "_"
                    start_sound_index = 0

        print("Morse : ", sentence)
        print("Traduction : ", self.decode_sentence(sentence))

    def add_symbole(self, letter, symbole) :
        """
        Add a new symbole to the list
        """
        self.letters[symbole] = letter

    def remove_symbole(self, symbole) :
        """
        Remove a symbole from the list
        """
        del self.letters[symbole]