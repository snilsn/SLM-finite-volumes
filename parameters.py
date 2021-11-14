L_x = 0.0005
L_y = 0.0002
L_z = 0.00006

N_x = 55
N_y = 25
N_z = 20

dx = L_x / N_x
dy = L_y / N_y
dz = L_z / N_z

packing_efficiency = 0.3

g = 9.81
sigma = 5.670374419e-8

argon_density = 0.974
argon_c = 519.16

steel_T_L = 1733.0
steel_T_S = 1693.0
steel_density = 7800.0
steel_density_liquid = 6881
steel_latent_heat = 272.0e3
steel_visc = 7.0e-3
steel_surface_tension_derivative = -0.40e-3
steel_liquid_absoprtion = 0.3
steel_powder_absoprtion = 0.7
steel_volumentric_exp_coeff = 5.85e-5
steel_youngs_modulos = 206.0
steel_fluid_c = 790.0
steel_emissivity = 0.7

laser_power = 60.0
beam_radius = 60e-6
distribution_factor = 1.5
scanning_speed = 0.25 #250 mm per second

layers = 5
hatches = 5

layer_thickness = L_z / layers
hatch_width = L_y / hatches

time_steps = 100
dt = beam_radius / scanning_speed * 0.05