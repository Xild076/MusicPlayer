import cx_Freeze


buildOptions = dict(include_files = ['allmusic/'])


executables = [
    cx_Freeze.Executable(
        "playlamusica.py",
        base="Win32GUI",  # Use "Win32GUI" to create a GUI application
        icon='icon.ico'
    )
]

cx_Freeze.setup(
    name="UD Musica Player",
    version="12.131417823",
    description="epic musiccccccccc hehehheheh yayayayayayayayaay :) :D :|",
    options=dict(build_exe = buildOptions),
    executables=executables
)
