from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize


import os
import glob
import shutil

dir_tree_structure=[]
dir_tree_structure_delete_c=[]
for root, dirs, files in os.walk('.'):
    for f in files:
        # Following files are ignored from converting the cython as some of the files are entry modules and 
        # some files are needs to be kept as their original to run the code and engines.
        if f.endswith('.py') and (f not in ['i2b2_cdi_app.py','runner.py','setup.py','__init__.py','__main__.py','addProject.py','loadSQL.py','utils.py','persistData.py','projectUpgrade.py','config_helper.py','config.py'])and '/test/' not in os.path.join(root, f):
            dir_tree_structure.append(os.path.join(root, f))
            dir_tree_structure_delete_c.append(os.path.join(root, f.replace('.py','.c')))
print(dir_tree_structure)


setup(
    name="i2b2_etl",
    version="1.3.4",
    include_package_data=True,

    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules = cythonize(dir_tree_structure,compiler_directives={'always_allow_keywords': True}))

for i in range(len(dir_tree_structure_delete_c)):
    try:
        if os.path.exists(dir_tree_structure[i]):
            os.remove(dir_tree_structure[i])
            os.remove(dir_tree_structure_delete_c[i])
    except Exception as e :
        logger.error(e)