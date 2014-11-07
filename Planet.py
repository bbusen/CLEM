from datetime import datetime



class Planet:

  length_of_year_in_days = 365.25
  ecc = 0.0167
  inclination_deg = -23.44
  solar_declination = 0
  solar_constant_W_per_m2 = 1361
  current_time = datetime(2012, 6, 12, 0, 0)

    def __init__(self, name, specified_time):
        self.name = name
        self.region_list = []
        self.longitude = [
          0, 0, 120, -120,
          0, 36, 72, 108, 144, 180, -144, -108, -72, -36,
          0, 36, 72, 108, 144, 180, -144, -108, -72, -36,
          0, 36, 72, 108, 144, 180, -144, -108, -72, -36,
          0, 36, 72, 108, 144, 180, -144, -108, -72, -36,
          0, 120, -120, 0]
        self.latitude = []
        self.current_time = specified_time
        self.solar_declination = -asin()
        
    def set_time(self, specified_time):
        current_time = specified_time
    
    def rotate(self, user):
        shine(self, user)
        convect(self, user)
        glow(self, user)
        display(self, user)
        
    def display(self, user)
    
    def shine(self, user)
