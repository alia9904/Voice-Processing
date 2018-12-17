import sys
sys.path.append("./")
from SpectrumGraph import *
from VoiceRecognition import *

if __name__ == "__main__":
    whichEngine = int(input("Select voice processing engine : \n 1 : google (online : more precise : requires internet connection) \n 2 : Built-in (offline) \n"))
    if whichEngine == 1:
        whichEngine = "google"
    elif whichEngine == 2 :
        whichEngine = "sphinx"
    else :
        whichEngine = "sphinx"
    VoiceRecognition(whichEngine).recognizeVoice()
    time.sleep(5) #noise cancelation waiting time
    SpectrumGraph(9 , 4 ,False).start_plot()
    
