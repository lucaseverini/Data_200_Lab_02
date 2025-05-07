#!/usr/bin/env python3

# Lab2 (May-6-2025)
# Class: DATA 200-22
# Instructor: Paramdeep Saini paramdeep.saini@sjsu.edu
# Student: Luca Severini 008879273 luca.severini@sjsu.edu

# This module is just a shorter name for the program that can start either the Console or GUI version of the program.

import stock_console
# import stock_GUI

def main():
    # For Console Version
    print("Lab 2 program - Luca Severini - 008879723")
    
    stock_console.main()

    # For GUI Version
    # stock_GUI.main()

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a script
    main()