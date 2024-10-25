#!/bin/bash
echo "Running startup commands..."
source /python-facereco/bin/activate
pip install face-recognition numpy dlib picamera2 opencv-python
cd MagicMirror
npm run start
