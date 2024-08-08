
import tkinter as tk
from gtts import gTTS
import pygame
import os
import threading
import speech_recognition as sr

class VoiceAssistantApp:
    def _init_(self, master):
        self.master = master
        master.title("Voice Assistant")

        self.label_listen = tk.Label(master, text="Listening...")
        self.label_listen.pack()

        self.label_speak = tk.Label(master, text="Assistant speaking...")
        self.label_speak.pack()

        self.label_result = tk.Label(master, text="Speak and see the text below:")
        self.label_result.pack()

        self.text_var = tk.StringVar()
        self.text_entry = tk.Entry(master, textvariable=self.text_var)
        self.text_entry.pack()

        self.listen_and_speak()  # Start listening automatically

    def listen_and_speak(self):
        threading.Thread(target=self.listen_and_update).start()

    def listen_and_update(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)

            while True:  # Continuous listening
                self.update_status("Listening...")
                try:
                    audio = recognizer.listen(source, timeout=5)
                    self.update_status("Recognizing...")
                    text = recognizer.recognize_google(audio)
                    self.update_text("You said: " + text)

                    response = self.generate_response(text)
                    self.speak(response)
                except sr.UnknownValueError:
                    self.update_text("Sorry, I couldn't understand.")
                except sr.RequestError as e:
                    self.update_text(f"Could not request results; {e}")

    def generate_response(self, command):
        # Customize responses based on keywords
        if "how are you" in command.lower():
            return "I'm doing well, thank you!"
        elif "tell me a joke" in command.lower():
            return "Why don't scientists trust atoms? Because they make up everything!"
        else:
            return "I understand."

    def speak(self, text):
        self.update_status("Assistant speaking...")
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")

        def play_audio():
            pygame.mixer.init()
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()
            os.remove("output.mp3")
            self.update_status("")
            self.update_text("Assistant said: " + text)

        audio_thread = threading.Thread(target=play_audio)
        audio_thread.start()

    def update_text(self, text):
        current_text = self.text_var.get()
        if current_text:
            current_text += "\n" + text
        else:
            current_text = text
        self.text_var.set(current_text)

    def update_status(self, status):
        self.label_listen.config(text=status)
        self.label_speak.config(text=status)

        

    if __name__ == "__main__":
        root = tk.Tk()
        app = VoiceAssistantApp(root)
        root.mainloop()