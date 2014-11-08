from datetime import datetime

class Planet:
  length_of_year_in_days = 365.25
  ecc = 0.0167
  inclination_deg = -23.44
  solar_declination = 0
  solar_constant = 1361 * 0.69 # W/m2, for v0.1 albedo 0.31
  current_time = datetime(2012, 6, 12, 0, 0)
  rotation_speed = 15 # degrees per hour
  winter_solstice_offset = 10 # used to find declination (latitude) of sun
  perigee_offset = -2

    def __init__(self, name, specified_time):
        self.name = name
        self.region_list = []
        self.longitude = np.array([
          0, 0, 120, -120,
          0, 36, 72, 108, 144, 180, -144, -108, -72, -36,
          0, 36, 72, 108, 144, 180, -144, -108, -72, -36,
          0, 36, 72, 108, 144, 180, -144, -108, -72, -36,
          0, 36, 72, 108, 144, 180, -144, -108, -72, -36,
          0, 120, -120, 0])
        self.latitude = np.array([
          90, 80.625, 80.625, 80.625,
          56.25, 56.25, 56.25, 56.25, 56.25, 56.25, 56.25, 56.25, 56.25, 56.25,
          18.75, 18.75, 18.75, 18.75, 18.75, 18.75, 18.75, 18.75, 18.75, 18.75,
          -18.75, -18.75, -18.75, -18.75, -18.75, -18.75, -18.75, -18.75, -18.75, -18.75,
          -56.25, -56.25, -56.25, -56.25, -56.25, -56.25, -56.25, -56.25, -56.25, -56.25,
          -80.625, -80.625, -80.625, -90])
        self.current_time = specified_time
        self.solar_declination = -asin()
        
    def set_time(self, specified_time):
        current_time = specified_time
        decimal_hour = current_time.hour + current_time.minute * 60 + current_time.second * 3600
        decimal_day = current_time.timetuple().yday + decimal_hour / 24
        hour_angle = 2 * pi * (decimal_hour - longitude / rotation_speed) / 24)
        solar_declination = -asin(
          sin(radians(inclination_deg) * 
          cos(2 * (decimal_day + winter_solstice_offset) / length_of_year_in_days + 
              2 * ecc * sin(2 * (decimal_day + perigee_offset) / length_of_year_in_days)
              )))
    
    def rotate(self, user):
        shine(self, user)
        convect(self, user)
        glow(self, user)
        display(self, user)
        
    def display(self, user)
    
    def shine(self, user)
      solar_elevation = asin(
        (cos(hour_angle) * cos(radians(latitude))) * cos(solar_declination) +
        sin(solar_declination) * sin(radians(latitude)) )
      np.clip(solar_elevation, 0, pi, out=solar_elevation)
      solar_energy = solar_constant * sin(solar_elevation) * user.timestep * 3600
