#VTT (Voice to Text) Module Develop
import speech_recognition as sr
import os
import time
import pyaudio

def cleaning():
    os.system('cls' if os.name == 'nt' else 'clear')

def welcome():
    art = r"""
                                                                                                                                                                
    ,---,        ,'  , `.                       ___                  ,---,                         
    ,`--.' |     ,-+-,.' _ |  ,--,               ,--.'|_              .'  .' `\                       
    |   :  :  ,-+-. ;   , ||,--.'|               |  | :,'     ,---,.,---.'     \                      
    :   |  ' ,--.'|'   |  ;||  |,      .--.--.   :  : ' :   ,'  .' ||   |  .`\  |               .---. 
    |   :  ||   |  ,', |  ':`--'_     /  /    '.;__,'  /  ,---.'   ,:   : |  '  |   ,---.     /.  ./| 
    '   '  ;|   | /  | |  ||,' ,'|   |  :  /`./|  |   |   |   |    ||   ' '  ;  :  /     \  .-' . ' | 
    |   |  |'   | :  | :  |,'  | |   |  :  ;_  :__,'| :   :   :  .' '   | ;  .  | /    /  |/___/ \: | 
    '   :  ;;   . |  ; |--' |  | :    \  \    `. '  : |__ :   |.'   |   | :  |  '.    ' / |.   \  ' . 
    |   |  '|   : |  | ,    '  : |__   `----.   \|  | '.'|`---'     '   : | /  ; '   ;   /| \   \   ' 
    '   :  ||   : '  |/     |  | '.'| /  /`--'  /;  :    ;          |   | '` ,/  '   |  / |  \   \    
    ;   |.' ;   | |`-'      ;  :    ;'--'.     / |  ,   /           ;   :  .'    |   :    |   \   \ | 
    '---'   |   ;/          |  ,   /   `--'---'   ---`-'            |   ,.'       \   \  /     '---"  
            '---'            ---`-'                                 '---'          `----'             
    "Shy Solutions from a shy dev."                                                                                                
    """ 
    print(art)


def menu(option_list, current_config):
    while True:
        cleaning()
        welcome()
        
        print("\n----- [MAIN CONFIG.] -----")
        print(f"Microphone ID: {current_config.get('mic', 'Default')}")
        print(f"Language: {current_config.get('lang', 'Undefined')}")
        
        print("\n----- [MAIN MENU] -----")
        print("-"*22)
        
        for i, option in enumerate(option_list, 1):
            print(f"[{i}] {option}")

        print(f"[{len(option_list) + 1}] Exit")
        print("-"*22)
        
        raw_selection = input("\n>>> Choose an option: ")
        
        try:
            
            selection = int(raw_selection)

            if 1 <= selection <= len(option_list):
                return selection - 1
            elif selection == len(option_list) + 1:
                return None
            else:
                input("Invalid Option. Press Enter...")
                
        except ValueError:
            input("Please select your option. Press Enter...")

AVAILABLE_LANGUAGES = {
    "1": {"name": "Español (España)", "code": "es-ES"},
    "2": {"name": "Español (LatAm)", "code": "es-419"},
    "3": {"name": "English (US)", "code": "en-US"},
    "4": {"name": "Japanese", "code": "ja-JP"}
}

def select_language():
    cleaning()
    print("\n--- Languages Supported ---")
    print("\nMore available languages incoming")
    for key, info in AVAILABLE_LANGUAGES.items():
        print(f"[{key}] {info['name']}")

    while True:
        option = input("Select your language (number): ").strip()
        
        if option in AVAILABLE_LANGUAGES:
            selection = AVAILABLE_LANGUAGES[option]
            print(f"-> Selected: {selection['name']}")
            time.sleep(1)
            return selection['code']
        else:
            print("Invalid Option. Try Again.")

def select_mic():
    cleaning()
    p = pyaudio.PyAudio()
    info_devices = []
    
    seen_core_names = set()
    
    print("\n----- [ Scanning Audio Devices ] -----")
    
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        name = dev.get('name')
        input_channels = dev.get('maxInputChannels')
        
        ignore_words = ["Microphone", "Micrófono", "Input", "Entrada"]
        
        clean_name = name
        for word in ignore_words:
            clean_name = clean_name.replace(word, "").strip()
        
        if (input_channels > 0 and
            clean_name not in seen_core_names and
            "Asignador" not in name and
            "Controlador primario" not in name):
            
            seen_core_names.add(clean_name)
            info_devices.append((i, name))
            
    p.terminate()
    
    print("\n--- [ Select Your Microphone ] ---")
    for index_list, (real_id, name) in enumerate(info_devices):
        print(f"[{index_list}] {name}")
        
    while True:
        try:
            option = int(input("\nSelect your microphone: "))
            if 0 <= option < len(info_devices):
                real_id = info_devices[option][0]
                real_name = info_devices[option][1]
                print(f"Selected: {real_name} (ID: {real_id})")
                return real_id
                
            print("Invalid Selection, Try again.")
        except ValueError:
            print("Please, enter a number.")

def hear_function(mic_id, lang_code):

    r = sr.Recognizer()
    
    print(f"\nInitializing microphone ID {mic_id}...")
    try:
        
        device = mic_id if mic_id is not None else None
        
        with sr.Microphone(device_index=mic_id) as source:
            print("Calibrating background noise (silence please)...")
            r.adjust_for_ambient_noise(source, duration=2)
            print("Calibration Ready, Speak Now...")
            
            audio = r.listen(source, timeout=10, phrase_time_limit=None)
            
            print("Processing audio...")
            text = r.recognize_google(audio, language=lang_code)
            print(f"\nYour Result: {text}")
            input("\nPress Enter to Return to Menu")
            return text
        
    except sr.WaitTimeoutError:
        print("Time out. No Speech Detected.")
        input("Press enter...")    
    except sr.UnknownValueError:
        print("Can't understand audio, try again.")
    except sr.RequestError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    current_mic = 0
    current_lang = "es-419"
    
    options = [
        "Select Microphone",
        "Select Language",
        "Test Recognition (One Shot)"
    ]
    
    while True:
        
        config_status = {"mic": current_mic, "lang": current_lang}
        
        choice = menu(options, config_status)
        
        if choice is None:
            print("Goodbye!")
            break
        elif choice == 0:
            current_mic = select_mic()
            
        elif choice == 1:
            current_lang = select_language()
            
        elif choice == 2:
            hear_function(current_mic, current_lang)