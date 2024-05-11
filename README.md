# gempy-geotop-pilot

This project is a first attempt to model some of the areas the Netherlands using GemPy and
its supported packages.

# Notes - Meeting 9.5.2024

## Minimal Actionable actions for 2024

### Resources:

- Willem 3 weeks
- Miguel - In kind
- Reinder - In kind

### Task:

1) Setting up repository - Willem

  1.1 Main project structure - Miguel

2) Pilot projects (priority):

  2.1 Subsection of South model - Miguel (High)

    2.1.1 Clay layer - Willem (High)

    2.1.2 Well correlation 40km 40 km

  2.2 Zeeland - Reinder (Low)

  2.4 Internal structural (Low)

  2.5 Jan Diederik/Clinoform (Low)


## TODO:

- [x] Prepare structure
    - [x] Test folder
    - [x] Examples folder
- [x] Read first data set ?with subsurface
  - [x] Read borehole data of one layer
- [x] First attempt to interpolate
- [ ] Start fine-tuning the interpolation
   
## Data thoughts

- We are missing orientation
- The borehole data is very dense
- A lot of formations, we should start with a subset

- I will start with the South area for no special reason

### Data Types


- Directly supported by GemPy:

**Borehole data**
- The specific way data is provided is not supported by subsurface out of the box.
- ? Is it worth to make the effort to make it compatible with subsurface?
  - I will start by making the reader in this package and then I can decide if it is worth to move it to subsurface.

**Auxiliary data**

**Topography**


## Issues

- (solved) Vertical exaggeration for pyvista plot is a bit broken and orientations did not show properly.
- (solved) Pyvista volume does not show the right colors
  - The issue seems to be that pyvista is splitting the scalar field not exactly at 1.5
  - **It was just float error**