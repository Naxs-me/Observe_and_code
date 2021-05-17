# Observe and Code

## What is Observe and Code?
1. Observe and code is a web application, that allows user to learn and practice programming and algorithms.
2. It not only provides question like hackerrank and codechef, it also provides some hints in form of intermidiate steps of the code to the user.

## Features of Observe and code:
1. Observe and code dynamically extracts dynamic information such as inputs, outputs, comments (if present in the snippet) alongwith changes in variable values during runtime. 
2. Presents hints to the user like when to start and end loops, how the value of variable changes as the loop is executed etc.
3. Pinpoints the location of error in the logic of the user.

## Working of Observe and code:
Observe and code is developed as a web application using the following approach:

<img alt="approach" src="https://user-images.githubusercontent.com/35232831/118478750-dd59e700-b72d-11eb-9bc9-fa404c5d86e7.png">

Step 1 - The user selects the question that they want to practice from the webpage. \
Step 2 - The structure for the IPython notebook is generated using static analysis of the abstract syntax tree of the code. The abstract syntax tree is created and analysed using the ast library of python
Step 3 - ast.parse() processes all the token and by following the rules of python, generates a tree which represents the whole code.
Step 4 - ast.NodeVisitor() is used to visit and analyse all the nodes of the tree in theorder of its execution. 
Step 5 - Using ast.NodeVisitor() different types of statements are identifed like, function delaration, if, else, for and so on along with their indentation. This information is used to generate a structure for the IPython notebook.
Step 6 - OAC then extracts the dynamic information instances by executing the codeusing a process similar toCOSPEX. The dynamic information instances are then filled within the generated IPython notebook. The incomplete IPython notebook is presented to the user.
Step 7 - User then inputs the solution of the problem.
Step 8 - Upon execution of the IPython notebook the the dynamic information instances are used to extract any error in the code.

## Steps to install and run Observe and code (for windows):
1. Download and extract the repository on your local machine.
2. Open the repository in Powershell  
3. Run the commands: $env:FLASK_APP = "flaskr", $env:FLASK_ENV = "development" and flask run
4. The OAC will run on http://127.0.0.1:5000/

## Steps to use Observe and code:
1. Select the question the you want to practice.
2. Type the command to run python on your machine in text box.
3. Press select.
4. A zip file will be downloaded which contains the IPython notebook in which you can practice.
5. After filling the IPython notebook execute the execute.py file to find the errors in the logic.

## How to contribute to Observe and code:
We will be very happy to receive any kind of contributions. Incase of a bug or an enhancement idea or a feature improvement idea, please open an issue or a pull request. Incase of any queries or if you would like to give any suggestions, please feel free to contact Nakshatra Gupta (cs17b020@iittp.ac.in), Ashutosh Rajput (cs17b007@iittp.ac.in) or Sridhar Chimalakonda (ch@iittp.ac.in) of RISHA Lab, IIT Tirupati, India.
