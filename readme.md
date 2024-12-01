# OptiNutrition
Optinutrition is an app that helps you find ideal recipes based on your nutrition goals and what you have in your fridge. 


###### The app development was done on MacOS Sonoma 14.6.1 using Python 3.13.0

## Introduction

Optinutrition is designed to assist international students in creating practical, healthy meals tailored to their available ingredients and dietary objectives. 

## Features

- **Login System**: Login with validation for email and password.
- **Macro Calculation**:
  - Automatically calculate macros based on user height, weight, age, gender, and exercise intensity.
  - Manually input macros (protein, fat, carbs, and calories).
- **Fridge Management**:
  - **Manual Entry**: Type fridge item names manually
  - **Image Recognition**: Upload a picture of your fridge, and the app detects ingredients.
- **Recipe Finder**:
  - Match recipes based on user calories, macros, and ingredient availability.
  - Shows missing ingredients and quantities needed for selected recipes.
- **Recipe Instructions**:
  - Display step-by-step cooking instructions for chosen recipes.


## Running The Code
In order to run the code you will need:
  - Python 
  - Library - To run our program, you will need the following libraries: request ...
        To download the required library type the following command   
    ```pip install -r requirements.txt ``` 

## About The Code

The following structures and algortithms were used:

A Hash Table was use to store each recipe and hold information such as ingredients, macros and instructions. It was also used to store the adress and coordinates for each supermarket.

The quick sort algorithm was used to sort recipes based on their calculated scores.


## Credits
Osama Abdelhak  
Khaled El Hamawi   
Mohamed Yacine Bakkoury   
Thanh An Tran   
Adriana Tarazona  
Ziad Tharwat
