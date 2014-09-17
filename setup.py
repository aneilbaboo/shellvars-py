from setuptools import setup

def read(f):
    try:
        with open(f) as file:
            return file.read()
    except:
        return ""

setup(name='shellvars-py',
      version='0.1.2',
      description='Read environment variables defined in a shell script into Python.',
      author_email='aneil.mallavar@gmail.com',
      license='Apache2',
      py_modules=['shellvars'],
      long_description = read('README.md'),
      url="http://github.com/aneilbaboo/shellvars-py",
      author="Aneil Mallavarapu",
      include_package_data = True,
      classifiers = [
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ]
)
