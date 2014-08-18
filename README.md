ytlist
======

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
Get one video.  | /video/id/      | GET           | None.                         | A video's details in JSON format.

JSON format returned from GET endpoints:
----------------------------------------
```javascript
{"id": 1, "title": "Some title.", "description": "Some desription.", "url": "XXXXXXX"}
```

The "url" element above is just the YouTube video id part.

JSON format expected by POST endpoint:
--------------------------------------
```javascript
{"url": "XXXXXXX"}
```

The "url" element above is just the YouTube video id part.
The rest will be figured out by the back end.

Status example:
---------------

Success:
```javascript
{"status": 0, "message": ""}
```

In the case of the POST endpoint, the message will be the id of the video that was added.

Error:
```javascript
{"status": 1, "Database not reachable."}
```

Installation
============

```fab install``` should do it. The installation requires:
* fabric (tested with v1.9.1),
* virtualenv (tested with v.1.11.5), and
* npm (tested with v.1.3.11).

Execution
=========

Execution is through the Django development server and sqlite3, for ease of deployment.
```fab run``` should be all that's required.

