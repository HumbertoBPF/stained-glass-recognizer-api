<h2>Stained Glass Recognizer API</h2>

<h3>Context</h3>

<p>The code in this repository was developed in a six-month project as part of a course 
(Pôle Project) of CentraleSupélec (University Paris-Saclay). I was a member of a group of 
four students and we developed an Android application capable of recognizing 
Stained Glass from churches.</p>

<p>The source code you find here is the API where images were processed and compared 
against a database of around 1800 images. The techniques used were:</p>

<ul>
    <li>Histogram of Oriented Gradients (HOG features) as pre-processing algorithm</li>
    <li>K Nearest Neighbors (KNN) as the classification algorithm</li>
</ul>

<p>Training data and database images were omitted from this repository to avoid 
intellectual property issues.</p>

<p>The API has a unique endpoint (/classify), which receives an image file and 
outputs information about the picture in the database the most similar to it.</p>

<p>The server was originally written in PHP and a Python script was called to perform 
the classification. I recently translated it into a Flask API because it seems more 
logical to have the entire application in a unique programming language.</p>

<h3>Installing the project</h3>

<p>Installing the project is simple. Follow the steps below:</p>

<ul>
    <li>Download the source code.</li>
    <li>
        Make sure you have Python (Python 3.10 is recommended) and
pip (Packager Installer for Python) on your computer.
    </li>
    <li>In the root of the project, run the command "pip install -r requirements.txt".
It will install the dependencies of the project.</li>
    <li>To launch the API, execute the file "app.py" <strong>or</strong> run the command 
"flask run --host=0.0.0.0".</li>
</ul>

<p><strong>Remark:</strong> if you try to call the API, it will fail due to the missing 
training data and database images. To address that, you can feed the model with your 
training data as described in the next section.</p>

<h3>Using your data</h3>

The project needs to have <strong>reference data</strong> and 
<strong>training data</strong> to work properly. 

<ul>
    <li>
    <strong>Reference data</strong> corresponds to the pictures used to train 
the machine learning model and complementary information about them (artist, glass data, 
church where the stained glass is, etc.). 
    </li>
    <li>
    <strong>Training data</strong> refers to pre-computed HOG features to be used in the training phase 
of the KNN model. They are stored as shelve files.
    </li>
</ul>

<p>To use your data, follow these steps:</p>

<ul>
    <li>Create a "db_data" and a "training_data" folder at the root of your project.</li>
    <li>
        Inside the "db_data" folder, create an "images" sub-folder with the stained-glass 
images you want to use to train the machine learning model.
    </li>
    <li>
        Run the "create_reference_and_training_data.py" script.
    </li>
</ul>

<p>In the end, you will have an "info_images.csv" file in the "db_data" folder and the 
pre-computed HOG features a "training_data" folder. Notice that the info_images.csv file 
has only the "filename" column with data. It's up to you to complete the other columns 
with information specific to the pictures you use (however, you don't need to do it to 
make the API work).</p>

<h3>Deployment</h3>

<p>I have designed a way do deploy this project on AWS. That also concerns changes on the 
data layer. <strong>These modifications can be found on the Git branch aws</strong>. 
The deployment process concerns:</p>

<ul>
    <li>The deployment process is done using AWS Elastic Beanstalk.</li>
    <li>Instead of storing images on a folder in the project, AWS S3 was used.</li>
    <li>
        Instead of storing image related data in a CSV file in the project structure, AWS
        DynamoDB was used.
    </li>
</ul>

<p>I advise you to proceed with the deployment process described here only if you are 
familiar with AWS, otherwise you will not understand the employed vocabulary.</p>

<p>I used the default Elastic Beanstalk environment settings, except for the number of
instances of the Auto Scaling Group, which ranges from 1 to 2 instances according to 
the load. Besides, the health check is performed using a new endpoint "/health". The 
instances are considered healthy when this endpoint returns a 204 status code.</p>

<p>To deploy the project on your AWS account, you'll need to install the AWS CLI and 
configure it on your computer. This is a very standard process when using AWS, and you
can follow <a target="_blank" href="https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html">the AWS official guide</a>.
After the installation, you will need to store your AWS credentials to be able to 
access your AWS account from the CLI. You can find ways to do so <a target="_blank" href="https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html">on the AWS docs</a>.</p>

<p>Then, you will need to install the EB CLI (Elastic Beanstalk
CLI), which is a way to automate Elastic Beanstalk deployments. I followed 
<a target="_blank" href="https://github.com/aws/aws-elastic-beanstalk-cli-setup">the guide available on the official AWS Git Repository</a>.</p>

<p>Switch to the Git branch <strong>aws</strong>, and tun the script 
<strong>send_data_to_aws.py</strong> to send image related data to AWS DynamoDB. 
DynamoDB is a serverless NoSQL database from AWS, which will be used by the Flask 
application as data source. In addition, upload the image folder to AWS S3 on the 
AWS console. S3 is a storage service for files in general.</p>

<p>Finally, you must run some EB CLI commands to create an Elastic Beanstalk application, 
set up a deployment environment, and deploy the project:</p>

<ul>
    <li>
        Run <strong>eb init</strong> to create an Elastic Beanstalk application. You will
        be prompted to provide some configuration information. The unique question that actually
        matters is the application platform, which should be Python.
    </li>
    <li>
        Run <strong>eb create -ip {role_name}</strong> to create a deployment environment.
        <strong>role_name</strong> should be replaced with the name of an AWS role that you 
        need to grant to your EC2 instances to let they make requests to other AWS services 
        (S3 and DynamoDB). This role should be attached to the following AWS managed policies: 
        AmazonDynamoDBReadOnlyAccess, AmazonS3ReadOnlyAccess, AWSElasticBeanstalkMulticontainerDocker, 
        AWSElasticBeanstalkWebTier, AWSElasticBeanstalkWorkerTier.
    </li>
    <li>
        Run <strong>eb deploy --staged</strong> to deploy your project. 
    </li>
</ul>

<p>Keep in mind that there are AWS costs associated with the Elastic Beanstalk deployment.
So if you are done with it, run the command <strong>eb terminate {environment-name}</strong>
to terminate the deployment environment.</p>
