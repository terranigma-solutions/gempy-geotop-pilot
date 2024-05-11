"""
Reading all boreholes and set up the stratigraphic pile

"""
import dotenv

from gempy_geotop_pilot.example_models import generate_south_model_base
import gempy as gp
import gempy_viewer as gpv

# %%
# TODO: Optimize surfaces

#  Read wells

# %%
dotenv.load_dotenv()

ve = 10

geo_model = generate_south_model_base(group_slicer=slice(5, 7))
gempy_plot3d = gpv.plot_3d(
    model=geo_model,
    show_data=True,
    show_lith=False,
    ve=ve,
    image=False,
    kwargs_pyvista_bounds={
            'show_xlabels': False,
            'show_ylabels': False,
            'show_zlabels': False,
    },
    kwargs_plot_data={'arrow_size': 100},
    kwargs_plot_structured_grid={'opacity': .8}
)

# %%
gpv.plot_2d(
    model=geo_model,
    section_names=['section1', 'section2', 'section3'],
    show_data=True,
    show_boundaries=False,
    ve=ve,
    projection_distance=100
)
