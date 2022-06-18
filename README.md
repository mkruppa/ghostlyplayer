# ghostlyplayer

A minimal browser to natively play videos from the World Wide Web (e.g. from YouTube).


# Install

1. Install the latest versions of python, pip, qt6 and mpv using your package manager. For Arch-based Linux distributions execute the following command in a shell:

```
sudo pacman -Sy python python-pip qt6 mpv
```

2. Install the required python packages for the project without root privileges:

```
pip install -U PyQt6 requests
```

3. Compile the Python UI:

```
pyuic6 --indent 0 --output src/ui/MainWindow.py src/ui/MainWindow.ui
```

# Run

After installing the project dependencies and compiling the UI the application can be run with:

```
python src/main.py
```

Then, here is how to watch a YouTube video:

1. Enter a search term into the line edit at the top and hit Enter.
2. Optionally, press the "More" button on the bottom to search for more results.
3. Find a video you want to watch and double click on it. This should play the video in an instance of mpv after a few seconds.