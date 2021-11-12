from fipy import numerix, CellVariable

def get_steel_specific_heat(temperature, mesh):
    
    temperature_array = numerix.array(temperature)
    specific_heat = 330.9+0.563*temperature_array-4.015e-4*temperature_array**2.0+9.465e-8*temperature_array**3.0
    
    return CellVariable(mesh = mesh, name = 'specific heat steel', value=specific_heat)

def get_steel_thermal_conductivity(mesh, temperature):
    
    temperature_array = numerix.array(temperature)
    thermal_conductivity = 11.82 + 1.06e-2*temperature_array
    
    return CellVariable(mesh = mesh, name = 'steel thermal conductivity', value = thermal_conductivity)

def get_gas_thermal_conductivity(mesh, temperature):
    
    temperature_array = numerix.array(temperature)
    thermal_conductivity = -0.1125/numerix.sqrt(temperature_array) + 1.35e-3*numerix.sqrt(temperature_array)+1.453e-7*temperature_array**(1.5)
    
    return CellVariable(mesh = mesh, name = 'gas thermal conductivity', value=thermal_conductivity)

def get_effective_cond(mesh, temperature, packing_factor):
    N = 12.0 #coordination number
    particle_diameter = 40e-6
    
    L = 5.4e-4/particle_diameter
    
    gas_cond = get_gas_thermal_conductivity(mesh, temperature)
    cond_array = numerix.array(gas_cond)
    
    k = cond_array*0.5*packing_factor* N *(0.5*numerix.log(1+L)+numerix.log(1+numerix.sqrt(L)) +1/(1+numerix.sqrt(L))-1)
    
    return CellVariable(mesh = mesh, name = 'effective thermal conductivity', value=k)

def get_effective_density(gas_density, solid_density, packing_factor):
    return solid_density * packing_factor + gas_density*(1-packing_factor)

def get_effective_specific_heat(gas_density, solid_density, packing_factor, specific_heat_gas, temperature, mesh):
    density = get_effective_density(gas_density, solid_density, packing_factor)
    specific_heat =  (solid_density*packing_factor*get_steel_specific_heat(temperature, mesh) + gas_density*(1-packing_factor)*specific_heat_gas)/density
    
    return CellVariable(mesh = mesh, name = 'specific heat', value=specific_heat)

def get_liquid_fraction(temperature, mesh, solidus_temperature, liquidus_temperature):
    temperature_array = numerix.array(temperature)
    
    mushy_array = (temperature_array - solidus_temperature)/(liquidus_temperature-solidus_temperature)
    
    solid_bool = numerix.array(temperature) < solidus_temperature
    liquid_bool = numerix.array(temperature) > liquidus_temperature

    liquid_fraction = numerix.where(solid_bool & liquid_bool, numerix.NaN, mushy_array)
    liquid_fraction[liquid_bool] = 1.0
    liquid_fraction[solid_bool] = 0.0

    return CellVariable(mesh = mesh, name = 'liquid_fraction', value = liquid_fraction)

