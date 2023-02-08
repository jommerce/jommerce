======
models
======

Session
=======

.. class:: Session

    .. py:method:: __getitem__(key)

      Example: ``fav_color = request.session['fav_color']``

    .. py:method:: __setitem__(key, value)

      Example: ``request.session['fav_color'] = 'blue'``

    .. py:method:: __delitem__(key)

      Example: ``del request.session['fav_color']``. This raises ``KeyError``
      if the given ``key`` isn't already in the session.

    .. py:method:: __contains__(key)

      Example: ``'fav_color' in request.session``

    .. py:method:: get(key, default=None)

      Example: ``fav_color = request.session.get('fav_color', 'red')``

    .. py:method:: pop(key, default=None)

      Example: ``fav_color = request.session.pop('fav_color', 'blue')``

    .. py:method:: keys()

    .. py:method:: items()

    .. py:method:: values()

    .. py:method:: setdefault()

    .. py:method:: clear()

    .. py:method:: update()
