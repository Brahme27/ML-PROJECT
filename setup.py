from setuptools import find_packages,setup

from typing import List
HYPEN_E_DOT="-e ."
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements        

setup(
    name="ML PROJECT",
    version="0.0.1",
    author="Brahme",
    author_email="zaynbrahme@gmail.com",
    packages=find_packages(), #checks where ever there is __init__ and consider it as package
    install_requires=get_requirements("requirements.txt")
) 




'''
why -e . in requirements,txt 

In a requirements.txt file, adding -e . 
at the end is done to install the current project in editable mode 
after installing all the necessary dependencies. 
The dependencies, such as external libraries like numpy or pandas, 
are installed first to ensure your project has everything it needs 
to run properly. Once the dependencies are set up, -e . 
installs your project in a way that allows you to make changes to the code, 
and those changes will be reflected immediately without needing to reinstall the package. 
This is particularly useful during development, 
as it makes the process more efficient by allowing live updates to the code.
'''