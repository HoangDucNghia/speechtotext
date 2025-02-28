import pyaudio
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from threading import Thread
from vosk import Model, KaldiRecognizer
import wave
import json
import datetime
import document

# Parameters for recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Vosk works best with 16000 Hz sample rate
CHUNK = 1024

# Global variables
is_recording = False
frames = []
full_transcription = ""  # Store all final transcribed text
interim_transcription = ""  # Store interim results temporarily

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Initialize Vosk Model
model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, RATE)

# Function to handle streaming transcription using Vosk
def stream_transcribe():
    global is_recording, full_transcription, interim_transcription
    is_recording = True

    # Open a streaming connection to PyAudio for microphone input
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    
    while is_recording:
        data = stream.read(CHUNK)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            transcript = result_dict.get("text", "")
            
            # Update interim or final transcription
            if result_dict.get("partial"):
                interim_transcription = result_dict["partial"]
            if result_dict.get("text"):
                full_transcription += " " + result_dict["text"]

            # Update the transcription text area in the GUI
            transcription_text.delete(1.0, tk.END)
            transcription_text.insert(tk.END, full_transcription + interim_transcription)

    stream.stop_stream()
    stream.close()
    print("Streaming stopped.")

# Function to transcribe an uploaded audio file using Vosk
def transcribe_audio_file(file_path):
    global full_transcription
    try:
        with wave.open(file_path, "rb") as audio_file:
            recognizer = KaldiRecognizer(model, audio_file.getframerate())
            full_transcription = ""
            while True:
                data = audio_file.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    result_dict = json.loads(result)
                    full_transcription += " " + result_dict.get("text", "")
                
            # Final transcription
            transcription_text.delete(1.0, tk.END)
            transcription_text.insert(tk.END, full_transcription)
            
            # Update additional features
            update_additional_features()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to transcribe audio file: {e}")

# Function to handle file upload
def upload_audio_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.wav *.mp3"), ("All Files", "*.*")]
    )
    if file_path:
        Thread(target=transcribe_audio_file, args=(file_path,)).start()

# Function to start recording and streaming
def start_recording():
    global full_transcription, interim_transcription
    full_transcription = ""  # Reset transcription when starting a new recording
    interim_transcription = ""  # Reset interim transcription
    Thread(target=stream_transcribe).start()

# Function to stop recording
def stop_recording():
    global is_recording
    is_recording = False
def translate_text():
    pass
def summarize_text():
    pass
def extract_keywords():
    pass
def detect_action_items():
    pass
def analyze_sentiment():
    pass
def export_transcription():
    pass
# Function to update additional features (translation, summarization, etc.)
def update_additional_features():
    # Translate the transcription
    translated_text = translate_text(full_transcription, "en")
    translation_text.delete(1.0, tk.END)
    translation_text.insert(tk.END, translated_text)

    # Summarize the transcription
    summary = summarize_text(full_transcription)
    summary_text.delete(1.0, tk.END)
    summary_text.insert(tk.END, summary)

    # Extract keywords
    keywords = extract_keywords(full_transcription)
    keywords_text.delete(1.0, tk.END)
    keywords_text.insert(tk.END, ", ".join(keywords))

    # Detect action items
    action_items = detect_action_items(full_transcription)
    action_items_text.delete(1.0, tk.END)
    action_items_text.insert(tk.END, "\n".join(action_items))

    # Analyze sentiment
    sentiment_score, sentiment_magnitude = analyze_sentiment(full_transcription)
    sentiment_label.config(text=f"Sentiment: Score={sentiment_score}, Magnitude={sentiment_magnitude}")

# Tkinter GUI
root = tk.Tk()
root.title("English Transcriber")
root.geometry("1000x800")

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Tab 1: Transcription
transcription_tab = ttk.Frame(notebook)
notebook.add(transcription_tab, text="Transcription")

# Transcription text area
transcription_label = ttk.Label(transcription_tab, text="Transcription:")
transcription_label.pack(pady=5)
transcription_text = scrolledtext.ScrolledText(transcription_tab, wrap=tk.WORD, width=100, height=20)
transcription_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Tab 2: Translation
translation_tab = ttk.Frame(notebook)
notebook.add(translation_tab, text="Translation")

# Translation text area
translation_label = ttk.Label(translation_tab, text="Translation:")
translation_label.pack(pady=5)
translation_text = scrolledtext.ScrolledText(translation_tab, wrap=tk.WORD, width=100, height=20)
translation_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Tab 3: Summary
summary_tab = ttk.Frame(notebook)
notebook.add(summary_tab, text="Summary")

# Summary text area
summary_label = ttk.Label(summary_tab, text="Summary:")
summary_label.pack(pady=5)
summary_text = scrolledtext.ScrolledText(summary_tab, wrap=tk.WORD, width=100, height=10)
summary_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Tab 4: Keywords
keywords_tab = ttk.Frame(notebook)
notebook.add(keywords_tab, text="Keywords")

# Keywords text area
keywords_label = ttk.Label(keywords_tab, text="Keywords:")
keywords_label.pack(pady=5)
keywords_text = scrolledtext.ScrolledText(keywords_tab, wrap=tk.WORD, width=100, height=10)
keywords_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Tab 5: Action Items
action_items_tab = ttk.Frame(notebook)
notebook.add(action_items_tab, text="Action Items")

# Action items text area
action_items_label = ttk.Label(action_items_tab, text="Action Items:")
action_items_label.pack(pady=5)
action_items_text = scrolledtext.ScrolledText(action_items_tab, wrap=tk.WORD, width=100, height=10)
action_items_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Tab 6: Sentiment Analysis
sentiment_tab = ttk.Frame(notebook)
notebook.add(sentiment_tab, text="Sentiment Analysis")

# Sentiment label
sentiment_label = ttk.Label(sentiment_tab, text="Sentiment:")
sentiment_label.pack(pady=10)

# Buttons frame
buttons_frame = ttk.Frame(root)
buttons_frame.pack(pady=10)

# Start recording button
record_button = ttk.Button(buttons_frame, text="Start Recording", command=start_recording)
record_button.grid(row=0, column=0, padx=5)

stop_button = ttk.Button(buttons_frame, text="Stop Recording", command=stop_recording)
stop_button.grid(row=0, column=1, padx=5)

# Upload audio file button
upload_button = ttk.Button(buttons_frame, text="Upload Audio File", command=upload_audio_file)
upload_button.grid(row=0, column=2, padx=5)

# Export transcription button
export_button = ttk.Button(buttons_frame, text="Export Transcription", command=export_transcription)
export_button.grid(row=0, column=3, padx=5)

# Exit button
exit_button = ttk.Button(buttons_frame, text="Exit", command=root.destroy)
exit_button.grid(row=0, column=4, padx=5)

root.mainloop()

