from tkinter import *
from tkinter import ttk, messagebox


class SettingsScreen(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.pack(fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):


        ttk.Label(
            self,
            text="⚙ Settings",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=20)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=25)



        appearance = ttk.LabelFrame(
            container,
            text="Appearance",
            padding=15
        )
        appearance.pack(fill="x", pady=10)

        ttk.Label(
            appearance,
            text="Theme:"
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.theme = StringVar(value="Light")

        ttk.Radiobutton(
            appearance,
            text="Light",
            variable=self.theme,
            value="Light"
        ).grid(row=0, column=1, padx=10)

        ttk.Radiobutton(
            appearance,
            text="Dark",
            variable=self.theme,
            value="Dark"
        ).grid(row=0, column=2)

        ttk.Radiobutton(
            appearance,
            text="System",
            variable=self.theme,
            value="System"
        ).grid(row=0, column=3)

        ttk.Label(
            appearance,
            text="Primary Color:"
        ).grid(row=1, column=0, sticky="w", pady=10)

        self.color = ttk.Combobox(
            appearance,
            state="readonly",
            values=[
                "Blue",
                "Green",
                "Purple",
                "Orange",
                "Red",
                "Gray"
            ]
        )

        self.color.current(0)
        self.color.grid(row=1, column=1, columnspan=2, sticky="w")

        ttk.Label(
            appearance,
            text="Font Size:"
        ).grid(row=2, column=0, sticky="w", pady=10)

        self.font = ttk.Combobox(
            appearance,
            state="readonly",
            values=[
                "Small",
                "Medium",
                "Large"
            ]
        )

        self.font.current(1)
        self.font.grid(row=2, column=1, sticky="w")

        self.animations = BooleanVar(value=True)

        ttk.Checkbutton(
            appearance,
            text="Enable animations",
            variable=self.animations
        ).grid(row=3, column=0, columnspan=3, sticky="w", pady=5)

        self.tooltips = BooleanVar(value=True)

        ttk.Checkbutton(
            appearance,
            text="Show tooltips",
            variable=self.tooltips
        ).grid(row=4, column=0, columnspan=3, sticky="w")



        interface = ttk.LabelFrame(
            container,
            text="Interface",
            padding=15
        )

        interface.pack(fill="x", pady=10)

        self.maximized = BooleanVar(value=True)
        self.remember = BooleanVar(value=True)
        self.confirm = BooleanVar(value=True)
        self.splash = BooleanVar(value=False)

        ttk.Checkbutton(
            interface,
            text="Start maximized",
            variable=self.maximized
        ).pack(anchor="w")

        ttk.Checkbutton(
            interface,
            text="Remember window size",
            variable=self.remember
        ).pack(anchor="w")

        ttk.Checkbutton(
            interface,
            text="Confirm before exiting",
            variable=self.confirm
        ).pack(anchor="w")

        ttk.Checkbutton(
            interface,
            text="Show splash screen",
            variable=self.splash
        ).pack(anchor="w")



        language = ttk.LabelFrame(
            container,
            text="Language",
            padding=15
        )

        language.pack(fill="x", pady=10)

        ttk.Label(
            language,
            text="Language:"
        ).grid(row=0, column=0)

        self.language = ttk.Combobox(
            language,
            state="readonly",
            values=[
                "English",
                "Português"
            ]
        )

        self.language.current(0)
        self.language.grid(row=0, column=1, padx=15)


        about = ttk.LabelFrame(
            container,
            text="About",
            padding=15
        )

        about.pack(fill="x", pady=10)

        ttk.Label(
            about,
            text="Network Monitor",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        ttk.Label(
            about,
            text="Version 1.0.0"
        ).pack(anchor="w")

        ttk.Label(
            about,
            text="Developed by Giovanni Milan"
        ).pack(anchor="w")


        buttons = ttk.Frame(self)
        buttons.pack(pady=25)

        ttk.Button(
            buttons,
            text="Save",
            width=15,
            command=self.save
        ).pack(side="left", padx=10)

        ttk.Button(
            buttons,
            text="Restore Defaults",
            width=18,
            command=self.restore
        ).pack(side="left", padx=10)

        ttk.Button(
            buttons,
            text="Back",
            width=15,
            command=self.back
        ).pack(side="left", padx=10)



    def save(self):

        messagebox.showinfo(
            "Settings",
            "Settings saved successfully!"
        )

    def restore(self):

        self.theme.set("Light")
        self.color.current(0)
        self.font.current(1)

        self.animations.set(True)
        self.tooltips.set(True)

        self.maximized.set(True)
        self.remember.set(True)
        self.confirm.set(True)
        self.splash.set(False)

        self.language.current(0)

    def back(self):

        from .control_panel import Control_panel

        self.destroy()
        Control_panel(self.master)
