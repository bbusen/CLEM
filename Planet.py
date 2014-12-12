from datetime import datetime
import numpy as np
import json, io

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
  num_cells = 48

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
        set_time(specified_time)

    def set_time(self, specified_time):
      current_time = specified_time
      decimal_hour = current_time.hour + current_time.minute * 60 + current_time.second * 3600
      decimal_day = current_time.timetuple().yday + decimal_hour / 24
      hour_angle = np.multiply((2 * pi / 24), np.divide(np.subtract(decimal_hour, longitude), rotation_speed))
      solar_declination = -asin(
        sin(radians(inclination_deg) * 
        cos(2 * (decimal_day + winter_solstice_offset) / length_of_year_in_days + 
        2 * ecc * sin(2 * (decimal_day + perigee_offset) / length_of_year_in_days) )))
    
    def rotate(self, user):
      while True:
        shine(self, user)
        convect(self, user)
        glow(self, user)
        display(self, user)
        if user.paused:
          with open('planet.txt', 'w') as outfile:
            json.dump(jsonData, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
          break
        
    def display(self, user):
      for i in range(num_cells):
        print repr(latitude[i]).rjust (6), repr(longitude[i]).rjust(6), repr(solar_energy[i]).rjust(6)
      print '\n'
    
    def shine(self, user):
      solar_elevation = np.asin(np.add(
        np.multiply(np.multiply(np.cos(hour_angle), np.cos(np.radians(latitude))), cos(solar_declination)),
        np.multiply(sin(solar_declination), np.sin(np.radians(latitude)))) )
      np.clip(solar_elevation, 0, pi, out=solar_elevation)
      solar_energy = np.multiply((solar_constant * user.timestep * 3600), np.sin(solar_elevation))
