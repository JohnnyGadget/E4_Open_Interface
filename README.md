## E4 OPEN Interface


## 🌟 Highlights

- Editing Preset parameters on the Emu E4 Sampler made easy!


## ℹ️ Overview

This software is an interface for Emu EOS on the Emu E4 Sampler. Written in Python so it could be easy to modify and update for just about anyone with an idea to do so. MIT LiCENSED :D


All are Encouraged to modify it as they see fit and make Commit requests to the primary project. If the commit makes sense it will be accepted.

Install pyinstaller by opening the terminal and running the command pip install pyinstaller.
Navigate to the directory where your Python script is located using the 'cd' command.
Run the command pyinstaller --onefile your_script_name.py to compile your Python script into an executable file. Replace 'your_script_name.py' with the name of your Python script.
Once the process is complete, you will find the generated executable file in the 'dist' directory.

### ✍️ Authors

JohnnyGadget

[![License: MIT](https://cdn.prod.website-files.com/5e0f1144930a8bc8aace526c/65dd9eb5aaca434fac4f1c34_License-MIT-blue.svg)](/LICENSE)


## 🚀 Usage

To Be Updated!


## ⬇️ Installation

Simple, understandable installation instructions!

```bash
pip install e4_open_interface
```

* Dependencies *
```bash
pip install wxPython
```

```bash
pip install mido[ports-rtmidi]
```

* Build Command *
...bash
pyinstaller --onefile --hidden-import=mido.backends.rtmidi main.py

...


And be sure to specify any other minimum requirements like Python versions or operating systems.

*You may be inclined to add development instructions here, don't.*


## 💭 Feedback and Contributing

Add a link to the Discussions tab in your repo and invite users to open issues for bugs/feature requests.

This is also a great place to invite others to contribute in any ways that make sense for your project. Point people to your DEVELOPMENT and/or CONTRIBUTING guides if you have them.
