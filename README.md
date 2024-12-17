# UT Automatic Course Adder
Based off https://github.com/christiandipert/UT-Course-Availability-Tracker

A script that runs in the background until a class opens up and automatically tries to add the class to your schedule. If there is a waitlist for the class, it will join the waitlist and set the swap class that you provide. You can also drop upon successful add if you need to replace a class.

# How to Use
Download and run the Python file using the command line or an IDE. The script will open a window that asks for whether you want to only add a class or drop upon successful add. Then, it will ask you for the Unique numbers of the classes you want to add, drop, or swap, the season and year you are registering for, and whether you want the Chrome tab to be minimized or not. After this, you will need to login with your UTEID and authenticate with Duo. Finally, the script will automatically refresh until the class is open and open up your registration page to add the classes and join the waitlist if needed. Make sure to check whether the courses were actually added by looking at your registration page and also looking at the terminal.

# Running the program:

Install the libraries required for the script:
```python
pip install selenium
```

To run the script, type this into your terminal or run it from an IDE with:
```python
python courseTrack.py
```
or
```python
python3 courseTrack.py
```


