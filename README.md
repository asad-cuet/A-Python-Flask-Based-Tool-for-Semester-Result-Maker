# A Python-based Tool for Semester Result Maker

This is a Web tools for making student result of a semester using Flask Web Framework. 
It takes grades and grade-points of all student in excel file for every course in a semester. Then one can see a specific student gpa  by putting student id as input

## Setup

1.
Create a folder where you will clone this project

2.
Open cmd in the created folder path and run below command

3.
Clone this project:
```
git clone https://github.com/asad-cuet/A-Python-Flask-Based-Tool-for-Semester-Result-Maker.git
```

4.
```
cd A-Python-Flask-Based-Tool-for-Semester-Result-Maker
```

5.
Install Python if not installed

6.
Install virtual environment and create a environment
```
pip install virtualenv
```
```
python -m venv v_env
```
7.
Activate virtual environment
```
v_env\Scripts\activate
```

8.
Install Flask
```
pip install Flask
```

9.
Install module used in this project
```
pip install pandas
```
```
pip install openpyxl
```

## Run the Server
Run Command
```
flask --debug run
```
Copy the provided link and paste it in the browser. Enjoy the project

## Grade-Sheet Excel File Data Format
In "Some Demo Grade-Sheet Files" Folder some files are given as sample of grade-sheet data.
You can use these files for testing the project.


## How to run the project again later?
You don't need to resetup for later use. Just follow these command

```
v_env\Scripts\activate
```
```
flask --debug run
```

## Some Screenshot

![Screenshot](scrrenshot/demo_1.jpg)

