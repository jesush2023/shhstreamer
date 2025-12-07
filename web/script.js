window.onload = async function() {
    console.log("Loading System...");

    let data = await eel.get_lists()();

    if (data) {

        fillSelect("micSelect", data.mics);
        fillSelect("voiceSelect", data.voices);

        let langSelect = document.getElementById("langSelect");
        langSelect.innerHTML = "";

        data.languages.forEach(langItem => {
            let option = document.createElement("option");

            option.text = langItem.name;
            option.value = langItem.code;

            langSelect.appendChild(option);
        });

        if (data.config) {

            document.getElementById("micSelect").value = data.config.mic;
            document.getElementById("voiceSelect").value = data.config.voice;
            document.getElementById("langSelect").value = data.config.lang;
            document.getElementById("hotkeyInput").value = data.config.hotkey || "f9"
            
            let volReal = data.config.volume;

            let threshReal = data.config.sensitivity || 20;

            let sSlider = document.getElementById("sensInput");
            let sLabel = document.getElementById("sensLabel");

            let slider = document.getElementById('volInput');
            let label = document.getElementById('volLabel');

            if (sSlider) sSlider.value = threshReal;
            if (sLabel) sLabel.innerText = threshReal + "%";

            if (slider) slider.value = volReal;
            if (label) label.innerText = volReal + "%";
        }

        js_log("--- System Loaded (Devices & Config) ---")
    }
};

function fillSelect(elementId, listaItems) {
    let select = document.getElementById(elementId);
    select.innerHTML = ""; 
    
    listaItems.forEach(item => {
        let option = document.createElement("option");
        option.value = item.id;
        option.text = item.name; 
        select.appendChild(option);
    });
}

function setConfig(key, value) {
    eel.update_config(key, value);
}

function start() {
    document.getElementById('btnStart').disabled = true;
    document.getElementById('btnStart').innerText = "WORKING...";

    document.getElementById('btnStop').disabled = false;
    document.getElementById('btnStop').innerText = "STOP STREAM";
    eel.start_stream();
}

function stop() {
    document.getElementById('btnStop').disabled = true;
    document.getElementById('btnStop').innerText = "STOP STREAM";

    eel.stop_stream();

    document.getElementById('btnStart').disabled = false;
    document.getElementById('btnStart').innerText = "STRAT STREAMING";

    js_log("Stopping... (Waiting for actual phase...)");
}

function updateVolume(val) {
    document.getElementById('volLabel').innerText = val + "%";
    eel.update_config('volume', val); 
}

function updateSens(val) {
    document.getElementById('sensLabel').innerText = val + "%";
    eel.update_config('sensitivity', val); 
}

async function setHotkey(){
    let val = document.getElementById("hotkeyInput").value;
    let success = await eel.update_hotkey(val)();

    if (success) {
        js_log("[SUCCESS] Hotkey changed to: "+ val);
    } else {
        js_log(" [ERROR] Invalid key.");
    }
}

eel.expose(js_trigger_start);
function js_trigger_start(){
    document.getElementById('btnStart').disabled = true;
    document.getElementById('btnStart').innerText = "WORKING...";
    document.getElementById('btnStop').disabled = false;
    document.getElementById('btnStop').innerText = "STOP STREAM";
    js_log(">>> START HOTKEY USED");
}

eel.expose(js_trigger_stop);
function js_trigger_stop(){
    stop();
    js_log(">>> STOP HOTKEY USED");
}

eel.expose(js_log);
function js_log(text) {
    let box = document.getElementById('console');
    let p = document.createElement('p');
    p.innerText = text;
    
    if(text.includes("You:")) p.style.color = "#00ffff";
    if(text.includes("Bot:")) p.style.color = "#00ff88";
    if(text.includes("Error")) p.style.color = "red";
    
    box.appendChild(p);
    box.scrollTop = box.scrollHeight;
}
