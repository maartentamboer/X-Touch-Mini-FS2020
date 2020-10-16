# X-Touch-Mini-FS2020
Control FS2020 with a Behringer X-Touch Mini

![X-TOUCH-MINI_P0B3M_Top_XL](https://user-images.githubusercontent.com/82336/96199071-7e8d7e80-0f4e-11eb-97e7-30d4527aa112.png)

# Configuration
Modify config.json to change assignments

# X-Touch configuration
To use the encoders, the behavior must be set to Relative2 mode.
To help with that I've added my config files that can be programmed to the X-Touch by using the
X-Touch editor software from Behringer.  
Download it from their [Product page](https://www.behringer.com/product.html?modelCode=P0B3M).

![xtouch_editor](https://user-images.githubusercontent.com/82336/96199074-7fbeab80-0f4e-11eb-9bb6-bf8b912a0fb2.png)

# Run

```
start msfs first
python main.py
```

# Installation

Note from @ticktricktrack
I'm not a python coder and I usually work on a Mac, I'll put as many comments in here to be able to follow this with minimal coding knowledge.

- `git`
- `python` [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
- make python and pip available in the windows terminal https://www.geeksforgeeks.org/how-to-set-up-command-prompt-for-python-in-windows10/
- visual c++, installed via build tools installer https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16

```
 # I prefer to use git bash as a terminal over the windows cmd
git clone https://github.com/ticktricktrack/X-Touch-Mini-FS2020.git
cd X-Touch-Mini-FS2020
pip install -r requirements.txt
```
