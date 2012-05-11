# JavaScript Hacking

This application is currently deployed at: http://jshacking.heroku.com/

## Introduction
This is a skill test for finding vulnerabilities in JavaScript aimed at the beginner to intermediate level. The user will be taken through a series of pages containing nothing but a form asking for a password to advance to the next level; however, the passwords are verified via JavaScript, which any web developer can tell you is a very bad idea. The passwords start to get hidden better as the test goes on, but as with any JavaScript security system, they can always be bypassed.

## Secret Key
The file app.py uses a secret key to control the session cookies that stop the user from advancing themselves just by knowing what the next URL is. This key is read from a file named key.pvt; this key is excluded from the source code on GitHub because it is in use on the actual deployed application.

To generate your own key, I have included a Python script that will generate a random and secure key.pvt file. If you choose to clone this repository and would like the application to run, simply run generate\_secret\_key.py and you will have a working application. Be careful with the new key.pvt file; make sure that you do not push it to GitHub especially if you have deployed the application elsewhere, and do not push your own key.pvt file and then submit a pull request.
