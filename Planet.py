from datetime import datetime
import numpy as np
import json, io, sys, select, pdb, math

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
    self.set_time(specified_time)
    self.latitude = np.array([
          90, 80.625, 80.625, 80.625,
          56.25, 56.25, 56.25, 56.25, 56.25, 56.25, 56.25, 56.25, 56.25, 56.25,
          18.75, 18.75, 18.75, 18.75, 18.75, 18.75, 18.75, 18.75, 18.75, 18.75,
          -18.75, -18.75, -18.75, -18.75, -18.75,
          -18.75, -18.75, -18.75, -18.75, -18.75,
          -56.25, -56.25, -56.25, -56.25, -56.25,
          -56.25, -56.25, -56.25, -56.25, -56.25,
          -80.625, -80.625, -80.625, -90])

  def set_time(self, specified_time):
    self.current_time = specified_time
    decimal_hour = (self.current_time.hour + self.current_time.minute * 60 +
                    self.current_time.second * 3600)
#    decimal_day = self.current_time.timetuple().yday + decimal_hour / 24
    decimal_day = 164.0
    self.hour_angle = np.multiply((2 * math.pi / 24),
                                  np.divide(np.subtract(decimal_hour,
                                                        self.longitude),
                                            self.rotation_speed))
    self.solar_declination = (
        -math.asin(math.sin(
            math.radians(self.inclination_deg) *
                        math.cos(2 *
                                 (decimal_day + self.winter_solstice_offset) /
                                 self.length_of_year_in_days + 2 * self.ecc *
                                 math.sin(2 *
                                          (decimal_day + self.perigee_offset) /
                                          self.length_of_year_in_days) ))))
    
  def rotate(self, user):
    for j in range(1, 3):
#    while True:
      self.shine(user)
#      self.convect(user)
#      self.glow(user)
      self.display(user)
#       if user.paused:
#        with open('planet.txt', 'w') as outfile:
#          json.dump(jsonData, outfile, sort_keys = True,
#                    indent = 4, ensure_ascii=False)
        
  def display(self, user):
    for i in range(self.num_cells):
      print repr(self.latitude[i]).rjust (6), \
            repr(self.longitude[i]).rjust(6), \
            repr(round(self.solar_energy[i], 2)).rjust(6)
    print '\n'
    
  def shine(self, user):
    self.solar_elevation = np.arcsin(
        np.add(np.multiply(np.multiply(np.cos(self.hour_angle),
                                       np.cos(np.radians(self.latitude))),
                           math.cos(self.solar_declination)),
               np.multiply(math.sin(self.solar_declination),
                           np.sin(np.radians(self.latitude)))) )
    np.clip(self.solar_elevation, 0, math.pi, out=self.solar_elevation)
    self.solar_energy = np.multiply(
        (self.solar_constant * user.timestep * 3600),
        np.sin(self.solar_elevation))