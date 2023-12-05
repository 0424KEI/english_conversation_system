import pygame
import time

def play_mp3(file_path):
    # Pygameの初期化
    pygame.init()

    try:
        # MP3ファイルの読み込み
        pygame.mixer.music.load(file_path)

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

# MP3ファイルのパスを指定して再生
mp3_file_path = "test.mp3"
play_mp3(mp3_file_path)
