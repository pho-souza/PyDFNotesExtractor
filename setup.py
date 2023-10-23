#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pip/pyinstaller build script for app.

Install as Python package:
    python3 setup.py install

Create EXE/APP:
    python3 setup.py build_binary
"""

import os
import sys
import shutil
import setuptools
import distutils.cmd
from app import __version__

OSX_INFO_PLIST = "configs/osx/Info.plist"

NAME = 'app'
MAIN = 'pydfannots.py'
VERSION = __version__


class BuildBinaryCommand(distutils.cmd.Command):
    description = 'build binary release'
    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass
    
    # noinspection PyShadowingNames
    def run(self):
        if sys.platform == 'darwin':
            with open(OSX_INFO_PLIST, 'r') as file:
                filedata = file.read()
                filedata = filedata.replace('5.5.2', VERSION)
            with open(OSX_INFO_PLIST, 'w') as file:
                file.write(filedata)
                
            command_gui = f'pyinstaller --noconfirm --onefile --windowed --noupx --icon "app/gui_assets/logo.icns" --name "pydfannotsgui" --clean --additional-hooks-dir "."  "pydfannots-gui.py"'
            command_cli = f'pyinstaller --noconfirm --onefile  --name "pydfannots" --noupx --clean  "pydfannots.py"'

            os.system(command_gui)
            #os.system(command_cli)
            if os.path.exists(f'dist/pydfannots_osx'):
                shutil.rmtree(f'dist/pydfannots_osx')
            os.makedirs(f'dist/pydfannots_osx', exist_ok=True)
            #shutil.move(f'dist/pydfannots.app',f'dist/pydfannots_osx/pydfannots_osx.app')
            shutil.move(f'dist/pydfannotsgui.app',f'dist/pydfannots_osx/pydfannotsgui_osx.app')
            os.makedirs(f'dist/pydfannots_osx/app', exist_ok=True)
            try:
                shutil.copytree(f'app/gui_assets', f'dist/pydfannots_osx/app/gui_assets', dirs_exist_ok=True, ignore_dangling_symlinks=True)
            except:
                pass
            try:
                shutil.copytree(f'app/templates', f'dist/pydfannots_osx/app/templates', dirs_exist_ok=True, ignore_dangling_symlinks=True)
            except:
                pass
            # os.chmod('dist/PyDFAnnots.app/Contents/Resources/7z', 0o777)
            # TODO /usr/bin/codesign --force -s "$MACOS_CERTIFICATE_NAME" --options runtime dist/Applications/Kindle\ Comic\ Converter.app -v
            # os.system('appdmg pydfannots.json dist/pydfannots' + "_osx" + '.dmg')
            exit(0)
        elif sys.platform == 'darwin_future_test':
            APP = ['pydfannots-gui.py']
            OPTIONS = {
                'argv_emulation': True
            }
            setuptools.setup(
                app = APP,
                options = {'py2app': OPTIONS},
                setup_requires = ['py2app'])
        elif sys.platform == 'win32':
            # command_gui = 'pyinstaller --noconfirm --onedir --windowed --noupx --icon "app/gui_assets/logo.ico" --name "PyDFAnnots GUI" --clean --add-data "app/gui_assets/;app/gui_assets/" --add-data "app/templates;app/templates/" --additional-hooks-dir "."  "app-gui.py"'
            command_gui = f'pyinstaller --noconfirm --onefile --windowed --noupx --icon "app/gui_assets/logo.ico" --name "pydfannotsgui" --clean --additional-hooks-dir "."  "pydfannots-gui.py"'
            command_cli = f'pyinstaller --noconfirm --onefile  --name "pydfannots" --noupx --clean  "pydfannots.py"'
            # command_cli = 'pyinstaller --noconfirm --onedir --noupx --name "PyDFAnnots" --clean --add-data "app/templates;app/templates/"  "app.py"'
            # os.system('pyinstaller -y -F -i app\\gui_assets\\logo.ico -n app_' + VERSION + ' -w --noupx pydfannots-gui.py')
            os.system(command_gui)
            os.system(command_cli)
            if os.path.exists(f'dist/PyDFAnnots_win'):
                shutil.rmtree(f'dist/PyDFAnnots_win')
            os.makedirs(f'dist/PyDFAnnots_win/app', exist_ok=True)
            shutil.move(f'dist/pydfannots.exe',f'dist/PyDFAnnots_win/pydfannots.exe')
            shutil.move(f'dist/pydfannotsgui.exe',f'dist/PyDFAnnots_win/pydfannotsgui_win.exe')
            try:
                shutil.copytree(f'app/gui_assets', f'dist/PyDFAnnots_win/app/gui_assets', dirs_exist_ok=True, ignore_dangling_symlinks=True)
            except:
                pass
            try:
                shutil.copytree(f'app/templates', f'dist/PyDFAnnots_win/app/templates', dirs_exist_ok=True, ignore_dangling_symlinks=True)
            except:
                pass
            exit(0)
        elif sys.platform == 'linux':
            command_gui = f'pyinstaller --noconfirm --onefile --windowed --noupx --icon "./app/gui_assets/logo.ico" --name "pydfannotsgui" --clean --additional-hooks-dir "."  "./pydfannots-gui.py"'
            command_cli = f'pyinstaller --noconfirm --onefile  --name "pydfannots" --noupx --clean  "./pydfannots.py"'
            # # os.system('pyinstaller -y -F -i app\\gui_assets\\logo.ico -n app_' + VERSION + ' -w --noupx pydfannots-gui.py')
            os.system(command_gui)
            os.system(command_cli)
            if os.path.exists(f'dist/pydfannots_linux'):
                shutil.rmtree(f'dist/pydfannots_linux')
            os.makedirs(f'dist/pydfannots_linux', exist_ok=True)
            shutil.move(f'dist/pydfannots',f'dist/pydfannots_linux/pydfannots_linux')
            shutil.move(f'dist/pydfannotsgui',f'dist/pydfannots_linux/pydfannotsgui_linux')
            os.makedirs(f'dist/pydfannots_linux/app', exist_ok=True)
            try:
                shutil.copytree('./app/gui_assets', './dist/pydfannots_linux/app/gui_assets', dirs_exist_ok=True, ignore_dangling_symlinks=True)
            except:
                pass
            try:
                shutil.copytree('./app/templates', './dist/pydfannots_linux/app/templates', dirs_exist_ok=True, ignore_dangling_symlinks=True)
            except:
                pass
            
            exit(0)
        else:
            exit(0)

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    cmdclass={
        'build_binary': BuildBinaryCommand,
    },
    name=NAME,
    version=VERSION,
    author='Pedro Souza',
    author_email='pho.souza.mail@gmail.com',
    description='PDF annotations extract using PyMuPDF.',
    long_description=readme,
    url='https://github.com/pho-souza/app',
    license=license,
    keywords=['pdf', 'annotations', 'highlight', 'pymupdf', 'obsidian'],
    entry_points={
        'console_scripts': [
            'pydfannots=app.cli:main',
        ],
        'gui_scripts': [
            'pydfannots=app.gui:main',
        ],
    },
    packages=['pydfannots'],
    install_requires=[
        'PyMuPDF>=1.21.1',
        'tkinterdnd2',
        'Jinja2'
    ],
    classifiers=[],
    zip_safe=False,
)