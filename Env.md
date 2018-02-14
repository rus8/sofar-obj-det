# Environment

Description of environment configuration to run all scripts in this repo.

Everything was set up in standard Ubuntu 16.04 Installation.

## Python

Install pip for Python 3:\
`$ sudo apt install python3-pip`

Install virtual env for Python 3:\
`$ sudo pip3 install virtualenv`

Create virtual environment for the project:\
`$ virtualenv -p python3 /path/to/new/virtual/environment`

Source your new venv in your shell environment:\
`$ source /path/to/new/virtual/environment/bin/activate`

Install NumPy package in your new venv:\
`(venv) $ pip install numpy`

Install pandas package in your new venv:\
`(venv) $ pip install pandas`

Install SciPy package in your new venv:\
`(venv) $ pip install scipy`

Install OpenCV package (unofficial!) in your new venv:\
`(venv) $ pip install opencv-python`

Install Cython for darkflow:\
`(venv) $ pip install cython`

Install TensorFlow for darkflow:\
`(venv) $ pip install tensorflow-gpu==1.0`

## darkflow
Implementation of "darknet"
for YOLO in TensorFlow. 

1) Clone it from GitHub:\
 `(venv) $ git clone https://github.com/thtrieu/darkflow.git`
2) Enter darkflow directory:\
 `(venv) $ cd darkflow`
3) Setup it locally using your new venv:\
 `(venv) $ pip install .`