import pyttsx3
#import utils

def select_voice():
    #utils.cleaning()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    voice_options = []
    
    for i, v in enumerate(voices):
        voice_options.append({
            "id": i,
            "name": v.name
        })
        
    return voice_options
    
    #Legacy. CMD UI
    
    """
    print("\n----- [ Available Voices ] -----")
    for i, v in enumerate(voices):
        print(f"[{i}], {v.name}")
        
    try:
        op = int(input("\n>>>Choose voice ID: "))
        if 0 <= op < len(voices):
            engine.setProperty('voice', voices[op].id)
            engine.say("Voice Selected")
            engine.runAndWait()
            return op
    except:
        pass
    return 0
    """

def speak(text, voice_index=0):
    if not text: return
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
        
    engine.setProperty('rate', 150)
    
    print(f"\n[BOT]: {text}")
    engine.say(text)
    engine.runAndWait()