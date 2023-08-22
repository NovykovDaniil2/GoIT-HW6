from setuptools import setup, find_namespace_packages

setup(name='clean-folder_HW7',
      version='1',
      description='This package will help you clean up the folder',
      author='Daniil Novykov',
      license='MIT',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      packages=find_namespace_packages(),
      entry_points={'console_scripts': [
          'clean-folder=clean_folder.clean:main']}
      )
