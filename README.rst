==========
gotenshita
==========

.. image:: https://badge.fury.io/py/gotenshita.svg
    :target: https://badge.fury.io/py/gotenshita
.. image:: https://travis-ci.org/wkentaro/gotenshita.svg?branch=master
    :target: https://travis-ci.org/wkentaro/gotenshita

See Gotenshita court open status.
The information is got from `undoukai <http://www.undou-kai.com/senyu/senyu_yoyaku.html>`_.


Install
=======

::

  pip install gotenshita


Usage
=====

::

  % gotenshita -h
  usage: gotenshita [-h] [-p] [-t] [court]

  positional arguments:
    court            A to F (default is all), supports multiple select like
                     'a,f'

  optional arguments:
    -h, --help       show this help message and exit
    -p, --show-past  show even if past time
    -t, --tomorrow   show tomorrow's data


.. image:: images/demo.png


License
=======
| Copyright (C) 2015-2016 Kentaro Wada
| Released under the MIT license
| http://opensource.org/licenses/mit-license.php
