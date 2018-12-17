import speech_recognition as sr
import threading

class AudioStreamThread(threading.Thread):
    def __init__(self , threadId , name , mainObject):
        
        threading.Thread.__init__(self)
        self.id = threadId
        self.name = name
        self.MO = mainObject

    def run(self):
        
        with sr.Microphone() as source:
            print("\nPlease wait till calibrating noise cancelation : ")
            self.MO.recognizer.adjust_for_ambient_noise(source , duration=5)
            
        with sr.Microphone() as source:
            print("Listening to you : ")
            self.MO.audio = self.MO.recognizer.listen(source)
            
class RecognizeThread(threading.Thread):
    def __init__(self , threadId , name , mainObject):
        
        threading.Thread.__init__(self)
        self.id = threadId
        self.name = name
        self.MO = mainObject

    def run(self):
        ast = AudioStreamThread(10 , "audio_stream_thread" , self.MO)
        ast.start()
        ast.join()
        
        whatYouSaid = ""
        engine = self.MO.pe
        if engine == "google":
            whatYouSaid = self.MO.recognizer.recognize_google(self.MO.audio)
        elif engine == "sphinx":
            whatYouSaid = self.MO.recognizer.recognize_sphinx(self.MO.audio)
        print("You said : " + whatYouSaid)
            
class VoiceRecognition():
    def __init__(self , processEngine):
        
        self.recognizer = sr.Recognizer()
        self.audio = 0
        self.pe = processEngine
        
    def recognizeVoice(self):
        
        RecognizeThread(11 , "recognize_thread" , self).start()

