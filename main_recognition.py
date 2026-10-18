import speech_recognition
import pyttsx3
from datetime import date
from datetime import datetime
import sqlite3

def chatting(name, id, check):
    name = 'hello' + name
    listener = speech_recognition.Recognizer()
    speaker = pyttsx3.init()
    speaker.say(name)
    speaker.runAndWait()
    check = 0
    while True:
        listener = speech_recognition.Recognizer()
        speaker = pyttsx3.init()
        CPU = ''
        with speech_recognition.Microphone() as mic:
            print('CPU : I am listening')
            audio = listener.listen(mic)
        try:
            you = listener.recognize_google(audio)
        except:
            you = ''
        print(you)
        if 'hello' in you or 'hi' in you or 'What room do I study' in you:
            if(check):
                CPU = "Today you have class at " + str(check) + " hours"
            else:
                CPU = 'Today you do not have any class'
        elif 'today' in you:
            today = date.today()	
            CPU = today.strftime("%B %d, %Y")
        elif 'what time is it' in you:
            now = datetime.now()
            CPU = now.strftime("%H hours %M minutes %S seconds")
        elif 'bye' in you:
            CPU = 'Bye'
            break
        elif 'goodbye' in you:
            CPU = 'Bye'
            break
        elif 'out' in you:
            CPU = 'Bye'
            break

        else:
            CPU = 'I cannot hear and understand you'
            check += 1
            if check > 3:
                break
            if you != '':
                conn = sqlite3.connect("data_student.db")
                query = "INSERT INTO ai (question) VALUES(" + str(you) + ")" + " WHERE id=" + str(id)
                print(query)
                conn.commit()
                conn.close()
        speaker.say(CPU)
        speaker.runAndWait()
