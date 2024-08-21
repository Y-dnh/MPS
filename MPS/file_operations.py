import os
from tkinter import filedialog
from pydub import AudioSegment
import shutil

# Set ffmpeg path
AudioSegment.converter = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')


def get_right_frame(right_frame):
    """
    Sets the global variable `frame` to the provided `right_frame`.

    This function assigns the `right_frame` argument to the global `frame` variable. The `frame`
    variable is used to reference the right-side frame in the application, allowing other parts
    of the code to access and modify this frame's attributes and methods.

    Args:
        right_frame (ctk.CTkFrame): The right-side frame to be assigned to the global `frame` variable.
            This should be an instance of the `RightFrame` class or a compatible frame object
            that contains the `songs_list` attribute.

    Note:
        - This function modifies the global variable `frame`, so ensure it is called with the correct
          frame instance before attempting to use `frame` in other functions or methods.
    """
    global frame
    frame = right_frame


def load_existing_songs():
    """
    Loads existing songs from the song list file.

    Returns:
        set: A set of song names loaded from the song list file. If the file does not exist, returns an empty set.

    Notes:
        The function reads from a global variable `song_list_path` which should specify the path to the song list file.
        Each line in the file is treated as a song name and is added to the returned set.
    """
    if not os.path.exists(song_list_path):
        return set()
    with open(song_list_path, "r") as file:
        return set(line.strip() for line in file)


def save_song(song_name):
    """
    Appends a new song name to the song list file.

    Args:
        song_name (str): The name of the song to be added to the song list file.

    Notes:
        The function appends the song name to the file specified by the global variable `song_list_path`.
        If the file does not exist, it will be created. Each song name is written on a new line.
    """
    with open(song_list_path, "a") as file:
        file.write(song_name + "\n")


def move_files():
    """
    Move and convert selected audio files to WAV format.

    This function opens a file dialog for the user to select audio files. For each selected file:
    - If the file's name (without extension) is not already in the existing songs set, it creates a new directory
      in the specified audio folder with the same name as the file (without extension).
    - Converts the audio file to WAV format and saves it in the new directory.
    - Updates the list of existing songs by adding the name of the new file.
    - Handles any exceptions that occur during file processing and logs an error message.

    Notes:
        The function uses the `filedialog` module to select files and `AudioSegment` from `pydub` to process audio files.
    """
    file_paths = filedialog.askopenfilenames(title="Open")
    for file_path in file_paths:
        file_name_without_extension = os.path.basename(file_path).rsplit(".", 1)[0]

        if file_name_without_extension in existing_songs:
            # TODO ...
            print(f"Audio file {file_name_without_extension} has already been imported")
            continue

        new_folder = os.path.join(audio_folder, file_name_without_extension)  # Creating new folder for the song with similar name
        os.makedirs(new_folder, exist_ok=True)
        wav_path = os.path.join(new_folder, file_name_without_extension + ".wav")  # Path where the song will be posted

        try:
            audio = AudioSegment.from_file(file_path)  # Load the audio file
            audio.export(wav_path, format="wav")  # Export the audio as WAV format
            save_song(file_name_without_extension)  # Save the song name to the list
            existing_songs.add(file_name_without_extension)  # Add the song to the set of existing songs
        except Exception as e:
            print(f"Error occurred while processing {file_path}: {e}")

    update_songs_list()


def move_folder():
    """
    Move and convert all audio files in a selected folder to WAV format.

    Opens a directory dialog for the user to select a folder. For each audio file found within the selected folder
    and its subdirectories:
    - If the file's name (without extension) is not already in the existing songs set, it creates a new directory
      in the specified audio folder with the same name as the file (without extension).
    - Converts the audio file to WAV format and saves it in the new directory.
    - Updates the list of existing songs by adding the name of the new file.
    - Handles any exceptions that occur during file processing and logs an error message.

    Notes:
        The function uses the `filedialog` module to select the folder and `AudioSegment` from `pydub` to process audio files.
    """
    folder_path = filedialog.askdirectory(title="Select Folder")
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_name_without_extension = filename.rsplit(".", 1)[0]

            if file_name_without_extension in existing_songs:
                print(f"Audio file {file_name_without_extension} has already been imported")
                continue

            new_folder = os.path.join(audio_folder, file_name_without_extension)  # Creating new folder for the song with similar name
            os.makedirs(new_folder, exist_ok=True)
            wav_path = os.path.join(new_folder, file_name_without_extension + ".wav")  # Path where the song will be posted

            try:
                audio = AudioSegment.from_file(os.path.join(dirpath, filename))  # Load the audio file
                audio.export(wav_path, format="wav")  # Export the audio as WAV format
                save_song(file_name_without_extension)  # Save the song name to the list
                existing_songs.add(file_name_without_extension)  # Add the song to the set of existing songs
            except Exception as e:
                print(f"Error occurred while processing {os.path.join(dirpath, filename)}: {e}")

    update_songs_list()


def delete_all_songs():
    """Delete all songs and clear the song list file."""
    open(song_list_path, 'w').close()  # Clear the song list file
    existing_songs.clear()  # Clear set of songs
    update_songs_list()  # Update treeview
    if os.path.exists(audio_folder):
        shutil.rmtree(audio_folder)  # Delete the folder with all songs


def update_songs_list():
    """
    Update the songs list view.

    This function updates the list of songs displayed in the UI. It does so by calling the
    `update_songs_list` method on the `songs_list` attribute of the `frame` object, which is
    an instance of the `CreatingTreeview` class within the `RightFrame` class.

    The `frame` object is set via the `get_right_frame` function and represents the right frame.
    This allows the `update_songs_list` function to refresh the song list
    view in the `RightFrame`'s Treeview widget.

    Notes:
        - Ensure that the `frame` object has been properly initialized and is an instance of the
          `RightFrame` class with an attribute `songs_list` having an `update_songs_list` method.
        - The `get_right_frame` function should be used to set the `frame` object before calling
          this function.
    """
    frame.songs_list.update_songs_list()  # Update the Treeview


song_list_path = "../Audio/song_list.txt"
audio_folder = os.path.join("..", "Audio")
existing_songs = load_existing_songs()
