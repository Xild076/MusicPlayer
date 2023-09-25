import cx_Freeze

exec_options = {
    "packages": [],
}

executables = [
    cx_Freeze.Executable(
        "C:/Users/harry/PycharmProjects/UDMusicPlayer/playlamusica.py",
        base="Win32GUI",  # Use "Win32GUI" to create a GUI application
    )
]

cx_Freeze.setup(
    name="UD Musica Player",
    version="1.4",
    description="epic musiccccccccc hehehheheh yayayayayayayayaay :) :D :|",
    options={"build_exe": exec_options},
    executables=executables
)
