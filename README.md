<h2>Stained Glass Recognizer API</h2>

<h3>Context</h3>

<p>The code in this repository was developed in a six months project as part of a course 
(Pôle Project) of CentraleSupélec (University Paris-Saclay). I was a member in a group of 
four students and we should develop an Android application capable to recognize 
Stained Glass from churches.</p>

<p>The source code that you find here is the API where images were processed and compared 
agains a database of around 1800 images. The techniques used were:</p>

<ul>
    <li>Histogram of Oriented Gradients (HOG features) as pre-processing algorithm</li>
    <li>K Nearest Neighbors (KNN) as the classification algorithm</li>
</ul>

<p>The API is composed of a unique endpoint (/classify), which receives an image file and 
outputs information of the picture in the database the most similar to it.</p>

<p>The server was originally written in PHP and a Python script was called to perform 
the classification. I recently translated it into a Flask API because it seems more 
logical to have the entire application in a unique programming language.</p>

<h3>Installing the project</h3>

<p>Installing the project is simple. Follow the steps below:</p>

<ul>
    <li>Download the source code.</li>
    <li>
        Make sure you have Python (Python 3.10 is recommended) and
pip (Packager Installer for Python) in your computer.
    </li>
    <li>In the root of the project, run the command "pip install -r requirements.txt".
It will install the dependencies of the project.</li>
    <li>To launch the API, execute the file "app.py" <strong>or</strong> run the command 
"flask run --host=0.0.0.0".</li>
</ul>