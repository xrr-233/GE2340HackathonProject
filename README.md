# GE2340 Hackathon Project

## Introduction

This is the project code of our GE2340 project. We choose topic 3: *Artificial Intelligence in Final Frontier — Space and Mother Earth!*

The topic we chose was *MAPPING SPACE TRASH IN REAL TIME*. It required us to develop an open-source geospatial application that displays and locates every known debris object orbiting Earth in real-time.

## 1st Stage - Shared Report File

https://docs.google.com/document/d/1TG3_h5EHDksCA8Txf1GN5Vv41esOtmRsXArG0DyZbE8/edit

The document in this link was composed during October 2-3, which was the date that the Hackathon took place. It records our initial attempt to work out the project.

## 2nd Stage - Further Exploration

Based on our first prototype, we developed our ideas and made deeper research into this topic. Here are some key points we have discovered:

- Cesium

  A JavaScript library that displays 3D earth and maps. Use WebGL to accelerate graphics for rendering. With specific data format such as Czml, it can easily generate the orbit of the satellites. Good performance on dynamic data visualization, faster than Worldwind JS.

- CZML

  A json data format that is used to describe a dynamic graphical scene. Mainly used for the Cesium virtual globe visualization on web browsers.

- TLE

  https://www.space-track.org/documentation#/tle

  In our project we focus on the second line, which includes 6 orbital parameters determining an orbit:

  1. **Semi-major axis**, which is half of the major axis of ellipse. For the circle, that is the radius;
  2. **Orbital eccentricity**, the ratio of the distance between the two focal points of the ellipse and its major axis. For a circle, it is 0.
  3. **Orbital inclination**, the angle between the orbital plane and the equatorial plane of the Earth. For a geostationary satellite above the equator, the inclination is 0.
  4. **Ascending intersection right ascension**. There exists a point at which a satellite crosses the equator as it moves from the southern to the northern hemispheres. The angle between this point and the vernal equinox with regard to the centre of the earth is called the ascending intersection right ascension.
  5. **Argument of perigee**, the Angle between perigee and ascending point of the earth.
  6. **True anomaly**, which tells the position of the satellite in orbit at the time when this TLE is recorded.

- LSTM

  Because the TLE data will change with time, it becomes a time series. And to predict the future data of the time series, LSTM is a good tool. It has better performance in predicting time series than RNN.

## Project Structure

### Workspace

The <u>workspace</u> is the "Project" folder.

### Framework

Flask framework is adopted for this project.

- "apps" folder: the Python code area, which can be understood as the back-end computation. In this folder, there are folders representing the back-end operations of different pages.  `__init__.py` is used to initialize the app.
  - "index" module: in `view.py`, it is for the initialisation of the template `index.html`.
  - "compute" module: in `LSTM.py`, it is for building a LSTM framework by <u>tensorflow2 and keras</u>; in `view.py`, it manages all the processing work after user's input.
- "static" folder: stores various files, such as image, CSS, Javascript, and data.

- "template" folder: called a template, which is used to render HTML. In our project it is `index.html`

- `app.py`: main program. By clicking <u>"play"</u> the program can directly generate a site. Click in to see the results.

It is recommended to run this project using **Pycharm IDE Pro** (free for students) and load the Flask framework.

## Use

You should enter a <u>correct</u> ID of a satellite. And because our earliest data is from the 250th day in 2021, you should choose a date <u>later</u> than this day. Until now the processing progress can only be seen in the <u>terminal</u>. After processing, clear the cache in the browser to see the result.

We provide a set of data to be the example (in Project/static/data/result.txt & result.czml).
