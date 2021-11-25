from fipy import numerix, CellVariable

def get_steel_specific_heat(temperature, mesh):
    
    #returns the specific heat of solid steel as CellVariable
    #valid for temperatures below solidus temperature
    
    temperature_array = numerix.array(temperature)
    specific_heat = 330.9+0.563*temperature_array-4.015e-4*temperature_array**2.0+9.465e-8*temperature_array**3.0
    
    return CellVariable(mesh = mesh, name = 'specific heat steel', value=specific_heat)

def get_effective_specific_heat(gas_density, solid_density, packing_factor, specific_heat_gas, temperature, mesh):
    
    #returns the effectiv specific heat of the powder
    #valid if the powder isnt completely melted
    
    density = get_effective_density(gas_density, solid_density, packing_factor)
    specific_heat =  (solid_density*packing_factor*get_steel_specific_heat(temperature, mesh) + gas_density*(1-packing_factor)*specific_heat_gas)/density
    
    return CellVariable(mesh = mesh, name = 'specific heat', value=specific_heat)

def get_specific_heat(temperature, liquid, molten, gas_density, solid_density, packing_factor, solidus_temperature, fluid_c):
    
    #returns the specific heat of the powder below solidus temperature,
    #returns linear transistion of powder and liquid steel specific heat between solidus and liquidus temparture
    #returns liquid steel spec heat for temperatures higher liquidis
    #returns solid steel c, when a cell has melted completely and tempeature is below solidus
    
    mesh = temperature.mesh
    effective_heat = numerix.array(get_effective_specific_heat(gas_density, solid_density, packing_factor, gas_density, temperature, mesh))
    solid = numerix.array(1.0-liquid)
    liquid = numerix.array(liquid)
    steal_heat = numerix.array(get_steel_specific_heat(temperature, mesh))
    
    temp_array = numerix.array(temperature)
    molten_array = numerix.array(molten)
    
    bool_mask = molten_array == 1.0
    heat_array = numerix.where(bool_mask, solid*steal_heat+liquid*fluid_c, solid*effective_heat + liquid*fluid_c)
    
    return CellVariable(mesh = mesh, name = 'effective heat', value = heat_array)

def get_steel_thermal_conductivity(mesh, temperature):
    
    temperature_array = numerix.array(temperature)
    thermal_conductivity = 11.82 + 1.06e-2*temperature_array
    
    return CellVariable(mesh = mesh, name = 'steel thermal conductivity', value = thermal_conductivity)

def get_gas_thermal_conductivity(mesh, temperature):
    
    temperature_array = numerix.array(temperature)
    thermal_conductivity = -0.1125/numerix.sqrt(temperature_array) + 1.35e-3*numerix.sqrt(temperature_array)+1.453e-7*temperature_array**(1.5)
    
    return CellVariable(mesh = mesh, name = 'gas thermal conductivity', value=thermal_conductivity)

def get_effective_cond(mesh, temperature, packing_factor):
    
    N = 7.0 #coordination number
    particle_diameter = 40e-6
    
    L = 5.4e-4/particle_diameter
    
    gas_cond = get_gas_thermal_conductivity(mesh, temperature)
    cond_array = numerix.array(gas_cond)
    
    k = cond_array*0.5*packing_factor* N *(0.5*numerix.log(1+L)+numerix.log(1+numerix.sqrt(L)) +1/(1+numerix.sqrt(L))-1)
    
    return CellVariable(mesh = mesh, name = 'effective thermal conductivity', value=k)

def get_thermal_conductivity(temperature, packing_factor, molten, liquid, liquid_cond, solidus_temperature, N_IH):
    
    liquid_cond = get_melting_cond(N_IH, liquid_cond)
    mesh = temperature.mesh
    temp_array = numerix.array(temperature)
    molten_array = numerix.array(molten)
    
    effective_cond = numerix.array(get_effective_cond(mesh, temperature, packing_factor))
    steal_cond = numerix.array(get_steel_thermal_conductivity(mesh, temperature))
    solid = numerix.array(1.0-liquid)
    liquid = numerix.array(liquid)

    bool_mask = molten_array == 1.0
    
    k = numerix.where(bool_mask, solid*steal_cond+liquid*liquid_cond, solid*effective_cond+liquid*liquid_cond)
    
    return CellVariable(mesh = mesh, name = 'thermal conductivity', value = k)

def get_melting_cond(N_IH, liquid_cond):
    return (1.0+0.84*N_IH)*liquid_cond

def get_effective_density(gas_density, solid_density, packing_factor):
    return solid_density * packing_factor + gas_density*(1-packing_factor)

def get_liquid_fraction(temperature, mesh, solidus_temperature, liquidus_temperature):
    temperature_array = numerix.array(temperature)
    
    mushy_array = (temperature_array - solidus_temperature)/(liquidus_temperature-solidus_temperature)
    
    solid_bool = numerix.array(temperature) < solidus_temperature
    liquid_bool = numerix.array(temperature) > liquidus_temperature

    liquid_fraction = numerix.where(solid_bool & liquid_bool, numerix.NaN, mushy_array)
    liquid_fraction[liquid_bool] = 1.0
    liquid_fraction[solid_bool] = 0.0

    return CellVariable(mesh = mesh, name = 'liquid_fraction', value = liquid_fraction)

def update_molten_cells(molten_cells, liquid_fraction):
    
    molten_array = numerix.array(molten_cells)
    liquid_array = numerix.array(liquid_fraction)
    
    new_molten_array = numerix.zeros(len(molten_array))
    
    new_molten_array = numerix.where(liquid_array == 1.0, 1.0, 0.0)
    new_molten_array = numerix.where(molten_array == 1.0, 1.0, new_molten_array)
    
    molten_cells = CellVariable(mesh = molten_cells.mesh, name = 'molten', value = new_molten_array)
    
    return molten_cells