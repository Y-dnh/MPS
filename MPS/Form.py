import os
from ctypes import windll
import webbrowser
import threading

import customtkinter as ctk
from tkinter import Menu
from tkinter import ttk
from PIL import Image

import file_operations
import music_controls


class ThemeManager:
    """
    The ThemeManager class is responsible for setting the application's theme to either dark or light mode.
    """

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
    """
    The `TitleBarRight` class is responsible for creating and managing the custom right-side title bar of the application,
    including buttons for closing and minimizing the window.

    Args:
        master (ctk.CTk): The parent widget to which this title bar frame belongs.
    """

    def __init__(self, master):
        super().__init__(master=master, corner_radius=0, fg_color="transparent")

        self.grid_columnconfigure(0, minsize=70, weight=1)  # The minimize button expands to fill available space
        self.grid_columnconfigure(1, minsize=70, weight=0)  # The close button has a fixed width and does not expand

        self.__creating_objects()
        self.__events()

    def __creating_objects(self):
        """
        Creates and configures the close and minimize buttons for the title bar.
        """
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
                                             text_color=("Black", "White"),
                                             fg_color="transparent",
                                             hover_color=("White", "Black"),
                                             command=self.minimize
                                             )
        self.minimize_button.grid(row=0, column=0, sticky="nes")
        self.close_button.grid(row=0, column=1, sticky="news")

    def __events(self):
        """
        Binds events to methods for moving the window by clicking and dragging the title bar.
        """
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.move_window)

    def start_move(self, event):
        """
        Initiates the window movement process by recording the starting position of the cursor.

        Args:
            event (tkinter.Event): The event containing the mouse click position.
        """
        self._drag_start_x = event.x + 240  # Add size of column 0 to correctly position the cursor along the x-axis
        self._drag_start_y = event.y

    def move_window(self, event):
        """
        Moves the window according to the mouse movement while dragging.

        Args:
            event (tkinter.Event): The event containing the current position of the cursor.
        """
        x = self.winfo_pointerx() - self._drag_start_x
        y = self.winfo_pointery() - self._drag_start_y
        self.master.geometry(f'+{x}+{y}')

    def minimize(self):
        """
        Minimizes the application window to the taskbar.

        Note:
            This method is specifically designed for Windows operating systems.
        """
        hwnd = windll.user32.GetParent(self.master.winfo_id())
        #  https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
        windll.user32.ShowWindow(hwnd, 2)


class TitleBarLeft(ctk.CTkFrame):
    """
    A custom left-side title bar for managing the window's title bar controls, including
    a logo button and a menu with various options.

    Args:
        master (ctk.CTk): The parent widget to which this title bar frame belongs.
        right_frame (ctk.CTkFrame): The right-side frame - RightFrame object
    """

    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)

        self.grid_columnconfigure(0, weight=1)
        self.logo_button_image = ctk.CTkImage(
            dark_image=Image.open("Images/Logo/DarkLogo.png"),
            light_image=Image.open("Images/Logo/WhiteLogo.png"),
            size=(30, 28)
        )
        self.hover_logo_button_image = {
            "Light": ctk.CTkImage(Image.open("Images/Logo/WhiteLogoHover.png"), size=(30, 28)),
            "Dark": ctk.CTkImage(Image.open("Images/Logo/DarkLogoHover.png"), size=(30, 28))
        }

        self.__creating_objects()
        self.__creating_menu()
        self.__events()

    def __creating_objects(self):
        """
        Create and configure the logo button for the title bar.
        """
        self.logo_button = ctk.CTkButton(master=self,
                                         width=35,
                                         height=30,
                                         text="",
                                         fg_color="transparent",
                                         command=lambda: self.logo_menu.post(
                                             x=self.master.winfo_rootx(),
                                             y=self.master.winfo_rooty() + self.logo_button.winfo_height()
                                         ),
                                         hover=False,
                                         image=self.logo_button_image
                                         )
        self.logo_button.grid(row=0, column=0, padx=(2, 0), pady=(5, 0), sticky="w")

    def __creating_menu(self):
        """
        Create and configure the menu that appears when clicking the logo button.
        Includes options for theme, file operations, and exiting the application.
        """
        self.logo_menu = Menu(master=self, tearoff=0)

        # TODO: Link to GitHub repository
        self.logo_menu.add_command(label="About", command=lambda: webbrowser.open("https://github.com"))
        self.logo_menu.add_separator()

        self.logo_menu.add_command(label="Open Files", command=file_operations.move_files)
        self.logo_menu.add_command(label="Open Folder", command=file_operations.move_folder)
        self.logo_menu.add_separator()

        self.appearance_menu = Menu(self, tearoff=0)
        self.appearance_menu.add_radiobutton(label="Light", command=ThemeManager.set_light_theme)
        self.appearance_menu.add_radiobutton(label="Dark", command=ThemeManager.set_dark_theme)
        self.logo_menu.add_cascade(label="Theme", menu=self.appearance_menu)

        self.logo_menu.add_command(label="Clear Downloads", command=file_operations.delete_all_songs)
        self.logo_menu.add_separator()

        self.logo_menu.add_command(label="Exit", command=quit)

    def __events(self):
        """
        Bind events to methods for moving the window and updating the logo button image on hover.
        """
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.move_window)

        self.logo_button.bind("<Enter>", lambda event: self.logo_button.configure(
            image=self.hover_logo_button_image.get(ctk.get_appearance_mode())))
        self.logo_button.bind("<Leave>", lambda event: self.logo_button.configure(image=self.logo_button_image))

    """Functional Public Methods"""

    def start_move(self, event):
        """
        Initiate the window movement process by recording the starting position of the cursor.

        Args:
            event (tkinter.Event): The event containing the mouse click position.
        """
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def move_window(self, event):
        """
        Move the window according to the mouse movement while dragging.

        Args:
            event (tkinter.Event): The event containing the current position of the cursor.
        """
        x = self.winfo_pointerx() - self._drag_start_x
        y = self.winfo_pointery() - self._drag_start_y
        self.master.geometry(f'+{x}+{y}')


class LeftFrame(ctk.CTkFrame):
    """
    A custom frame that displays an album cover as a vinyl disk image.

    Args:
        master (ctk.CTk): The parent widget to which this frame belongs.
    """

    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)

        self.vinyl_disk_image = ctk.CTkImage(dark_image=Image.open("Images/Buttons/VinylDiskLight.png"),
                                             light_image=Image.open("Images/Buttons/VinylDiskDark.png"),
                                             size=(225, 225))

        self.album_cover_label = ctk.CTkLabel(master=self, image=self.vinyl_disk_image, text="")
        self.album_cover_label.grid(row=1, column=0, padx=(10, 0), pady=(20, 10), sticky="news")


class CenterFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, corner_radius=0, fg_color="transparent")

        self.__creating_objects()

    def __creating_objects(self):
        self.bass_button = ctk.CTkButton(master=self,
                                         width=75,
                                         height=30,
                                         fg_color="Red",
                                         text="Bass",
                                         command=None,
                                         hover=True,
                                         )
        self.drum_button = ctk.CTkButton(master=self,
                                         width=75,
                                         height=30,
                                         fg_color="Red",
                                         text="Drum",
                                         command=None,
                                         hover=True,
                                         )
        self.vocals_button = ctk.CTkButton(master=self,
                                           width=75,
                                           height=30,
                                           fg_color="Red",
                                           text="Vocals",
                                           command=None,
                                           hover=True,
                                           )
        self.other_button = ctk.CTkButton(master=self,
                                          width=75,
                                          height=30,
                                          fg_color="Red",
                                          text="Other",
                                          command=None,
                                          hover=True,
                                          )

        self.bass_slider = ctk.CTkSlider(master=self,
                                         width=250,
                                         height=15,
                                         from_=0,
                                         to=100,
                                         number_of_steps=25,
                                         progress_color=("Red", "Red")
                                         )
        self.drum_slider = ctk.CTkSlider(master=self,
                                         width=250,
                                         height=15,
                                         from_=0,
                                         to=100,
                                         number_of_steps=25,
                                         progress_color=("Red", "Red")
                                         )
        self.vocals_slider = ctk.CTkSlider(master=self,
                                           width=250,
                                           height=15,
                                           from_=0,
                                           to=100,
                                           number_of_steps=25,
                                           progress_color=("Red", "Red")
                                           )
        self.other_slider = ctk.CTkSlider(master=self,
                                          width=250,
                                          height=15,
                                          from_=0,
                                          to=100,
                                          number_of_steps=25,
                                          progress_color=("Red", "Red")
                                          )
        self.bass_button.grid(row=0, column=0, pady=(20, 0), padx=(7, 0))
        self.drum_button.grid(row=1, column=0, pady=(35, 0), padx=(7, 0))
        self.vocals_button.grid(row=2, column=0, pady=(35, 0), padx=(7, 0))
        self.other_button.grid(row=3, column=0, pady=(35, 0), padx=(7, 0))

        self.bass_slider.grid(row=0, column=1, pady=(20, 0))
        self.drum_slider.grid(row=1, column=1, pady=(35, 0))
        self.vocals_slider.grid(row=2, column=1, pady=(35, 0))
        self.other_slider.grid(row=3, column=1, pady=(35, 0))


class RightFrame(ctk.CTkFrame):
    """
    A custom right-side frame that includes a tree view for displaying songs and buttons for managing them.

    Args:
        master (ctk.CTk): The parent widget to which this frame belongs.
    """

    def __init__(self, master):
        super().__init__(master=master)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=300)  # Search column fill available space

        self.__creating_objects()
        self.songs_list = self.CreatingTreeview(master=self)

    def __creating_objects(self):
        """
        Creates and configures widgets for the RightFrame, including search label,
        add button, delete button, and the add menu.
        """
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

        self.add_menu.add_command(label="Open Files", command=file_operations.move_files)
        self.add_menu.add_command(label="Open Folder", command=file_operations.move_folder)

        self.search_label.grid(row=2, column=0, sticky="news", padx=(10, 0))
        self.add_button.grid(row=2, column=1, sticky="news")
        self.delete_button.grid(row=2, column=2, sticky="news")

    class CreatingTreeview(ctk.CTkFrame):
        """
        A frame containing a tree view to display a list of songs.

        Args:
            master (ctk.CTk): The parent widget to which this frame belongs.
        """

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

            # TODO: Delete
            self.update_songs_list()

            self.song_treeview.bind("<Double-1>", self.on_item_click)

        def on_item_click(self, event):
            """
            Handles item click events in the tree view.

            Args:
                event (tkinter.Event): The event containing information about the mouse click.
            """
            selected_item = self.song_treeview.focus()
            song_name = self.song_treeview.item(selected_item, "values")[0]
            music_controls.get_song_name(song_name)

        def update_songs_list(self):
            """
            Updates the list of songs displayed in the Treeview widget.

            - Clears the current list of songs from the Treeview.
            - Reads the song names from the file "../Audio/song_list.txt" if it exists.
            - Inserts each song name into the Treeview with alternating row tags for visual distinction.
            - Logs a message indicating that the Treeview has been updated.

            Notes:
                - The song names are read from each line of the text file.
                - Rows are tagged as "even" or "odd" based on their index to alternate row colors.
            """
            self.songs_list = []
            self.song_treeview.delete(*self.song_treeview.get_children())

            if os.path.isfile("../Audio/song_list.txt"):
                with open("../Audio/song_list.txt", "r") as song_list:
                    for index, song_name in enumerate(song_list):
                        song_name = song_name.strip()
                        tag = "even" if index % 2 == 0 else "odd"
                        self.song_treeview.insert("", "end", values=(song_name,), tags=(tag,))
                print("Treeview updated")


class BottomFrame(ctk.CTkFrame):
    """
    A custom bottom frame for managing playback controls and displaying song information.

    Args:
        master (ctk.CTk): The parent widget to which this frame belongs.
    """

    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)

        self.grid_columnconfigure((0, 1, 2), weight=0)  # Columns 0, 1, and 2 have no expansion
        self.grid_columnconfigure((3, 4), weight=1)  # Columns 3 and 4 expand
        self.grid_columnconfigure((5, 6, 7), weight=0)  # Columns 5, 6, and 7 have no expansion

        self.album_cover_image = ctk.CTkImage(
            dark_image=Image.open("Images/Buttons/VinylDiskLight.png"),
            light_image=Image.open("Images/Buttons/VinylDiskDark.png"),
            size=(40, 40)
        )
        self.images = {
            "next": ctk.CTkImage(
                dark_image=Image.open("Images/Buttons/NextLight.png"),
                light_image=Image.open("Images/Buttons/NextDark.png"),
                size=(40, 40)
            ),
            "pause": ctk.CTkImage(
                dark_image=Image.open("Images/Buttons/PauseLight.png"),
                light_image=Image.open("Images/Buttons/PauseDark.png"),
                size=(40, 40)
            ),
            "play": ctk.CTkImage(
                dark_image=Image.open("Images/Buttons/PlayLight.png"),
                light_image=Image.open("Images/Buttons/PlayDark.png"),
                size=(40, 40)
            ),
            "previous": ctk.CTkImage(
                dark_image=Image.open("Images/Buttons/PreviousLight.png"),
                light_image=Image.open("Images/Buttons/PreviousDark.png"),
                size=(40, 40)
            ),
            "repeat": ctk.CTkImage(
                dark_image=Image.open("Images/Buttons/RepeatLight.png"),
                light_image=Image.open("Images/Buttons/RepeatDark.png"),
                size=(40, 40)
            ),
            "repeat_selected": ctk.CTkImage(
                dark_image=Image.open("Images/Buttons/RepeatLightSelected.png"),
                light_image=Image.open("Images/Buttons/RepeatDarkSelected.png"),
                size=(40, 40)
            ),
            "shuffle": ctk.CTkImage(
                dark_image=Image.open("Images/Buttons/ShuffleLight.png"),
                light_image=Image.open("Images/Buttons/ShuffleDark.png"),
                size=(40, 40)
            ),
            "volume": ctk.CTkImage(
                dark_image=Image.open("Images/Buttons/VolumeLight.png"),
                light_image=Image.open("Images/Buttons/VolumeDark.png"),
                size=(40, 40)
            )
        }

        self.is_playing = False
        self.paused = False
        self.music_thread = None

        self.__creating_objects()

    def __creating_objects(self):
        """
        Create and configure the buttons and labels for the bottom frame.
        """
        self.album_cover_label = ctk.CTkLabel(
            master=self,
            image=self.album_cover_image,
            text=""
        )

        self.label = ctk.CTkLabel(
            master=self,
            width=30,
            height=30,
            text="Song name\nArtist nickname",
            anchor="e"
        )

        self.previous_button = self.__create_button(self.images.get("previous"))
        self.play_pause_button = self.__create_button(self.images.get("play"))
        self.next_button = self.__create_button(self.images.get("next"))
        self.volume_button = self.__create_button(self.images.get("volume"))
        self.repeat_button = self.__create_button(self.images.get("repeat"))
        self.shuffle_button = self.__create_button(self.images.get("shuffle"))

        self.previous_button.configure(command=...)
        self.play_pause_button.configure(command=self.toggle_play_pause)
        self.next_button.configure(command=...)
        self.volume_button.configure(command=...)
        self.repeat_button.configure(command=...)
        self.shuffle_button.configure(command=...)

        self.album_cover_label.grid(row=0, column=3, padx=(0, 5), pady=(0, 0), sticky="nes")
        self.label.grid(row=0, column=4, padx=(5, 0), pady=(0, 0), sticky="nws")

        self.previous_button.grid(row=0, column=0, pady=(10, 10), sticky="news")
        self.play_pause_button.grid(row=0, column=1, pady=(10, 10), sticky="news")
        self.next_button.grid(row=0, column=2, pady=(10, 10), sticky="news")
        self.volume_button.grid(row=0, column=5, pady=(10, 10), sticky="news")
        self.repeat_button.grid(row=0, column=6, pady=(10, 10), sticky="news")
        self.shuffle_button.grid(row=0, column=7, pady=(10, 10), sticky="news")

    def __create_button(self, image):
        """
        Creates a button with the specified image and command.

        Args:
            image (ctk.CTkImage): The image to be displayed on the button.
            command (callable, optional): The function to be called when the button is clicked.

        Returns:
            ctk.CTkButton: The created button widget.
        """
        button = ctk.CTkButton(
            master=self,
            width=40,
            height=40,
            fg_color="transparent",
            text="",
            hover=False,
            image=image
        )
        return button

    def toggle_play_pause(self):
        """
        Toggle between play and pause states. Changes the button image and command accordingly.
        """
        if self.is_playing:
            # Stop playback
            self.play_pause_button.configure(image=self.images["play"])
            self.is_playing = False
            music_controls.play_pause_music()
        else:
            # Start playback
            self.play_pause_button.configure(image=self.images["pause"])
            self.is_playing = True
            music_controls.play_pause_music()



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

        self.frame_center = CenterFrame(master=self)
        self.frame_center.grid(row=1, column=1, padx=(3, 3), pady=(0, 0), sticky="news")

        self.frame_left = LeftFrame(master=self)
        self.frame_left.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="news")

        self.frame_bottom = BottomFrame(master=self)
        self.frame_bottom.grid(row=2, column=0, columnspan=3, padx=(0, 0), pady=(5, 10), sticky="news")

        self.frame_right = RightFrame(master=self)
        self.frame_right.grid(row=1, column=2, padx=(3, 0), pady=(0, 0), sticky="news")
        file_operations.get_right_frame(self.frame_right)

        self.title_bar_left = TitleBarLeft(master=self)
        self.title_bar_left.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="news")

        self.title_bar_right = TitleBarRight(master=self)
        self.title_bar_right.grid(row=0, column=1, columnspan=2, padx=(0, 0), pady=(0, 0), sticky="news")


if __name__ == "__main__":
    app = MPS()
    ThemeManager.set_dark_theme() if ctk.get_appearance_mode() == "Dark" else ThemeManager.set_light_theme()
    app.mainloop()
