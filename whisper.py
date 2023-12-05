import pyaudio
import wave
import openai

openai.api_key = "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"

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

record_flag = True
user_content = ''

def voice_to_text():
    global record_flag, user_content
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []
    print("録音中...")
    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            if (record_flag):
                break
    except KeyboardInterrupt:
        pass
    print("録音終了")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # WAVファイルとして保存
    wave_output_filename = 'user_audio.wav'
    with wave.open(wave_output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    # WAVファイルを読み込んでtranscribeメソッドに渡す
    with open(wave_output_filename, 'rb') as audio_file:
        transcript = openai.Audio.transcribe('whisper-1', audio_file)
        user_content = transcript['text']
