# encoding: utf-8

# (c) 2014-2023 Open Risk, all rights reserved
#
# FuriousBanker is licensed under the MIT license a copy of which is included
# in the source distribution of FuriousBanker. This is notwithstanding any licenses of
# third-party software included in this distribution. You may not use this file except in
# compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.


from setuptools import setup

__version__ = '0.3.0'

ver = __version__

setup(
    name='FuriousBanker',
    version=ver,
    packages=['FuriousBanker'],
    url='https://github.com/open-risk/FuriousBanker',
    download_url='https://github.com/open-risk/FuriousBanker/v_0.3.0.tar.gz',
    license='The MIT License (MIT)',
    author='Open Risk',
    author_email='info@openrisk.eu',
    description='A python game platform for learning about risk management',
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'networkx',
        'pytest',
        'kivy'
    ],
    include_package_data=True,
    zip_safe=False,
    provides=['FuriousBanker'],
    keywords=['serious games', 'simulation', 'risk management'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Financial and Insurance Industry',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ]
)
