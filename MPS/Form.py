import os
from ctypes import windll
import subprocess
import webbrowser
import shutil

import pyaudio
import wave
from pydub import AudioSegment

import customtkinter as ctk
from tkinter import Menu, filedialog
from tkinter import ttk
from PIL import Image

# Set ffmpeg path
AudioSegment.converter = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')


class FileOperations:
    def __init__(self, right_frame):
        self.right_frame = right_frame
        self.song_list_path = "../Audio/song_list.txt"
        self.audio_folder = os.path.join("..", "Audio")
        self.existing_songs = self.load_existing_songs()

    def load_existing_songs(self):
        """Load existing songs from the song list file."""
        if not os.path.exists(self.song_list_path):
            return set()
        with open(self.song_list_path, "r") as file:
            return set(line.strip() for line in file)

    def save_song(self, song_name):
        """Append a new song to the song list file."""
        with open(self.song_list_path, "a") as file:
            file.write(song_name + "\n")

    def move_files(self):
        """Move and convert selected audio files to WAV format."""
        file_paths = filedialog.askopenfilenames(title="Open")
        for file_path in file_paths:
            file_name_without_extension = os.path.basename(file_path).rsplit(".", 1)[0]

            if file_name_without_extension in self.existing_songs:
                print(f"Audio file {file_name_without_extension} has already been imported")
                continue

            new_folder = os.path.join(self.audio_folder, file_name_without_extension)
            os.makedirs(new_folder, exist_ok=True)
            wav_path = os.path.join(new_folder, file_name_without_extension + ".wav")

            try:
                audio = AudioSegment.from_file(file_path)
                audio.export(wav_path, format="wav")
                self.save_song(file_name_without_extension)
                self.existing_songs.add(file_name_without_extension)
            except Exception as e:
                print(f"Error occurred while processing {file_path}: {e}")

        self.update_songs_list()

    def move_folder(self):
        """Move and convert all audio files in a selected folder to WAV format."""
        folder_path = filedialog.askdirectory(title="Select Folder")
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                file_name_without_extension = filename.rsplit(".", 1)[0]

                if file_name_without_extension in self.existing_songs:
                    print(f"Audio file {file_name_without_extension} has already been imported")
                    continue

                new_folder = os.path.join(self.audio_folder, file_name_without_extension)
                os.makedirs(new_folder, exist_ok=True)
                wav_path = os.path.join(new_folder, file_name_without_extension + ".wav")

                try:
                    audio = AudioSegment.from_file(os.path.join(dirpath, filename))
                    audio.export(wav_path, format="wav")
                    self.save_song(file_name_without_extension)
                    self.existing_songs.add(file_name_without_extension)
                except Exception as e:
                    print(f"Error occurred while processing {os.path.join(dirpath, filename)}: {e}")

        self.update_songs_list()

    def delete_all_songs(self):
        """Delete all songs and clear the song list file."""
        if os.path.exists(self.audio_folder):
            shutil.rmtree(self.audio_folder)
        open(self.song_list_path, 'w').close()  # Clear the song list file
        self.existing_songs.clear()
        self.update_songs_list()

    def update_songs_list(self):
        """Update the songs list view."""
        self.right_frame.songs_list.update_songs_list()  # Update the Treeview


class ThemeManager:
    @staticmethod
    def set_dark_theme():
        style = ttk.Style()
        ctk.set_appearance_mode("Dark")
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="#d0d0d0", fieldbackground="#2b2b2b")
        style.configure("Treeview.Heading", background="#333333", foreground="#d0d0d0", relief='flat')
        app.frame_right.songs_list.song_treeview.tag_configure("even", background="#2e2e2e")
        app.frame_right.songs_list.song_treeview.tag_configure("odd", background="#333333")

    @staticmethod
    def set_light_theme():
        style = ttk.Style()
        ctk.set_appearance_mode("Light")
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="#000000", fieldbackground="#dbdbdb")
        style.configure("Treeview.Heading", background="#e3e3e3", foreground="#000000", relief='flat')
        app.frame_right.songs_list.song_treeview.tag_configure("even", background="#dbdbdb")
        app.frame_right.songs_list.song_treeview.tag_configure("odd", background="#e3e3e3")


class TitleBarRight(ctk.CTkFrame):
    """Title bar right class. Contains buttons for closing and minimizing"""

    def __init__(self, master):
        super().__init__(master=master, corner_radius=0, fg_color="transparent")

        self.grid_columnconfigure(0, minsize=70, weight=1)
        self.grid_columnconfigure(1, minsize=70, weight=0)

        self.__creating_objects()
        self.__events()

    """GUI Private Methods"""

    def __creating_objects(self):
        self.close_button = ctk.CTkButton(master=self,
                                          width=70,
                                          height=36,
                                          text='×',
                                          font=(None, 25),
                                          corner_radius=0,
                                          text_color=("Black", "White"),
                                          fg_color="transparent",
                                          hover_color=("White", "Black"),
                                          command=quit
                                          )
        self.minimize_button = ctk.CTkButton(master=self,
                                             width=70,
                                             height=36,
                                             text='—',
                                             font=(None, 15),
                                             corner_radius=0,
                                             text_color=("Black", "White"),  # TODO text
                                             fg_color="transparent",
                                             hover_color=("White", "Black"),  # TODO hover
                                             command=self.minimize
                                             )
        self.minimize_button.grid(row=0, column=0, sticky="nes")
        self.close_button.grid(row=0, column=1, sticky="news")

    # These events are duplicated in the TitleBarLeft
    def __events(self):
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.move_window)

    """Functional Public Methods"""

    def start_move(self, event):
        self._drag_start_x = event.x + 240  # Add size of column 0 to correctly position the cursor along the x-axis
        self._drag_start_y = event.y

    def move_window(self, event):
        x = self.winfo_pointerx() - self._drag_start_x
        y = self.winfo_pointery() - self._drag_start_y
        self.master.geometry(f'+{x}+{y}')

    # TODO add window maximization from the taskbar
    def minimize(self):
        # get the handle to the taskbar
        hwnd = windll.user32.GetParent(self.master.winfo_id())
        # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
        windll.user32.ShowWindow(hwnd, 2)


class TitleBarLeft(ctk.CTkFrame):
    """Title bar left class. Contains logo button and menu"""

    def __init__(self, master, file_operations):
        super().__init__(master=master, corner_radius=0)
        self.file_operations = file_operations

        self.grid_columnconfigure(0, weight=1)
        self.logo_button_image = ctk.CTkImage(dark_image=Image.open("Images/Logo/DarkLogo.png"),
                                              light_image=Image.open("Images/Logo/WhiteLogo.png"),
                                              size=(30, 28))
        self.hover_logo_button_image = {
            "Light": ctk.CTkImage(Image.open("Images/Logo/WhiteLogoHover.png"), size=(30, 28)),
            "Dark": ctk.CTkImage(Image.open("Images/Logo/DarkLogoHover.png"), size=(30, 28))}

        self.__creating_objects()
        self.__creating_menu()
        self.__events()

    """GUI Private Methods"""

    def __creating_objects(self):
        self.logo_button = ctk.CTkButton(master=self,
                                         width=35,
                                         height=30,
                                         fg_color="transparent",
                                         text="",
                                         command=lambda: self.logo_menu.post(x=self.master.winfo_rootx(),
                                                                             y=self.master.winfo_rooty() + self.logo_button.winfo_height()),
                                         hover=False,
                                         image=self.logo_button_image
                                         )
        self.logo_button.grid(row=0, column=0, padx=(2, 0), pady=(5, 0), sticky="w")

    def __creating_menu(self):
        self.logo_menu = Menu(master=self, tearoff=0)

        # TODO yeah, link to github repo
        self.logo_menu.add_command(label="About", command=lambda: webbrowser.open("https://github.com"))
        self.logo_menu.add_separator()

        self.logo_menu.add_command(label="Open Files", command=self.file_operations.move_files)
        self.logo_menu.add_command(label="Open Folder", command=self.file_operations.move_folder)
        self.logo_menu.add_separator()

        self.appearance_menu = Menu(self, tearoff=0)
        self.appearance_menu.add_radiobutton(label="Light", command=ThemeManager.set_light_theme)
        self.appearance_menu.add_radiobutton(label="Dark", command=ThemeManager.set_dark_theme)
        self.logo_menu.add_cascade(label="Theme", menu=self.appearance_menu)

        self.logo_menu.add_command(label="Clear Downloads", command=self.file_operations.delete_all_songs)
        self.logo_menu.add_separator()

        self.logo_menu.add_command(label="Exit", command=quit)

    # self.bind are duplicated in the TitleBarRight
    def __events(self):
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.move_window)

        self.logo_button.bind("<Enter>", lambda event: self.logo_button.configure(
            image=self.hover_logo_button_image.get(ctk.get_appearance_mode())))
        self.logo_button.bind("<Leave>", lambda event: self.logo_button.configure(image=self.logo_button_image))

    '''Functional Public Methods'''

    def start_move(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def move_window(self, event):
        x = self.winfo_pointerx() - self._drag_start_x
        y = self.winfo_pointery() - self._drag_start_y
        self.master.geometry(f'+{x}+{y}')

    # TODO add window maximization from the taskbar
    def minimize(self):
        # get the handle to the taskbar
        hwnd = windll.user32.GetParent(self.master.winfo_id())
        # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
        windll.user32.ShowWindow(hwnd, 2)


class LeftFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)

        self.vinyl_disk_image = ctk.CTkImage(dark_image=Image.open("Images/Buttons/VinylDiskLight.png"),
                                             light_image=Image.open("Images/Buttons/VinylDiskDark.png"),
                                             size=(225, 225))

        self.album_cover_label = ctk.CTkLabel(master=self, image=self.vinyl_disk_image, text="")
        self.album_cover_label.grid(row=1, column=0, padx=(10, 0), pady=(20, 10), sticky="news")


class RightFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=300)

        self.__creating_objects()
        self.songs_list = self.CreatingTreeview(master=self)

    class CreatingTreeview(ctk.CTkFrame):
        def __init__(self, master):
            super().__init__(master=master, fg_color="transparent")
            self.grid(row=1, column=0, columnspan=3, sticky="news")
            self.songs_list = []

            self.song_treeview = ttk.Treeview(self, columns=("name", "length"), show="headings")
            self.song_treeview.grid(padx=(10, 0), pady=10, row=1, column=0, sticky="nse")
            self.song_treeview.heading("name", text="Name")
            self.song_treeview.heading("length", text="Length")
            self.song_treeview.column("name", anchor="w", width=325)
            self.song_treeview.column("length", anchor="w", width=50)

            self.scrollbar = ctk.CTkScrollbar(self,
                                              orientation="vertical",
                                              command=self.song_treeview.yview,
                                              button_color="#bdbdbd",
                                              button_hover_color="#adadad"
                                              )
            self.song_treeview.configure(yscrollcommand=self.scrollbar.set)

            self.scrollbar.grid(row=1, column=1, sticky="ns")

            # TODO delete
            self.update_songs_list()

            self.song_treeview.bind("<Double-1>", self.on_item_click)

        def on_item_click(self, event):
            selected_item = self.song_treeview.focus()
            song_name = self.song_treeview.item(selected_item, "values")[0]
            print("Ви вибрали пісню:", song_name)

        def update_songs_list(self):
            self.songs_list = []
            self.song_treeview.delete(*self.song_treeview.get_children())

            if os.path.isfile("../Audio/song_list.txt"):
                with open("../Audio/song_list.txt", "r") as song_list:
                    for index, song_name in enumerate(song_list):
                        song_name = song_name.strip()
                        tag = "even" if index % 2 == 0 else "odd"
                        self.song_treeview.insert("", "end", values=(song_name,), tags=(tag,))
                print("Treeview updated")

    def __creating_objects(self):
        self.search_label = ctk.CTkLabel(self, width=30, height=30, anchor="w", text="Search")
        self.add_button = ctk.CTkButton(master=self,
                                        width=30,
                                        height=30,
                                        fg_color="red",
                                        text="Plus",
                                        command=lambda: self.add_menu.post(x=self.add_button.winfo_rootx(),
                                                                           y=self.add_button.winfo_rooty() + self.add_button.winfo_height()),
                                        hover=False,
                                        )
        self.delete_button = ctk.CTkButton(master=self,
                                           width=30,
                                           height=30,
                                           fg_color="Red",
                                           text="Minus",
                                           command=None,
                                           hover=False,
                                           )

        self.add_menu = Menu(master=self, tearoff=0)

        self.add_menu.add_command(label="Open Files", command=FileOperations.move_files)
        self.add_menu.add_command(label="Open Folder", command=FileOperations.move_folder)

        self.search_label.grid(row=2, column=0, sticky="news", padx=(10, 0))
        self.add_button.grid(row=2, column=1, sticky="news")
        self.delete_button.grid(row=2, column=2, sticky="news")


class BottomFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)
        self.grid_columnconfigure((0, 1, 2), weight=0)  # Ліва сторона розширюється
        self.grid_columnconfigure((3, 4), weight=1)  # Ліва сторона розширюється
        self.grid_columnconfigure((5, 6, 7), weight=0)  # Ліва сторона розширюється

        self.album_cover_image = ctk.CTkImage(dark_image=Image.open("Images/Buttons/VinylDiskLight.png"),
                                              light_image=Image.open("Images/Buttons/VinylDiskDark.png"),
                                              size=(40, 40))

        self.album_cover_label = ctk.CTkLabel(master=self, image=self.album_cover_image, text="")
        self.album_cover_label.grid(row=0, column=3, padx=(0, 5), pady=(0, 0), sticky="nes")

        self.label = ctk.CTkLabel(self, width=30, height=30, text=f"Song name\nArtist nickname", anchor="e")
        self.label.grid(row=0, column=4, padx=(5, 0), pady=(0, 0), sticky="nws")

        self.images = {
            "next": ctk.CTkImage(dark_image=Image.open("Images/Buttons/NextLight.png"),
                                 light_image=Image.open("Images/Buttons/NextDark.png"),
                                 size=(40, 40)),
            "pause": ctk.CTkImage(dark_image=Image.open("Images/Buttons/PauseLight.png"),
                                  light_image=Image.open("Images/Buttons/PauseDark.png"),
                                  size=(40, 40)),
            "play": ctk.CTkImage(dark_image=Image.open("Images/Buttons/PlayLight.png"),
                                 light_image=Image.open("Images/Buttons/PlayDark.png"),
                                 size=(40, 40)),
            "previous": ctk.CTkImage(dark_image=Image.open("Images/Buttons/PreviousLight.png"),
                                     light_image=Image.open("Images/Buttons/PreviousDark.png"),
                                     size=(40, 40)),
            "repeat": ctk.CTkImage(dark_image=Image.open("Images/Buttons/RepeatLight.png"),
                                   light_image=Image.open("Images/Buttons/RepeatDark.png"),
                                   size=(40, 40)),
            "repeat_selected": ctk.CTkImage(dark_image=Image.open("Images/Buttons/RepeatLightSelected.png"),
                                            light_image=Image.open("Images/Buttons/RepeatDarkSelected.png"),
                                            size=(40, 40)),
            "shuffle": ctk.CTkImage(dark_image=Image.open("Images/Buttons/ShuffleLight.png"),
                                    light_image=Image.open("Images/Buttons/ShuffleDark.png"),
                                    size=(40, 40)),
            "volume": ctk.CTkImage(dark_image=Image.open("Images/Buttons/VolumeLight.png"),
                                   light_image=Image.open("Images/Buttons/VolumeDark.png"),
                                   size=(40, 40))
        }
        for i in self.images.items():
            setattr(self, i[0] + "_button", self.create_button(i[1]))

        self.previous_button.grid(row=0, column=0, pady=(10, 10), sticky="news")
        self.pause_button.grid(row=0, column=1, pady=(10, 10), sticky="news")
        self.next_button.grid(row=0, column=2, pady=(10, 10), sticky="news")
        self.volume_button.grid(row=0, column=5, pady=(10, 10), sticky="news")
        self.repeat_button.grid(row=0, column=6, pady=(10, 10), sticky="news")
        self.shuffle_button.grid(row=0, column=7, pady=(10, 10), sticky="news")

    def create_button(self, image, command=...):
        button = ctk.CTkButton(master=self,
                               width=40,
                               height=40,
                               fg_color="transparent",
                               text="",
                               command=command,
                               hover=False,
                               image=image)
        return button


class MPS(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x600")
        self.overrideredirect(True)
        self.iconbitmap("Images/Logo/Ico.ico")
        self.attributes("-alpha", 1.0)
        self.grid_rowconfigure(0, minsize=36, weight=1)
        self.grid_rowconfigure(1, minsize=495, weight=1)
        self.grid_rowconfigure(2, minsize=75, weight=1)
        self.grid_columnconfigure(0, minsize=240, weight=1)
        self.grid_columnconfigure(1, minsize=340, weight=1)
        self.grid_columnconfigure(2, minsize=400, weight=1)

        self.frame_center = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_right = ctk.CTkFrame(self)

        self.frame_center.grid(row=1, column=1, padx=(3, 3), pady=(0, 0), sticky="news")

        self.frame_left = LeftFrame(master=self, )
        self.frame_left.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="news")
        self.frame_bottom = BottomFrame(master=self)
        self.frame_bottom.grid(row=2, column=0, columnspan=3, padx=(0, 0), pady=(5, 10), sticky="news")
        self.frame_right = RightFrame(master=self)
        self.frame_right.grid(row=1, column=2, padx=(3, 0), pady=(0, 0), sticky="news")
        self.title_bar_left = TitleBarLeft(master=self, file_operations=FileOperations(self.frame_right))
        self.title_bar_left.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="news")
        self.title_bar_right = TitleBarRight(master=self)
        self.title_bar_right.grid(row=0, column=1, columnspan=2, padx=(0, 0), pady=(0, 0), sticky="news")


if __name__ == "__main__":
    app = MPS()
    ThemeManager.set_dark_theme() if ctk.get_appearance_mode() == "Dark" else ThemeManager.set_light_theme()
    app.mainloop()

