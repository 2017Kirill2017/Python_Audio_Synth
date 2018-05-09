# -*- coding: utf-8 -*-
"""
Created on Wed May  9 2018

@author: Glu(k)hov Kirill
"""
import os
from random import randint
from pygame import mixer
import time
from gtts import gTTS
from langdetect import detect_langs
from langdetect import DetectorFactory
DetectorFactory.seed = 0


class Voice_Synth:
    def __init__(self, rem=False):
        self.tts = None
        self.last_path = None
        self.remove_old = rem
        mixer.init()
        
    def to_mp3(self, txt, language=None):
        if not language:
            language = max(detect_langs(txt), key=lambda x: x.prob).lang
        self.tts = gTTS(text=txt, lang=language)
    
    def save_mp3(self, path):
        if self.tts:
            self.tts.save(path)
            if self.remove_old:
                if self.last_path:
                    mixer.music.load(path)
                    mixer.stop
                    mixer.quit
                    if(os.path.exists(self.last_path)):
                        os.remove(self.last_path)
            self.last_path = path
    
    def play_mp3(self, path=None):
        if not path: path = self.last_path
        mixer.music.load(path)
        mixer.music.play()
        while mixer.music.get_busy(): time.sleep(0.1)
    
    def kill(self):
        self.to_mp3("Надеюсь, что вам понравилась сия программа", language="ru")
        name = "Bye"+str(randint(0,999999))+".sn.mp3"
        self.save_mp3(name)
                
    pass


def main():
    print("Хотите просмотреть возможности программы?")
    answer = input("[y/n]:")
    if "y" in answer.lower():
        synth = Voice_Synth(True)
        synth.to_mp3('Привет, человек! Как у тебя дела?')
        synth.save_mp3("1.mp3")
        synth.play_mp3()
        synth.to_mp3('Пока, человек! До скорой встречи!')
        synth.save_mp3("2.mp3")
        synth.play_mp3()
        synth.kill()
        synth.play_mp3()
    else:
        synth = Voice_Synth()
        while True:
            print("Если хотите выйти из программы - введите 'q'. Иначе - пустую строку")
            if input(">>").lower() == "q": 
                synth.kill()
                synth.play_mp3()
                break
            
            print("Введите текст:")
            txt = input(">>")
            print("Какой это язык ('ru'-русский, 'en'- ангийский, '*'- я не знаю)?")
            language = input(">>")
            if "*" in language: language = None
            synth.to_mp3(txt, language)
            print("Введите путь, по которому я сохраню mp3")
            path = input(">>")
            while True:
                try:
                    synth.save_mp3(path)
                    break
                except BaseException as e:
                    print("Что-то пошло не так:", e)
                    print("Введите другой путь, по которому я сохраню mp3")
                    path = input(">>")
            print("Проиграть Вам mp3 файл?")
            answer = input("[y/n]:")
            if "y" in answer.lower():
                synth.play_mp3()
    pass


if __name__ == "__main__":
    main()