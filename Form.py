import customtkinter as ctk
from tkinter import Menu, filedialog
import webbrowser
from PIL import Image


class LogoButton(ctk.CTkButton):
    IS_PRESSED = False

    def __init__(self, master, menu):
        super().__init__(master=master,
                         width=50,
                         height=20,
                         image=ctk.CTkImage(light_image=Image.open("New folder/WhiteLogo.png"), size=(75, 20)),
                         fg_color="transparent",
                         text="",
                         hover_color="#888888"
                         )
        self.menu = menu
        self.configure(command=self.show_menu)

    def show_menu(self):
        if self.IS_PRESSED is False:
            self.menu.post(self.winfo_rootx(), self.winfo_rooty() + self.winfo_height())
            self.IS_PRESSED = True
        else:
            self.menu.unpost()
            self.IS_PRESSED = False


class LogoMenu(Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=0)
        self.add_command(label="About", command=self.open_github)
        self.add_command(label="Settings", command=self.open_settings)
        self.add_separator()

        self.add_command(label="Open Files", command=self.adding_files)
        self.add_command(label="Open Folder", command=self.adding_folder)
        self.add_separator()

        self.add_command(label="Exit", command=master.quit)

    @staticmethod
    def open_github():
        webbrowser.open("https://github.com")

    @staticmethod
    def open_settings(self):
        pass

    @staticmethod
    def adding_files():
        filedialog.askopenfilenames(title="Open")

    @staticmethod
    def adding_folder():
        filedialog.askdirectory(title="Select Folder")


class SettingsWindow(ctk.CTk):
    def __init__(self, master):
        super().__init__(master)
        self.title("Settings")
        self.geometry("300x200")
        # TODO setting window


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MPS")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.logo_menu = LogoMenu(self)
        self.app_name_button = LogoButton(master=self, menu=self.logo_menu)
        self.app_name_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.mainloop()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
