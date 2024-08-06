import os
from ctypes import windll
import subprocess
import webbrowser

import pyaudio
import wave
from pydub import AudioSegment

import customtkinter as ctk
from tkinter import Menu, filedialog
from tkinter import ttk
from PIL import Image


def find_ffmpeg():
    """
    Finds the location of `ffmpeg.exe` by checking the system PATH variable.
    Ensure that the directory containing `ffmpeg.exe` is included in the PATH environment variable.
    """

    try:
        result = subprocess.run(["where", "ffmpeg"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# Set ffmpeg path
AudioSegment.converter = find_ffmpeg()


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

    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)

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

        self.logo_menu.add_command(label="Open Files", command=self.move_files)
        self.logo_menu.add_command(label="Open Folder", command=self.move_folder)
        self.logo_menu.add_separator()

        self.appearance_menu = Menu(self, tearoff=0)
        self.appearance_menu.add_radiobutton(label="Light", command=lambda: ctk.set_appearance_mode("Light"))
        self.appearance_menu.add_radiobutton(label="Dark", command=lambda: ctk.set_appearance_mode("Dark"))
        self.logo_menu.add_cascade(label="Theme", menu=self.appearance_menu)

        # TODO add commands
        self.logo_menu.add_command(label="Clear Downloads", command=...)
        self.logo_menu.add_command(label="Storage Location", command=...)
        self.logo_menu.add_separator()

        self.logo_menu.add_command(label="Exit", command=quit)

    # These events are duplicated in the TitleBarRight
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

    @staticmethod
    def move_files():
        file_paths = filedialog.askopenfilenames(title="Open")
        for file_path in file_paths:
            file_name_without_extension = os.path.basename(file_path).rsplit(".", 1)[0]
            new_folder = os.path.join("..", "Audio", file_name_without_extension)
            try:
                os.makedirs(new_folder, exist_ok=True)
                audio = AudioSegment.from_file(file_path)
                wav_path = os.path.join(new_folder, file_name_without_extension + ".wav")
                audio.export(wav_path, format="wav")
            except FileExistsError:
                print(f"Audio file {file_name_without_extension} has already been imported")

    @staticmethod
    def move_folder():
        folder_path = filedialog.askdirectory(title="Select Folder")
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                file_name_without_extension = filename.rsplit(".", 1)[0]
                new_folder = os.path.join("..", "Audio", file_name_without_extension)
                try:
                    os.makedirs(new_folder, exist_ok=True)
                    audio = AudioSegment.from_file(os.path.join(dirpath, filename))
                    wav_path = os.path.join(new_folder, file_name_without_extension + ".wav")
                    audio.export(wav_path, format="wav")
                except FileExistsError:
                    print(f"Audio file {filename} has already been imported")


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
        # self.audio_list = ttk.Treeview()
        # self.audio_list.grid(row=0, column=0)


class BottomFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)
        self.grid_columnconfigure((0, 1, 2), weight=0)  # Ліва сторона розширюється
        self.grid_columnconfigure(3, weight=1)  # Ліва сторона розширюється
        self.grid_columnconfigure((4, 5, 6), weight=0)  # Ліва сторона розширюється

        self.album_cover_image = ctk.CTkImage(dark_image=Image.open("Images/Buttons/VinylDiskLight.png"),
                                              light_image=Image.open("Images/Buttons/VinylDiskDark.png"),
                                              size=(40, 40))

        self.album_cover_label = ctk.CTkLabel(master=self, image=self.album_cover_image, text="")
        self.album_cover_label.grid(row=0, column=3, padx=(0, 0), pady=(0, 0), sticky="news")

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
        self.volume_button.grid(row=0, column=4, pady=(10, 10), sticky="news")
        self.repeat_button.grid(row=0, column=5, pady=(10, 10), sticky="news")
        self.shuffle_button.grid(row=0, column=6, pady=(10, 10), sticky="news")

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

        self.title_bar_left = TitleBarLeft(master=self)
        self.title_bar_left.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="news")
        self.title_bar_right = TitleBarRight(master=self)
        self.title_bar_right.grid(row=0, column=1, columnspan=2, padx=(0, 0), pady=(0, 0), sticky="news")
        self.frame_left = LeftFrame(master=self)
        self.frame_left.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="news")
        self.frame_bottom = BottomFrame(master=self)
        self.frame_bottom.grid(row=2, column=0, columnspan=3, padx=(0, 0), pady=(5, 10), sticky="news")
        self.frame_right = RightFrame(master=self)
        self.frame_right.grid(row=1, column=2, padx=(3, 0), pady=(0, 0), sticky="news")


if __name__ == "__main__":
    app = MPS()
    app.mainloop()
