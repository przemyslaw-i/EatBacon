#!/usr/bin/env python

"""
GUI helpers for Eat Bacon
"""

__author__ = "Przemyslaw I."
__copyright__ = "Copyright 2022, Przemyslaw I."
__license__ = "MIT"
__version__ = "0.1.0"

from tkinter import Tk, ttk, Label, Button, Entry, END, messagebox

def label(parent, position, text, font=12):
    """
    Creates Label object.
    """
    lbl = Label(parent, text=text, font=font)
    lbl.grid(column=position[0], row=position[1])
    return lbl

def button(parent, position, text, action=None, width=10):
    """
    Creates Button object.
    """
    btn = Button(parent, text=text, width=width)
    btn.grid(column=position[0], row=position[1])
    if action:
        btn.config(command=action)
    return btn

def entry(parent, position, width, font=12, text=None):
    """
    Creates Entry (one line input) object.
    """
    fld = Entry(parent, font=font, width=width)
    fld.grid(column=position[0], row=position[1])
    if text:
        fld.insert(END, '2')
    return fld

def window(title="Eat Bacon", padding=10, resizable=(False, False)):
    """
    Creates window and gid frame for it.
    """
    # Window
    win = Tk()
    win.title(title)
    win.resizable(resizable[0], resizable[1])

    # Frame
    frm = ttk.Frame(win, padding=padding)
    frm.grid()

    # Return objects
    return (win, frm)

def question_box(title, message, yes_func=None, no_func=None):
    """
    Asks question and executes function depending on the answer
    """
    msg = messagebox.askquestion(title, message, icon='question')
    if msg == 'yes':
        if yes_func:
            yes_func()
    else:
        if no_func:
            no_func()
