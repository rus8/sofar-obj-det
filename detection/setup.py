from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy
import os

VERSION = "1.0.0"

if os.name =='nt' :
    ext_modules=[
        Extension("objdet.cython_utils.nms",
            sources=["objdet/cython_utils/nms.pyx"],
            #libraries=["m"] # Unix-like specific
            include_dirs=[numpy.get_include(), "."]
        ),        
        Extension("objdet.cython_utils.cy_yolo2_findboxes",
            sources=["objdet/cython_utils/cy_yolo2_findboxes.pyx"],
            #libraries=["m"] # Unix-like specific
            include_dirs=[numpy.get_include(), "."]
        ),
        Extension("objdet.cython_utils.cy_yolo_findboxes",
            sources=["objdet/cython_utils/cy_yolo_findboxes.pyx"],
            #libraries=["m"] # Unix-like specific
            include_dirs=[numpy.get_include(), "."]
        )
    ]

elif os.name =='posix' :
    ext_modules=[
        Extension("objdet.cython_utils.nms",
            sources=["objdet/cython_utils/nms.pyx"],
            libraries=["m"], # Unix-like specific
            include_dirs=[numpy.get_include(), "."]
        ),        
        Extension("objdet.cython_utils.cy_yolo2_findboxes",
            sources=["objdet/cython_utils/cy_yolo2_findboxes.pyx"],
            libraries=["m"], # Unix-like specific
            include_dirs=[numpy.get_include(), "."]
        ),
        Extension("objdet.cython_utils.cy_yolo_findboxes",
            sources=["objdet/cython_utils/cy_yolo_findboxes.pyx"],
            libraries=["m"], # Unix-like specific
            include_dirs=[numpy.get_include(), "."]
        )
    ]

else :
    ext_modules=[
        Extension("objdet.cython_utils.nms",
            sources=["objdet/cython_utils/nms.pyx"],
            libraries=["m"] # Unix-like specific
        ),        
        Extension("objdet.cython_utils.cy_yolo2_findboxes",
            sources=["objdet/cython_utils/cy_yolo2_findboxes.pyx"],
            libraries=["m"] # Unix-like specific
        ),
        Extension("objdet.cython_utils.cy_yolo_findboxes",
            sources=["objdet/cython_utils/cy_yolo_findboxes.pyx"],
            libraries=["m"] # Unix-like specific
        )
    ]

setup(
    version=VERSION,
	name='objdet',
    description='Object detection. YOLO via TensorFlow.',
    license='GPLv3',
    packages = find_packages(),
    ext_modules = cythonize(ext_modules)
)