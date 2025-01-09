'''
The setup.py file is an ssentials part of packaing and distributing
Python Projects. It is used by setuptools to define the configuration 
of your project, such as it's metadata, dependencies, and more.
'''
# find_packages :- consider an folder having __init__.py file 
# as package
from setuptools import find_packages, setup
from typing import List

def get_requirments()-> List[str]:
    '''
    This function returns the list of requirements.
    '''
    requirement_list:List[str] = []
    try:
        with open("requirements.txt","r") as file:
            # Reading lines from the file
            lines = file.readlines()
            # Procssing each line
            for line in lines:
                requirement = line.strip()
                # Ignoring empty lines and end of requiremnet fie "-e ."
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("rquirements.txt filr not found")
    
    return requirement_list

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Deepak Khokhar",
    author_email="deepakkhokhar1313@gmail.com",
    packages=find_packages(),
    install_requires=get_requirments()
)