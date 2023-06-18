# gempy-geotop-pilot

This project is a first attempt to model some of the areas the Netherlands using GemPy and
its supported packages.


## TODO:

- [x] Prepare structure
    - [x] Test folder
    - [x] Examples folder
- [ ] Read first data set with subsurface
  - [ ] Read borehole data
   
   
## Data thoughts

- We are missing orientation
- The borehole data is very dense
- A lot of formations, we should start with a subset

- I will start with the South area for no special reason

### Data Types


- Directly supported by GemPy:

** Borehole data **
- The specific way data is provided is not supported by subsurface out of the box.
- ? Is it worth to make the effort to make it compatible with subsurface?
  - I will start by making the reader in this package and then I can decide if it is worth to move it to subsurface.

** Auxiliary data **

** Topograpy **