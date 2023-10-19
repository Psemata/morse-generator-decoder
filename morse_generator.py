import numpy as np
import sounddevice as sd
import soundfile as sf
import scipy as sc
import scipy.signal as scs
import wave
import struct

class Morse_Generator :
    # échantillonage : ~22050
    # Un point tous les (fréquence d'échantillonage) : 1/22050
    # fréquence du signal : 440
    # Bip court : 200 ms
    # Bip long : 600 ms
    # Silence entre chaque symbole : 200 ms
    # Silence entre lettre : 600 ms
    # Silence entre mot : 1000 ms

    def __init__(self, sample_frequency) :
        self.letters = {
            "A" : "._",
            "B" : "_...",
            "C" : "_._.",
            "D" : "_..",
            "E" : ".",
            "F" : ".._.",
            "G" : "__.",
            "H" : "....",
            "I" : "..",
            "J" : ".___",
            "K" : "_._",
            "L" : "._..",
            "M" : "__",
            "N" : "_.",
            "O" : "___",
            "P" : ".__.",
            "Q" : "__._",
            "R" : "._.",
            "S" : "...",
            "T" : "_",
            "U" : ".._",
            "V" : "..._",
            "W" : ".__",
            "X" : "_.._",
            "Y" : "_.__",
            "Z" : "__.."
        }
        self.sound = []
        self.morse_phrase = ""
        self.sample_frequency = sample_frequency

    def generate_file(self, sentence) :
        """
        Function used to generate a sound file which will contains morse code
        """
        self.conversion(sentence)
        self.sentence_to_wav("morse.wav")

    def conversion(self, sentence) :
        """
        Convert a sentence to morse code
        """
        for letter in sentence :
            if letter == " " :
                # Space wait
                self.add_silence(1000)
            else :
                for symbole in self.letters[letter.upper()] :
                    if symbole == "." :
                        # Short bip sound
                        self.add_sound(200)
                    elif symbole == "_" :
                        # Long bip sound
                        self.add_sound(600)
                    # Silence between symboles
                    self.add_silence(200)
                    self.morse_phrase += symbole
                # Silence between letters
                self.add_silence(600)
                self.morse_phrase += " "

    def print_phrase(self) :
        print(self.morse_phrase)

    def add_sound(self, duration_ms=300, frequency=440.0, amplitude=1.0) :
        """
        Add a sound to the morse code
        """
        n_points = duration_ms * (self.sample_frequency /  1000.0)

        for x in range(int(n_points)) :
            self.sound.append(amplitude * np.sin(2*np.pi*frequency*(x / self.sample_frequency)))

    def add_silence(self, duration_ms=300) :
        """
        Add a silence to the morse code
        """
        n_points = duration_ms * (self.sample_frequency / 1000.0)

        for x in range(int(n_points)) :
            self.sound.append(0.0)

    def sentence_to_wav(self, file_name) :
        """
        Function which generate a wav file from the generated morse code
        """
        wav_file = wave.open(file_name, "w")
        nchannels = 1
        sampwidth = 2

        nframes = len(self.sound)
        comptype = "NONE"
        compname = "not compressed"
        wav_file.setparams((nchannels, sampwidth, self.sample_frequency, nframes, comptype, compname))

        for sample in self.sound :
            wav_file.writeframes(struct.pack('h', int(sample * 32767.0)))

        wav_file.close()

    def add_letter(self, letter, symbole_tab) :
        """
        Add a letter to the list
        """
        self.letters[letter] = symbole_tab

    def remove_letter(self, letter) :
        """
        Remove a letter from the list
        """
        del self.letters[letter]