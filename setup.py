'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools to define the configuration 
of your project, such as its metadata, dependencies, and more
'''


from setuptools import find_packages,setup
from typing import List

def get_requirements()->list[str]:
    '''
    This is function will return list of requirements
    '''

    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            #process each line
            for line in lines:
                #get rid of the white spaces before and after the words
                requirement=line.strip()
                #hand pick what you need
                if requirement and requirement!= '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("The requirements.txt file not found")

    return requirement_lst

print(get_requirements())

setup(
    name="Network Security",
    version="0.0.1",
    author="Akanksha Kushwaha",
    author_email="akushwaha033@outlook.com",
    packages=find_packages(),
    install_requires=get_requirements()

)
        

