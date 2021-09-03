# Description

A simple script for scarping latest emails using **BeautifulSoup** python library. This script only works for stm.eng.ruh.ac.lk


# How to use?

Just needs only credentials.

## Install Requirements

- Clone this repo:
```
git clone https://github.com/xlastfire/stm_updates/
cd mirrorbot
```

- Install requirements 
```
pip install beautifulsoup4
```
## Set Credentials

In credenttials.py file, set your user name and password.
- Username should be like **someone_abcde_e21** format.


## Execute/Run

In your terminam or command promt
- goto the code directory
```
cd path/to/the/folder
```
- run grab.py file
```
python grab.py
```
The output will be saved in the same directory as _emails.txt_

## Additional

### Printing in the command prompt or in the terminal
If you need to see each email overview in the command prompt or terminal,   set the to_console value to the True

- In line 59
```
to_console = True
```

### Easy running
You can create a bat file for easy running the script. Follow this.

- First, do the stuffs mentioned in **Printing in the command prompt or in the terminal**

- Create a file in the desktop like,
```
any_name.bat
```

- Right click and go edit. Then add this. Write the folder path correctly.
```
python path\to\the\folder\grab.py
```

Now you can easily see the results in your console by running bat file.














