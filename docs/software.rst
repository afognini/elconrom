Usage of the ElConRoM library
==============================

The usage of the ElConRoM library is outlined in an example of moving motor 1.

.. code-block:: python

  from elconrom import ElConRoM
  import time

  motor = ElConRoM()

  #Select motor number 1
  motor.number(1)

  #Home motor
  motor.home()

  #Set it to 90 degrees
  motor.abs_position_degrees(90)

  #Wait one second
  time.sleep(1)

  #Drive back to zero degrees
  motor.abs_position_degrees(0)

It can be necessary to reduce the speed to reach more accurate stopping behavior. For example:

.. code-block:: python

  motor.speed(70)


Installation
===================

The ElConRoM Python library can be installed by the provided setup script.

You can install it either by::

	sudo python setup.py install

or by::

	sudo python3 setup.py install

depending on your Python installation. Note, ElConRoM needs Python 3 or higher.

You can test if the installation worked by importing the library:

.. code-block:: python

	import elconrom

If that did not give you an error the installation worked successfully.
