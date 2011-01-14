Requires a configuration file ~/.google-reader-notification in YAML format. Example file:

	username: my.google.account@googlemail.com
	password: secretpassword!12

Also requires the libgreader (available through pypi) and rsvg, PIL (use your distributions packages).

Icon (in file "icon.svg") created by Alexander Metz, licensed under the [Create Commons CC BY-NC-SA 3.0 license](http://creativecommons.org/licenses/by-nc-sa/3.0/).

All other program code is subject to the following license

Installation
============
Currently, there's no nice installation method for this package. On Ubuntu, you can

  $ sudo apt-get install python-stdeb

and then

  $ pypi-install libgreader

to install the prerequisites in a nice way.

License
=======
Copyright (c) 2010 Marc Brinkmann

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
