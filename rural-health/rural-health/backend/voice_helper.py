from speech_service import speech_to_text, text_to_speech
def process_voice():
    user_input = speech_to_text()
    print("User Input:", user_input)
    response = f"You said: {user_input}"
    text_to_speech(response)
if __name__ == "__main__":
    process_voice()