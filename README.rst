==============================
Django Websocket Notifications
==============================

A Django application to deliver user notifications made with 
`django-snitch <https://github.com/marcosgabarda/django-snitch>`_ using WebSockets.

.. image:: https://img.shields.io/pypi/v/django-websocket-notifications
    :target: https://pypi.org/project/django-websocket-notifications/
    :alt: PyPI

.. image:: https://codecov.io/gh/marcosgabarda/django-websocket-notifications/branch/main/graph/badge.svg?token=EY6DV8O6ZT
    :target: https://codecov.io/gh/marcosgabarda/django-websocket-notifications

.. image:: https://img.shields.io/badge/code_style-black-000000.svg
    :target: https://github.com/ambv/black

.. image:: https://readthedocs.org/projects/django-websocket-notifications/badge/?version=latest
    :target: https://django-websocket-notifications.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Quick start
-----------

This applications works using django-channels, so, you need to integrate this with 
your project before to integrate django-websocket-notifications. So, to make the 
quick start as quick and simple as possible, we've made the following assumptions:

* You already have integrated django-channels
* You are using a channel layer, like Redis
* You have a `routing.py` file
* Your project uses DRF to deliver a RESTful API

**1** Install using pip:

.. code-block:: bash

    pip install django-websocket-notifications

**2** Add "websocket_notifications" to your INSTALLED_APPS settings like this:

.. code-block:: python

    INSTALLED_APPS += ('websocket_notifications',)

**3** Add the routing patterns to your `routing.py` file:

.. code-block:: python

    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter, URLRouter
    from websocket_notifications.routing import websocket_urlpatterns


    application = ProtocolTypeRouter(
        {"websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),}
    )

**4** (Optional) In order to test the integration, you can add the following view to your `urls.py` file to be able to access to a testing view:

.. code-block:: python

    urlpatterns += [
        path(
            "websocket-notifications/",
            include(
                "websocket_notifications.urls",
                namespace="websocket_notifications",
            ),
        ),
    ]

Now, you can access to `/websocket-notifications/listener/` to check the integration.

**5** Add the ViewSet to the DRF router:

.. code-block:: python

    from websocket_notifications.api.rest_framework import NotificationGroupViewSet


    router = routers.DefaultRouter()
    router.register("websocket-notifications/groups", viewset=NotificationGroupViewSet)

**6** Integrate with `django-snitch`:

.. code-block:: python

    from websocket_notifications.snitch.backends import WebSocketNotificationBackend


    @snitch.register(EVENT)
    class MyEventHandler(snitch.EventHandler):
        ephemeral = True
        notification_backends = [WebSocketNotificationBackend]