from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:
    '''
     this method return a list of requiremnts
    '''
    requirements = []

    with open(file_path, "r") as file:
        requirements = file.readlines()
        requirements = [line.replace("\n", "") for line in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name = 'amazon-india-mobilephone-data-analysis',
    version = '0.0.1',
    author = 'Sanjitha Amarathunga',
    author_email= 'author9x@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)