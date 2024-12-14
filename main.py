import speech_recognition as sr
import sounddevice as sd
import google.generativeai as gai
import gtts
import soundfile as sf
from playsound import playsound

gai.configure(api_key="YOU_API_KEY")

# Function to get response
def chat(input):
  model = gai.GenerativeModel('gemini-1.5-flash')
  output  = model.generate_content(input)
  return output.text

# Function to convert speech to text
def speechToText():
    text = ""
    r = sr.Recognizer()
    # Use sounddevice to record audio
    duration = 5  # Duration of recording in seconds
    fs = 44100  # Sample rate
    print("Speak now...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    
    sf.write("temp_audio.wav", audio_data, fs)

    # Use speech recognition on the audio file
    with sr.AudioFile("temp_audio.wav") as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not recognize your voice.")
        return None

# function to convert text to audio
def textToSpeech(text):
  tts = gtts.gTTS(text)
  tts.save("output.mp3")
  playsound("output.mp3")

# Main function
def main():
  text = ""
  while(text != "exit"): # Exit the loop if the user says "exit"
    text = speechToText()
    print(text)
    try:
        response = chat(text)
        print(response)
        textToSpeech(response)
    except:
        print("Sorry, I could not understand you.")

if __name__ == "__main__":
    main()
