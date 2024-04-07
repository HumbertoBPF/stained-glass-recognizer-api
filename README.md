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

<p>Training data and database images were omitted from this repository to avoid 
intellectual property issues.</p>

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

<p><strong>Remark:</strong> if you try to call the API, it will fail due to the missing 
training data and database images. To address that, you can feed the model with your own 
training data as described in the next section.</p>

<h3>Using your own data</h3>

To work properly, the project needs to have <strong>reference data</strong> and 
<strong>training data</strong>. 

<ul>
    <li>
    <strong>Reference data</strong> corresponds to the pictures used to train 
the machine learning model and complementary information about them (artist, glass data, 
church where the stained-glass is, etc.). 
    </li>
    <li>
    <strong>Training data</strong> refers to pre-computed HOG features to be used in the training phase 
of the KNN model. They are stored as shelve files.
    </li>
</ul>

<p>To use your own data, follow these steps:</p>

<ul>
    <li>Create a "db_data" folder in the root of your project.</li>
    <li>
        Inside this folder, create an "images" sub-folder with the stained-glass images you 
want to use to train the machine learning model.
    </li>
    <li>
        Run the "create_reference_and_training_data.py" script.
    </li>
</ul>

<p>At the end, you will have an "info_images.csv" file in the "db_data" folder and the 
pre-computed HOG features a "training_data" folder. Notice that the info_images.csv file 
has only the "filename" column with data. It's up to you to complete the other columns 
with information specific to the pictures you use (however, you don't need to do it in 
order to make the API work).</p>
