import pyaudio
import wave
import os
import threading

song = None
position = 0
p = pyaudio.PyAudio()
stream = None
is_playing = False
music_thread = None
pause_event = threading.Event()


def get_song_name(name):
    global song, position
    song_folder = os.path.join("..", "Audio", name)
    song_path = os.path.join(song_folder, name + ".wav")
    try:
        song = wave.open(song_path, "rb")
        position = 0
        print(f"Loaded song: {name}")
    except FileNotFoundError:
        print(f"Error: The file {song_path} was not found.")
    except wave.Error as e:
        print(f"Error: The file {song_path} could not be opened as a WAV file. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def play_pause_music():
    global is_playing
    if not is_playing:
        if pause_event.is_set():
            pause_event.clear()
            is_playing = True
        else:
            play_music()
    else:
        pause_music()


def play_music():
    global music_thread, is_playing

    def play():
        global stream, position, is_playing
        if song is None:
            print("No song loaded for playback.")
            return
        if stream is None or not stream.is_active():
            stream = p.open(format=p.get_format_from_width(song.getsampwidth()),
                            channels=song.getnchannels(),
                            rate=song.getframerate(),
                            output=True)
        song.setpos(position)
        while stream.is_active():
            if pause_event.is_set():
                pause_event.wait()
                continue
            data = song.readframes(1024)
            if not data:
                break
            stream.write(data)
            position = song.tell()
        stream.stop_stream()
        stream.close()
        stream = None
        is_playing = False

    if music_thread is None or not music_thread.is_alive():
        pause_event.clear()
        music_thread = threading.Thread(target=play)
        music_thread.start()
        is_playing = True


def pause_music():
    global is_playing
    pause_event.set()
    is_playing = False

# TODO Del all songs
# TODO Double click
# TODO Close app
