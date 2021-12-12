from fipy import numerix

L_x = 0.0004
L_y = 0.0002
L_z = 0.00006

N_x = 30
N_y = 30
N_z = 26

dx = L_x / N_x
dy = L_y / N_y
dz = L_z / N_z

packing_efficiency = 0.6

T_A = 300.0

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
steel_cond_fluid = 30.0 #???

laser_power = 60.0
beam_radius = 30e-6
distribution_factor = 1.0
scanning_speed = 1.0 #1000 mm per second

N_IH = laser_power*steel_liquid_absoprtion/(numerix.pi*beam_radius**2*scanning_speed)/(steel_density_liquid*steel_fluid_c*(steel_T_L-T_A)+steel_density_liquid*steel_latent_heat)

layers = 3
hatches = 5

layer_thickness = L_z / layers
hatch_width = L_y / hatches

time_steps = 100
dt = beam_radius / scanning_speed * 0.1