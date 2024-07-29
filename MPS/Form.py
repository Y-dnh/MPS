import customtkinter as ctk
from tkinter import Menu, filedialog
import webbrowser
from PIL import Image


# images = {
#             "next": ctk.CTkImage(dark_image=Image.open("Images/Buttons/NextDark.png"),
#                                  light_image=Image.open("Images/Buttons/NextLight.png")),
#             "pause": ctk.CTkImage(dark_image=Image.open("Images/Buttons/PauseDark.png"),
#                                   light_image=Image.open("Images/Buttons/PauseLight.png")),
#             "play": ctk.CTkImage(dark_image=Image.open("Images/Buttons/PlayDark.png"),
#                                  light_image=Image.open("Images/Buttons/PlayLight.png")),
#             "previous": ctk.CTkImage(dark_image=Image.open("Images/Buttons/PreviousDark.png"),
#                                      light_image=Image.open("Images/Buttons/PreviousLight.png")),
#             "repeat": ctk.CTkImage(dark_image=Image.open("Images/Buttons/RepeatDark.png"),
#                                    light_image=Image.open("Images/Buttons/RepeatLight.png")),
#             "repeat_selected": ctk.CTkImage(dark_image=Image.open("Images/Buttons/RepeatDarkSelected.png"),
#                                             light_image=Image.open("Images/Buttons/RepeatLightSelected.png")),
#             "shuffle": ctk.CTkImage(dark_image=Image.open("Images/Buttons/ShuffleDark.png"),
#                                     light_image=Image.open("Images/Buttons/ShuffleLight.png")),
#             "vinyl_disk": ctk.CTkImage(dark_image=Image.open("Images/Buttons/VinylDiskDark.png"),
#                                        light_image=Image.open("Images/Buttons/VinylDiskLight.png")),
#             "volume": ctk.CTkImage(dark_image=Image.open("Images/Buttons/VolumeDark.png"),
#                                    light_image=Image.open("Images/Buttons/VolumeLight.png"))
#         }

class LeftFrame(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        super().__init__(master=self.master)

        self.vinyl_disk_image = ctk.CTkImage(dark_image=Image.open("Images/Buttons/VinylDiskDark.png"),
                                             light_image=Image.open("Images/Buttons/VinylDiskLight.png"))
        self.logo_button_image = ctk.CTkImage(dark_image=Image.open("Images/Logo/DarkLogo.png"),
                                              light_image=Image.open("Images/Logo/WhiteLogo.png"),
                                              size=(75, 25))

        self.hover_logo_button_image = {"Light": ctk.CTkImage(Image.open("Images/Logo/WhiteLogoHover.png"), size=(75, 25)),
                                        "Dark": ctk.CTkImage(Image.open("Images/Logo/DarkLogoHover.png"), size=(75, 25))}


        self.logo_button = ctk.CTkButton(master=self.master,
                                         width=75,
                                         height=25,
                                         fg_color="transparent",
                                         text="",
                                         command=lambda: self.logo_menu.post(x=self.master.winfo_rootx(),
                                                                             y=self.master.winfo_rooty() + self.logo_button.winfo_height()),
                                         hover=False,
                                         image=self.logo_button_image
                                         )

        self.logo_button.grid(row=0, column=0)

        self.logo_button.bind("<Enter>", lambda event: self.logo_button.configure(image=self.hover_logo_button_image.get(ctk.get_appearance_mode())))
        self.logo_button.bind("<Leave>", lambda event: self.logo_button.configure(image=self.logo_button_image))

        self.logo_menu = Menu(master=self.master, tearoff=0)

        self.logo_menu.add_command(label="About", command=lambda: webbrowser.open("https://github.com"))
        self.logo_menu.add_separator()

        self.logo_menu.add_command(label="Open Files", command=lambda: filedialog.askopenfilenames(title="Open"))
        self.logo_menu.add_command(label="Open Folder", command=lambda: filedialog.askdirectory(title="Open"))
        self.logo_menu.add_separator()

        self.appearance_menu = Menu(self, tearoff=0)
        self.appearance_menu.add_radiobutton(label="Light", command=lambda: ctk.set_appearance_mode("Light"))
        self.appearance_menu.add_radiobutton(label="Dark", command=lambda: ctk.set_appearance_mode("Dark"))
        self.logo_menu.add_cascade(label="Theme", menu=self.appearance_menu)

        self.logo_menu.add_command(label="Clear Downloads", command=...)
        self.logo_menu.add_command(label="Storage Location", command=...)
        self.logo_menu.add_separator()

        self.logo_menu.add_command(label="Exit", command=master.quit)





class MPS(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MPS")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.grid_rowconfigure(0, minsize=525, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, minsize=250, weight=1)
        self.grid_columnconfigure(1, minsize=300, weight=1)
        self.grid_columnconfigure(2, minsize=350, weight=1)

        self.frame_left = ctk.CTkFrame(self)
        self.frame_center = ctk.CTkFrame(self)
        self.frame_right = ctk.CTkFrame(self)
        self.frame_bottom = ctk.CTkFrame(self)
        self.frame_left.grid(row=0, column=0, padx=(10, 3), pady=(10, 0), sticky="nswe")
        self.frame_center.grid(row=0, column=1, padx=(3, 3), pady=(10, 0), sticky="nswe")
        self.frame_right.grid(row=0, column=2, padx=(3, 10), pady=(10, 0), sticky="nswe")
        self.frame_bottom.grid(row=1, column=0, columnspan=3, padx=(10, 10), pady=(5, 10), sticky="nswe")

        LeftFrame(master=self.frame_left)


if __name__ == "__main__":
    app = MPS()
    app.mainloop()
