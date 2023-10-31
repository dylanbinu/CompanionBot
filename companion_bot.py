from collections import deque
import openai
from gtts import gTTS
import os
import time
import pyaudio
import wave
import api_secrets
import assemblyai as aai
import datetime
import requests
import string
import csv
import boto3
from PIL import Image
import cv2

def main():
    active_emotion = "happy"
    img = Image.open(active_emotion + ".jpg")
    img.show()
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    if ret:
        # Save the captured frame as an image file
        cv2.imwrite("captured_image.jpg", frame)
        print("Image captured and saved as captured_image.jpg")
        
    cap.release()

    cv2.destroyAllWindows()
    

    def evaluateEmotions():
        # Read access keys from a CSV file
        with open('Jakob_accesskeys.csv', 'r') as csvInput:
            next(csvInput)
            reader = csv.reader(csvInput)
            for line in reader:
                access_key_id = line[0]
                secret_access_key = line[1]

            # Ensure the indentation of the following lines is consistent with the block above
        photo = 'neil_smiling.jpg'

            # Create a Rekognition client using the access keys
        client = boto3.client('rekognition', region_name='us-east-2', aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key)

        # Open the image file for reading
        with open(photo, 'rb') as source_image:
            source_bytes = source_image.read()

        # Use the source_bytes to send the image to the detect_faces function
        response = client.detect_faces(Image={'Bytes': source_bytes}, Attributes=['ALL'])

# Check if faces are detected in the response
        if 'FaceDetails' in response:
            emotions = []

            # Iterate over detected faces
            for face_detail in response['FaceDetails']:
        # Extract emotions if available
                if 'Emotions' in face_detail:
                    for emotion in face_detail['Emotions']:
                        # Extract the type and confidence of the emotion
                        emotion_type = emotion['Type']
                        emotion_confidence = emotion['Confidence']
                        emotions.append((emotion_type, emotion_confidence))

            for emotion, confidence in emotions:
            #for emotion, confidence in emotions:
                print(emotion)
                textToSpeech("I can say with " + str(int(confidence)) + " percent confidence that you seem " + str(emotion).lower())
                break
        else:
            print("No faces detected in the image.")

    def evaluateEmotionsDefault():
        # Read access keys from a CSV file
        with open('Jakob_accesskeys.csv', 'r') as csvInput:
            next(csvInput)
            reader = csv.reader(csvInput)
            for line in reader:
                access_key_id = line[0]
                secret_access_key = line[1]

            # Ensure the indentation of the following lines is consistent with the block above
        photo = 'captured_image.jpg'

            # Create a Rekognition client using the access keys
        client = boto3.client('rekognition', region_name='us-east-2', aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key)

        # Open the image file for reading
        with open(photo, 'rb') as source_image:
            source_bytes = source_image.read()

        # Use the source_bytes to send the image to the detect_faces function
        response = client.detect_faces(Image={'Bytes': source_bytes}, Attributes=['ALL'])

# Check if faces are detected in the response
        if 'FaceDetails' in response:
            emotions = []

            # Iterate over detected faces
            for face_detail in response['FaceDetails']:
        # Extract emotions if available
                if 'Emotions' in face_detail:
                    for emotion in face_detail['Emotions']:
                        # Extract the type and confidence of the emotion
                        emotion_type = emotion['Type']
                        emotion_confidence = emotion['Confidence']
                        emotions.append((emotion_type, emotion_confidence))

            for emotion, confidence in emotions:
            #for emotion, confidence in emotions:
                os.system("osascript -e 'tell application \"Preview\" to quit'")  # Close the Preview app
                time.sleep(0.3)
                img = Image.open(str(emotion).lower() + ".jpg")
                img.show()
                print(emotion)
                active_emotion = str(emotion)
                break
        else:
            print("No faces detected in the image.")
        pauseObject = input("Press Enter")
          # Close the Preview app
        

    openai.api_key = api_secrets.API_KEY_OPENAI_CHATGPT
    aai.settings.api_key = api_secrets.API_KEY_ASSEMBLYAI

    # Function to turn text to speech
    # Input: Any string that will be translated to an audio file and played
    def textToSpeech(text):
        speech = gTTS(text=text, lang=language, slow=False, tld="ie")
        speech.save("textToSpeech.mp3")

        audio = "textToSpeech.mp3"
        os.system("afplay " + audio)

    def recordAudio(audioFileName, time):
        FRAMES_PER_BUFFER = 3200
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        p = pyaudio.PyAudio()

        stream = p.open(
            format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            frames_per_buffer = FRAMES_PER_BUFFER
        )

        print("Start speaking: ")

        seconds = time
        frames = []
        for i in range(0, int(RATE/FRAMES_PER_BUFFER*seconds)):
            data = stream.read(FRAMES_PER_BUFFER)
            frames.append(data)

        stream.stop_stream
        stream.close
        p.terminate

        print("Processing recording.")

        obj = wave.open(audioFileName, "wb")
        obj.setnchannels(CHANNELS)
        obj.setsampwidth(p.get_sample_size(FORMAT))
        obj.setframerate(RATE)
        obj.writeframes(b"".join(frames))
        obj.close()

    def transcribeAudioFile(audioFileName): 
        AUDIO_FILE_URL = audioFileName

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(AUDIO_FILE_URL)
        return transcript.text

    def speechToText(audioFileName, time):
        recordAudio(audioFileName, time)
        request = transcribeAudioFile(audioFileName)
        return request

    def processTimerInput(timerInput):
        word_dict = {"zero": 0, "0": 0, "one": 1, "1": 1, "two": 2, "2": 2, "three": 3, "3": 3, 
                    "four": 4, "4": 4, "five": 5, "5": 5, "six": 6, "6": 6, "seven": 7, "7": 7,
                    "eight": 8, "8": 8, "nine": 9, "9": 9,"ten": 10, "10": 10, "eleven": 11, 
                    "11": 11, "twelve": 12, "12": 12, "thirteen": 13, "13": 13,"fourteen": 14, 
                    "14": 14, "fifteen": 15, "15": 15,"sixteen": 16, "16": 16,"seventeen": 17, 
                    "17": 17, "eighteen": 18, "18": 18, "nineteen": 19, "19": 19,"twenty": 20, 
                    "20": 20, "thirty": 30, "30": 30, "forty": 40, "40": 40, "fifty": 50, "50": 50}
        result = 0
        valueExists = False
        timerInput = timerInput.translate(str.maketrans('','',string.punctuation)).lower()
        print(timerInput + "/")
        for word in timerInput.split():
            if word in word_dict:
                valueExists = True
                result += word_dict[word]
                print(str(result))

        if(valueExists): return result

        else: return int(timerInput)

    def set_timer():
        # Get hours, minutes, and seconds from user
        textToSpeech("How many hours would you like on your timer?")
        input_hours = speechToText("timer.wav" , 3)
        textToSpeech("How many minutes would you like on your timer?")
        input_minutes = speechToText("timer.wav", 3)
        textToSpeech("How many seconds would you like on your timer?")
        input_seconds = speechToText("timer.wav", 3)

        print("Input: " + input_hours + " hours, " + input_minutes + " minutes, and " + input_seconds + " seconds.")

        # Convert inputs to integers
        timer_hour = processTimerInput(input_hours)
        timer_minute = processTimerInput(input_minutes)
        timer_second = processTimerInput(input_seconds)

        print(str(timer_hour) + ":" + str(timer_minute) + ":" + str(timer_second))

        timer_hour = int(timer_hour)
        timer_minute = int(timer_minute)
        timer_second = int(timer_second)

        # Calculate total seconds for the timer
        total_seconds = timer_hour * 3600 + timer_minute * 60 + timer_second

        # Get the current time in seconds
        current_time = time.time()

        # Calculate the alert time in seconds
        alert_time = current_time + total_seconds

        # While the user doesn't say cancel or the timer expires, run this loop.
        while True:
            # Get the current time and compare alert time to current time.
            current_time = time.time()
            if current_time >= alert_time:
                print("Time's up!")
                textToSpeech("Time's up!")
                os.system('afplay timerAlert.wav')
                # Break out of this loop after playing the "time's up" alert.
                break

            print(f"Target time: {time.ctime(alert_time)}")
            print(f"Current time: {time.ctime(current_time)}")
            print("If you would like to cancel the timer, say 'cancel'")
            textToSpeech("The clock is ticking. If you would like to cancel the timer, say 'cancel'")

            timerInput = speechToText("timer.wav", 4)
            if "cancel." in timerInput.lower() or "cancel" in timerInput.lower():
                textToSpeech("The timer has been cancelled.")
                break
            # Sleep for 1 second before running this loop again.
            time.sleep(1)

    # Function to convert kelvin temperature to fahrenheit and celsius
    def kelvin_to_celsius_fahrenheit(kelvin):
        celsius = kelvin - 273.15
        fahrenheit = celsius * (9/5) + 32
        return celsius, fahrenheit

    # Retrieve weather data including temperature, 
    def getWeather(city):
        print(city)
        city = city.translate(str.maketrans('','',string.punctuation))
        print(city)
        CITY = city
        openWeatherUrl = api_secrets.API_OPEN_WEATHER_BASE_URL + "appid=" + api_secrets.API_KEY_OPEN_WEATHER + "&q=" + CITY

        response = requests.get(openWeatherUrl).json()
        temp_kelvin = response['main']['temp']
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
        wind_speed = response['wind']['speed']

        humidity = response['main']['humidity']
        description = response['weather'][0]['description']
        sunrise_time = datetime.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
        sunset_time = datetime.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

        weather = f"The temperature in {CITY} is currently {temp_fahrenheit:.2f} degrees Fahrenheit. It feels like {feels_like_fahrenheit:.2f} degrees Fahrenheit. The humidity in {CITY} is at {humidity}% and the wind speed is blowing at {wind_speed}m/s. The general weather in {CITY} is {description}. "
        return weather

    def getTemperature(city):
        print(city)
        city = city.translate(str.maketrans('','',string.punctuation))
        print(city)
        CITY = city
        openWeatherUrl = api_secrets.API_OPEN_WEATHER_BASE_URL + "appid=" + api_secrets.API_KEY_OPEN_WEATHER + "&q=" + CITY

        response = requests.get(openWeatherUrl).json()
        temp_kelvin = response['main']['temp']
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
        
        weather = f"The temperature in {CITY} is currently {temp_fahrenheit:.2f} degrees Fahrenheit. It feels like {feels_like_fahrenheit:.2f} degrees Fahrenheit."
        return weather


    limit = "30"                # Word limit for ChatGPT response
    name = "Dylan"              # Name that you would like ChatGPT to address you as
    language = "en"             # Language of ChatGPT response
    communicate = False         # Communicate toggle

    current_time = datetime.datetime.now()

    current_time_str = current_time.strftime("It is currently %I:%M %p on %A, %B %d, %Y")

    # Initial Prompt: Ask user if they would like to talk
    textToSpeech("Hello " + name + "! Would you like to talk to me? ")


    request = speechToText("initialPrompt.wav", 2)

    # Input prompt to take user input in response to Initial Prompt

    if "yes" in request.lower():     # If "yes" is contained in the response
        communicate = True          # Set communicate toggle to True

    if communicate == True:
        textToSpeech("Cool! Welcome to my main menu. Choose something from one of my many functions!")

    while communicate == True:

        request = speechToText("choicePrompt.wav", 3)

        if "wait" in request.lower():
            textToSpeech("No worries, I'll wait for you. If you'd like me to start listening again, say the words 'wake up'.")
            while ("wake" not in request.lower() and "up" not in request.lower()):
                os.system('afplay idling.wav')
                request = speechToText("waitPhrase.wav", 5)
                print("Take your time. I'll wait for you.")
            
            textToSpeech("That was a nice little nap! What else would you like to do from my main menu?")

        if "thank you" in request.lower() or "no." == request.lower():
                communicate = False
                print(communicate)
                break
        
        if "chat" in request.lower() or "talk" in request.lower():
            textToSpeech("Sure thing! What's up?")
            
            while True:
                chatgptRequest = speechToText("chatgptPrompt.wav", 5)

                if "wait" in chatgptRequest.lower():
                    textToSpeech("I gotcha! Take your time. I'll wait for ya. If you'd like me to start listening again, say 'continue'")
                    while "wake" not in chatgptRequest.lower() and "up" not in chatgptRequest.lower():
                        os.system('afplay idling.wav')
                        chatgptRequest = speechToText("waitPhrase.wav", 2)
                        print("Take your time. I will wait for you.")

                    textToSpeech("That was a nice little nap! What else would you like to do from my main menu?")

                if "thank you" in chatgptRequest.lower() or "thanks" in chatgptRequest.lower() or "no." == chatgptRequest.lower():
                    print(communicate)
                    break

                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": chatgptRequest + ". Keep response under " + limit + " words."}])
                print(completion.choices[0].message.content)

                textToSpeech(completion.choices[0].message.content)
                textToSpeech("I'm listening.")
                
            textToSpeech("Sure thing! What else would you like to do from my main menu?")

        if "time " in request.lower() or "time." in request.lower():
            textToSpeech(current_time_str)
            textToSpeech("What else would you like to do from my main menu?")

        if "timer" in request.lower():
            set_timer()
            textToSpeech("What else would you like to do from my main menu?")
        
        if"weather" in request.lower():
            textToSpeech("Which city would you like to check the weather for?")

            city = speechToText("getWeather.wav", 3)
            weather = getWeather(city)
            
            textToSpeech(weather)
            textToSpeech("What else would you like to do from my main menu?")

        if"temperature" in request.lower():
            textToSpeech("Which city would you like to check the temperature for?")

            city = speechToText("getWeather.wav", 3)
            temperature = getTemperature(city)

            textToSpeech(temperature)
            textToSpeech("What else would you like to do from my main menu?")

        if "emotions" in request.lower() or "emotion" in request.lower():
            evaluateEmotions()
            textToSpeech("What else would you like to do from my main menu?")

    if "thank you" in request.lower() or "thanks" in request.lower():
        textToSpeech("No problem " + name + ". Have a great day and remember that I am here for you if you ever need me!")

    else:
        textToSpeech("Gotcha " + name + ". Have a great day and remember that I am here for you if you ever need me!")
main()