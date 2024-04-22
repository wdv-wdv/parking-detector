# Parking Detector

This is my first endeavor into using Computer Vision (OpenCV) and Python.

Like most people living in London will know, street parking is highly contested and everybody wants to park in front of their own home. Parking detector analyzes images and reports when a new parking spot opens.

## How to Use

The script is executed from the command prompt and requires a path to the image to be analyzed.

```cli
parkingdetector FILENAME
```

Remember to update the `parkingdetector.ini` / `parkingdetector.dev.ini` located in the script-root folder. Details are lower down.

This can be automated by using something like incron.

```text
#incrontab  
\path\to\images\ IN_CREATE \python-scripts\parkingdetector $@/$#
#or  
\path\to\images\ IN_MODIFY  \python-scripts\parkingdetector $@/$#
```

[incrontab man page](https://manpages.debian.org/testing/incron/incrontab.5.en.html)

## What Does the Script Do

After the `cli.py` checks command arguments and parameters, it passes control over to the `process.py` which handles the chain of executions and loads the image into memory.

### Apply Mask

`mask.py`

Before detecting any object, a mask is applied to the image to limit/focus an area-of-interest. The mask is a simple black and white image where the white area will be the area of interest. I used a Paint.Net .pdn file.

See the example in the resource folder.

### Detect Objects

`detect.py`

Using the YOLO model from Ultralytics, the image is inspected for known COCO objects which are filtered by type being a car and location in terms of distance from the curb.

While the masking limited detection to the parking area only, passing cars are also at times being detected. To filter out these false positives, the bottom end of the detect box for the car needs to be in the lower half of the area-of-interest.

Gaps between cars are then calculated by looking for the shortest distance between two car objects. Two buffer end gaps are then added on the left or right of the last cars on each end.

In debug mode, detection boxes are drawn on the image.

* **Purple boxes:** Any object.
* **Red boxes:** Object of interest; car in the right location
* **Blue & Cyan boxes:** Gaps between cars. **Cyan** are where detect boxes overlap
* **Red cross:** Points along the top edge of the mask lower half

### Analyze

`analyze.py`

The next step is to determine which gaps collected from the detection phase are large enough to be a parking space.

Because of the perspective of the image caused by the angle of the camera, parking spaces may vary in pixel size on the image. In my case, I determine the parking space on the left side of the image is around 600 pixel width. The car parked on the right edge is about a quarter of the size. This is configurable in the `.ini` file. Example below.

```ini
FACTOR = 0.25
LENGTH = 600
```

A yellow box is drawn on the image where the space is located.

### Parking Status

`status.py`

The status module will determine if an alert should be sent. Reporting is delayed by 5 minutes to prevent false reporting.

The current state of parking is stored locally. The easiest solution was to leverage the config/ini feature. In the ini file is a special section `[Status]` just for this.

```ini
[Status]
parking = False
first = 2024-04-19 22:45:06.880964+00:00
number = 0
```

### Slack Message

`slack.py`

If the status module allows reporting, a Slack message is sent with the image attached.

## Configuration (INI)

Configuration settings are held in the `parkingdetector.ini` located in the script-root folder. When run in debug mode (un-optimized), the script will use the `parkingdetector.dev.ini` instead.

```ini
[Detect]
mask_filename = /path/to/mask.jpg

[Analyze]
MERIDIEM = 0
FACTOR = 0.25
LENGTH = 600

[Slack]
token = <place your Slack token here>
channel_name = parking

[Status]
parking = False
first = 2024-04-19 22:45:06.880964+00:00
number = 0
```

### `[Detect]` section

* **mask_filename:** path to the area-of-interest mask image

### `[Analyze]` section

This is to handle perspective caused by camera angles.

* **MERIDIEM:** Represents the closest point to the camera in pixels from the left of the image. Currently, this only works with the MERIDIEM on the left edge of the image.
* **FACTOR:** The difference in object size from the MERIDIEM to the edge of the image
* **LENGTH:** Size of a parking space in pixels on the MERIDIEM

### `[Slack]` section

* **token:** After creating the appropriate Slack API bot app. This is where the token goes.
* **channel_name:** The name of the channel where the messages will be sent.

### `[Status]` section

This is used by the script to store parking space status. **Do not change anything here**

## License

`parkingdetector` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
