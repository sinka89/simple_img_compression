## **Simple lightweight image converter**

_`Simple image converter that accepts a variety of image formats (lossless and lossy) and returns .jpeg, .png, .webp, or .jp2`_

_Supported raw types: '.dng', '.raw', '.cr2', '.crw', '.erf', '.raf', '.tif', '.kdc', '.dcr', '.mos',
                                  '.mef', '.nef', '.orf', '.rw2', '.pef', '.x3f', '.srw', '.srf', '.sr2', '.arw',
                                  '.mdc',
                                  '.mrw'._

The converter is based on: 
- python 3.7
- waitress 1.4.3
- flask 1.1.1
- Pillow 7.0.0
- rawpy 0.14.0

Uses rawpy for raw image conversion & Pillow for lossy images, flasgger for Swagger api doc generation.

##### **Swagger documentation available at host/apidocs**

**_Installation and running:_**
1. clone source
2. create venv in project (python -m venv venv)
3. activate venv (win \venv\Scripts\activate.bat | \venv\Scripts\activate)
4. pip install -r requirements.txt
5. python app.py

For deploying in linux env past microconvert.service into /etc/systemd/system &
run sudo systemctl daemon-reload &
sudo systemctl start microconvert.service

*Note: The ExecStart from microconvert.service must match the location of the project, and it must have a python virtual environment created (see step 2)