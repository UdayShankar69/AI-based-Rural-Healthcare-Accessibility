import speech_recognition as sr
import pyttsx3
# Initialize recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")
        # Reduce noise
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        return "Sorry, could not understand audio"
    except sr.RequestError:
        return "Speech service unavailable"
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()
if __name__ == "__main__":
    user_text = speech_to_text()
    text_to_speech(f"You said {user_text}")