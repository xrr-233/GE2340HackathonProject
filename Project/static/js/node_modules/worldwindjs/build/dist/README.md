![Emxsys](docs/emxsys_logo.png)

# WorldWindJS
[![NPM](https://img.shields.io/npm/v/worldwindjs.svg)](https://www.npmjs.com/package/worldwindjs) 

## Important News
***Mitigation efforts are underway to ensure that WorldWindJS based projects are insulated from the effects of the NASA WorldWind project suspension.***

## A community supported and enhanced Web WorldWind library
__WorldWindJS__ is a fork of the popular [Web WorldWind](https://github.com/NASAWorldWind/WebWorldWind)
library from NASA (with contributions from ESA). This fork provides a release channel for builds based on the latest fixes
and features from WebWorldWind's [develop branch](https://github.com/NASAWorldWind/WebWorldWind/commits/develop) plus several "cherry-picked" enhancements from the WorldWind community.

This fork exists to support the development of several personal projects, including:

- [Explorer](https://worldwind.earth/explorer) - the WorldWind Explorer
- [WMT v2.0](https://worldwind.earth/wildfire) -  Wildfire Management Tool v2.0 (_under development_)
- [Bible Atlas](https://viewer.earth/bible-atlas) - Geography and cartography of the Holy Land (_under development_)
- [worldwind-react-globe](https://worldwind.earth/worldwind-react-globe/) - A React component for Web WorldWind
- [worldwind-react-globe-bs4](https://worldwind.earth/worldwind-react-globe-bs4/) - React Bootstrap4 UI components for Web WorldWind
- [worldwind-react-app](https://worldwind.earth/worldwind-react-app/) - A geo-browser web app using Web WorldWind with React and Bootstrap 4 

WorldWindJS is made available in the spirit of the NASA motto: _For the benefit of all._  Show your support for this project by giving it a [star](https://github.com/worldwindearth/worldwindjs/stargazers)!

### Enhancements include:

- A template for creating geo-browser web apps with Bootstrap and Knockout (apps/worldwind-app-template).
- Keyboard navigation controls for the globe
- Improved the resolution of Bing imagery
- Support for a translucent night-image
- Removed dependency vulnerabilities
- Fixed WMTS tile geo-registration 

### Migrating from NASA WebWorldWind

- The WorldWindJS npm package is available in the [npm repository](https://www.npmjs.com/package/worldwindjs).
- WorldWindJS is available on the __unpkg__ and __jsDelivr__ CDNs. See [CDN providers](https://github.com/worldwindearth/worldwindjs/wiki/CDN-providers) in the wiki for examples.
- The project supports npm dependencies on its git repository: See [npm dependencies](https://github.com/worldwindearth/worldwindjs/wiki/npm-dependencies) in the wiki for examples. 
- The JS libraries (production and debug) and the image resources are available in the [GitHub releases](https://github.com/worldwindearth/worldwindjs/releases/latest).


#### Changes from WebWorldWind release 0.9.0
- `NavigatorState` has been deprecated. Its properties have migrated to `DrawContext`.
- Added the `HeatMap` from the WorldWind `NASAWorldWind/feature/heatmap` branch.
- Added the `ShapeEditor` from the WorldWind `NASAWorldWind/enhancement/shape_editor_refactoring` branch.

#### Changes from the WebWorldWind develop branch
- WorldWindJS is a drop in replacement for WebWorldWind's __worldwind.js__ and __worldwind.min.js__ libraries built from the WebWorldWind develop branch. There are no changes to the API other than additions.

### Additional Resources
#### Tutorials
- [How to Build a WorldWindJS Web App](https://worldwindearth.github.io/worldwindjs/) on the project website

#### Demos
- [__worldwind-web-app__ demo](https://worldwindearth.github.io/worldwind-web-app/): A geo-browser built with Bootstrap and KnockoutJS.
- [__worldwind-react-app__ demo](https://worldwind.earth/worldwind-react-app/): A geo-browser built with React using the [worldwind-react-globe](https://github.com/emxsys/worldwind-react-globe) and [worldwind-react-globe-bs4](https://github.com/emxsys/worldwind-react-globe-bs4) components.

#### Related projects
- __[worldwind-react-globe](https://github.com/emxsys/worldwind-react-globe)__: A React-based Globe component that encapulates WorldWindJS.
- __[worldwind-react-globe-bs4](https://github.com/emxsys/worldwind-react-globe-bs4)__: Bootstrap UI components for the Globe component including a layer manager, tools palette, placename search, and settings.

#### NPM Downloads
- [__worldwindjs__ package](https://www.npmjs.com/package/worldwindjs): This library as an npm package.
- [__worldwind-react-globe__ package](https://www.npmjs.com/package/worldwind-react-globe): Globe component encapulating WorldWindJS.
- [__worldwind-react-globe-bs4__ package](https://www.npmjs.com/package/worldwind-react-globe-bs4): Bootstrap UI for the Globe component.

---

## Web WorldWind

3D virtual globe API in JavaScript for the web, developed by NASA. The European Space Agency has provided valuable
contributions to this platform since 2015. Web WorldWind provides a geographic context, complete with terrain, and a
collection for shapes for displaying and interacting with geographic or geo-located information in 3D and 2D in any
modern web browser. High-resolution terrain and imagery is retrieved from remote servers automatically as needed, while
enabling developers to include their own custom terrain and imagery.

[worldwind.arc.nasa.gov](https://worldwind.arc.nasa.gov) has setup instructions, developers guides, API documentation and more.

## Get Started

The Web WorldWind [Developer's Guide](https://worldwind.arc.nasa.gov/web) has a complete description of Web WorldWind's
functionality. You'll also find there links to many Web WorldWind resources, including a user guide. For novices on WorldWind, 
A [Get Started](https://worldwind.arc.nasa.gov/web/get-started/) tutorial is the place to go. The latest Web WorldWind release 
provides many simple [examples](https://github.com/NASAWorldWind/WebWorldWind/tree/develop/examples) showing how to use all of
 Web WorldWind's functionality.

## Building

[Install NodeJS](https://nodejs.org). The build is known to work with Node.js 12.18.0 LTS.

- `npm install` downloads WorldWind's dependencies and builds everything

- `npm run build` builds everything

- `npm run doc` generates the WorldWind API documentation

- `npm run test` runs WorldWind's unit tests

- `npm run test:watch` automatically runs WorldWind's unit tests when source code changes

- `npm version <newversioo>` changes the version number in package.json

- `npm publish` publishes the build to npm

## License

Copyright 2003-2006, 2009, 2017, 2020 United States Government, as represented
by the Administrator of the National Aeronautics and Space Administration.
All rights reserved.

The NASAWorldWind/WebWorldWind platform is licensed under the Apache License,
Version 2.0 (the "License"); you may not use this file except in compliance
with the License. You may obtain a copy of the License
at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

NASAWorldWind/WebWorldWind also contains the following 3rd party Open Source
software:

   ES6-Promise – under MIT License
   libtess.js – SGI Free Software License B
   Proj4 – under MIT License
   JSZip – under MIT License

A complete listing of 3rd Party software notices and licenses included in
WebWorldWind can be found in the WebWorldWind 3rd-party notices and licenses
PDF found in code  directory.
