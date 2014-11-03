class Planet:

  length_of_year_in_days = 365.25
  ecc = 0.0167
  inclination_deg = -23.44
  solar_declination = 0
  solar_constant_W_per_m2 = 1361
  
    def __init__(self, name):
        self.name = name
        self.region_list = []
        
    def set_time(self, current_time):
    
    def rotate(self, timestep, num_steps):
