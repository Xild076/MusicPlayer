import cx_Freeze


buildOptions = dict(include_files = ['UDMusicPlayer/allmusic/'])


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
    options=dict(build_exe = buildOptions),
    executables=executables
)
