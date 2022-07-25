=============
configuration
=============

AUTH_SESSION_COOKIE_NAME
------------------------
.. code-block:: python

    AUTH_SESSION_COOKIE_NAME = "session_key"

The name of the cookie to use for sessions. This can be whatever you want
(as long as it’s different from the other cookie names in your application).

AUTH_SESSION_COOKIE_AGE
-----------------------
.. code-block:: python

    AUTH_SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2

Default: 1209600 (2 weeks, in seconds)
The age of session cookies, in seconds.

AUTH_SESSION_COOKIE_DOMAIN
--------------------------
.. code-block:: python

    AUTH_SESSION_COOKIE_DOMAIN = None

The domain to use for session cookies. Set this to a string such as "example.com" for cross-domain cookies,
or use None for a standard domain cookie.

To use cross-domain cookies with **CSRF_USE_SESSIONS**, you must include a leading dot (e.g. ".example.com") to accommodate
the CSRF middleware’s referer checking.

Be cautious when updating this setting on a production site.
If you update this setting to enable cross-domain cookies on a site that previously used standard domain cookies,
existing user cookies will be set to the old domain. This may result in them being unable to log in as long as these cookies persist.

AUTH_SESSION_COOKIE_SECURE
--------------------------
.. code-block:: python

    AUTH_SESSION_COOKIE_SECURE = False

Whether to use a secure cookie for the session cookie.
If this is set to True, the cookie will be marked as “secure”,
which means browsers may ensure that the cookie is only sent under an HTTPS connection.

Leaving this setting off isn’t a good idea because an attacker could capture an unencrypted session cookie with
a packet sniffer and use the cookie to hijack the user’s session.

AUTH_SESSION_COOKIE_PATH
------------------------
.. code-block:: python

    AUTH_SESSION_COOKIE_PATH = "/"

The path set on the session cookie. This should either match the URL path of your Django installation or be parent of that path.

This is useful if you have multiple Django instances running under the same hostname.
They can use different cookie paths, and each instance will only see its own session cookie.

AUTH_SESSION_COOKIE_HTTPONLY
----------------------------
.. code-block:: python

    AUTH_SESSION_COOKIE_HTTPONLY = True

Whether to use HttpOnly flag on the session cookie.
If this is set to True, client-side JavaScript will not be able to access the session cookie.

HttpOnly is a flag included in a Set-Cookie HTTP response header.

This makes it less trivial for an attacker to escalate a cross-site scripting vulnerability into full hijacking of a user’s session.
There aren’t many good reasons for turning this off. Your code shouldn’t read session cookies from JavaScript.

AUTH_SESSION_COOKIE_SAMESITE
----------------------------
.. code-block:: python

    AUTH_SESSION_COOKIE_SAMESITE = "Lax"

The value of the SameSite flag on the session cookie.
This flag prevents the cookie from being sent in cross-site requests thus preventing CSRF attacks and making
some methods of stealing session cookie impossible.

Possible values for the setting are:

``'Strict'``: prevents the cookie from being sent by the browser to the target site in all cross-site browsing context,
even when following a regular link.

For example, for a GitHub-like website this would mean that if a logged-in user follows a link to a private GitHub project
posted on a corporate discussion forum or email, GitHub will not receive the session cookie and the user won’t be able to
access the project. A bank website, however, most likely doesn’t want to allow any transactional pages to be linked from
external sites so the 'Strict' flag would be appropriate.

``'Lax'``: provides a balance between security and usability for websites that want to maintain
user’s logged-in session after the user arrives from an external link.

In the GitHub scenario, the session cookie would be allowed when following a regular link from an external website and
be blocked in CSRF-prone request methods (e.g. POST).

``'None'`` (string): the session cookie will be sent with all same-site and cross-site requests.

``False`` (bool): disables the flag.


.. note::

    Modern browsers provide a more secure default policy for the SameSite flag and will assume Lax
    for cookies without an explicit value set.
