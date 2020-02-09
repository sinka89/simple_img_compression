## **Simple lightweight image converter**

_`Simple image converter that accepts a variety of image formats (lossless and lossy) and returns .jpeg or .png`_

The converter is based on: 
- python 3.7
- waitress 1.4.3
- flask 1.1.1
- Pillow 7.0.0
- rawpy 0.14.0

Uses rawpy for raw image conversion & Pillow for lossy images, flasgger for Swagger api doc generation.

##### **Swagger documentation available at host/apidocs**

**_Installation and running:_**
- clone source
- create venv in project (python -m venv venv)
- activate venv (win \venv\Scripts\activate.bat | \venv\Scripts\activate)
- pip install -r requirements.txt
- python app.py