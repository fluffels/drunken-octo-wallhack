drunken-octo-wallhack
=====================

This project implements a REST API for managing a list of YouTube videos.
The API is documented below.
Also included is a user interface for this API.

API
===

Function        | Resource        | HTTP Method   | Data                          | Returns
----------------|-----------------|---------------|-------------------------------|--------
List videos.    | /video/         | GET           | None.                         | A list of video details in JSON format.
Add video.      | /video/         | POST          | Video details in JSON format. | A status in JSON format.
Delete video.   | /video/id/      | DELETE        | None.                         | A status in JSON format.

Video details example:
----------------------
As received from GET /video/:
```javascript
{'id': 1, 'description': "Some desription.", 'url': "http://youtube.com/watch?v=XXXXXXX"}
```

As sent to POST /video/:
```javascript
{'url': "http://youtube.com/watch?v=XXXXXXX"}
```

Status example:
---------------

Success:
```javascript
{'status': 0, 'message': ""}
```

Error:
```javascript
{'status': 1, "Database not reachable."}
```

