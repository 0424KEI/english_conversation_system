"""
Basic example of edge_tts usage.
"""

import asyncio

import edge_tts

TEXT = "of course. Once upon a time, there was an old man who lived in a small village. This old lady was very curious and she was always looking for new adventures."
VOICE = "en-GB-SoniaNeural"
OUTPUT_FILE = "test.mp3"


async def amain() -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(amain())
    finally:
        loop.close()

# https://www.toyo.co.jp/onetech_blog/articles/detail/id=38865
# https://github.com/rany2/edge-tts