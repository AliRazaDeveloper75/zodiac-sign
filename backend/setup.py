from setuptools import setup, find_packages

setup(
    name="palm-ai-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'Flask==2.3.3',
        'Flask-CORS==4.0.0',
        'opencv-python==4.8.1.78',
        'numpy==1.24.3',
        'Pillow==10.0.0'
    ],
)