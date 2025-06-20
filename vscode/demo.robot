*** Settings ***
Library  SeleniumLibrary
Test Setup  Open Browser   http://localhost:3000/admin


*** Keywords ***
login sucess
    Input Text    name=email    admin@mail.fr
    Input Text    name=password    password1
    Click Button    css:.button.primary

*** Test Cases ***
login sucess

Create Cat
    Go To    http://localhost:3000/admin