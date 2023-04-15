# Read Me #

## Installation ##

To make sure you have all the required files:
1. Install python
2. Enter `pip install -r requirements` into Command Prompt.
      Do this in your environment folder as well if you plan to use one.

## Running the server ##

To run the server, while in the project folder (capstone):

Device | Command
------------- | -------------
Windows | `py manage.py runserver`
Mac | `python manage.py runserver`

It will say ctrl+break to close, but ctrl+c also works. I believe ctrl is replaced with command for Mac

## Virtual Environment ##

If you perhaps are unable to run the server, consider making an virtual environment(venv for short)
1. Install venv using `pip install venv` in Command Prompt
2. Ensure your PATH includes the path to your Scripts file in the venv you create
3. Activate your venv by typing in the relative path to activate file in Scripts
    For example: ".\(venv name\)\Scripts\activate" if you are in the project folder
    "." means this folder
  You might need to make a python virtual environment in a new folder within the project


### Extra ###
For a quick tutorial on making a Django website, click on the following link:
https://www.youtube.com/watch?v=jCDZSVHA0-Y&t=185
We used multiple videos in its accompanying playlist
