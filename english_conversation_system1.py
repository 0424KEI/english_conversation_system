import pyaudio
import wave
import asyncio
import edge_tts
import pygame
import time
import readchar
import threading
from openai import OpenAI
client = OpenAI(api_key='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')



FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

record_flag = False
user_content = ''
chatgpt_content = ''
chatgpt_messages = []
chatgpt_voice = 'en-GB-SoniaNeural'
mp3_output_filename = 'chatgpt_audio.mp3'
wave_output_filename = 'user_audio.wav'

def speech_to_text():
    global record_flag, user_content, wave_output_filename, client
    record_flag = True
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []
    print("recording...")
    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            if not(record_flag):
                break
    except KeyboardInterrupt:
        pass
    print("recording finished")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # WAVファイルとして保存
    with wave.open(wave_output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    # WAVファイルを読み込んでtranscribeメソッドに渡す
    with open(wave_output_filename, 'rb') as audio_file:
        response = client.audio.translations.create(
            model="whisper-1", 
            file=audio_file,
        )
        # print(f'response: {response}')
        user_content = response.text
        

def chatgpt_api():
    global chatgpt_content, chatgpt_messages, client
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chatgpt_messages
    )
    # print(f'response: {response}')
    chatgpt_content = response.choices[0].message.content


def text_to_speech():
    global chatgpt_content, chatgpt_voice, mp3_output_filename
    async def amain() -> None:
        communicate = edge_tts.Communicate(text=chatgpt_content, voice=chatgpt_voice)
        # communicate = edge_tts.Communicate(text=chatgpt_content, voice=chatgpt_voice, rate='-50%') // rate=''でスピード調整 
        await communicate.save(mp3_output_filename)
    # 新しいイベントループを作成
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(amain())
    finally:
        loop.close()

def play_mp3_file():
    global mp3_output_filename
    # Pygameの初期化
    pygame.init()

    try:
        # MP3ファイルの読み込み
        pygame.mixer.music.load(mp3_output_filename)

        # 音声の再生
        pygame.mixer.music.play()

        # 再生中かどうかを確認し、再生が終了するまで待機
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    except pygame.error as e:
        print(f"Error: {e}")
    finally:
        # Pygameの終了
        pygame.quit()

def main():
    global chatgpt_messages, user_content, chatgpt_content
    speech_to_text()
    chatgpt_content = user_content.replace('\n','')
    chatgpt_messages.append({'role': 'user', 'content': user_content})
    chatgpt_api()
    chatgpt_content = chatgpt_content.replace('\n','')
    chatgpt_messages.append({'role': 'assistant', 'content': chatgpt_content})
    # print(f'chatgpt_messages: {chatgpt_messages}')
    print(f'User: {user_content}')
    print(f'Conversation Partner: {chatgpt_content}')
    text_to_speech()
    play_mp3_file()

def keyboad_process():
    global record_flag
    system_content = input("Please set the conversation partner: ")
    chatgpt_messages.append({'role': 'system', 'content': system_content})
    while True:
        c = readchar.readkey()
        if c == '\n':
            main_thread = threading.Thread(target=main)
            main_thread.start()
            c = readchar.readkey()
            if c == '\n':
                record_flag = False


if __name__ == "__main__":
    keyboad_process()