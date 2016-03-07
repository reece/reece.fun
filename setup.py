from setuptools import setup, find_packages

package_name = "reece.sandbox"
short_description = "This is the short description"
long_description = """This is a longer decsription about the project. It may span multiple lines."""

setup(
    author = 'Reece Hart',
    author_email = 'reecehart@gmail.com',
    description = short_description,
    license = 'Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)',
    long_description = long_description,
    name = package_name,
    packages = find_packages(),
    url = 'https://github.com/reece/reece.sandbox',
    use_scm_version = True,
    zip_safe = True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
      ],

    # keywords=[
    # ],

    # install_requires=[
    # ],

    setup_requires=[
	"setuptools_scm",
        "nose",
        #"sphinx",
        #"sphinxcontrib-fulltoc",
        "wheel",
    ],

    tests_require=[
        "coverage",
    ],
)

## <LICENSE>
## Copyright 2016 Reece Hart (reecehart@gmail.com)
## 
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## 
##     http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## </LICENSE>
