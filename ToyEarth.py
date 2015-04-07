#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
import numpy as np
import json, io, sys, select, pdb, math
# enable debugging
import cgitb
cgitb.enable()
interface_output_type = 'web'

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
  noon_offset = 12
  num_cells = 48

  def __init__(self, specified_time = current_time):
    self.region_list = []
    self.solar_elevation = np.zeros(48)
    self.longitude = np.array([
          0, 120, -120, 0,
          108, 144, 180, -144, -108, -72, -36, 0, 36, 72,
          108, 144, 180, -144, -108, -72, -36, 0, 36, 72,
          108, 144, 180, -144, -108, -72, -36, 0, 36, 72,
          108, 144, 180, -144, -108, -72, -36, 0, 36, 72,
          120, -120, 0, 0])
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
    self.land_0 = np.array([
          [270.9, 0.25], [274.8, 0.25], [272.0, 0.25], [273.2, 0.25],
          [295.4, 0.25],
          [285.4, 0.25], [278.7, 0.25], [282.0, 0.25], [285.9, 0.25],
          [276.5, 0.25], [282.0, 0.25],
          [285.9, 0.25], [294.3, 0.25], [300.9, 0.25], 
          [304.3, 0.25],
          [304.3, 0.25], [303.2, 0.25], [302.0, 0.25], [300.9, 0.25],
          [303.2, 0.25], [300.9, 0.25],
          [313.7, 0.25], [305.4, 0.25], [304.3, 0.25], 
          [302.6, 0.25],
          [299.8, 0.25], [300.9, 0.25], [298.7, 0.25], [297.6, 0.25],
          [285.9, 0.25], [298.7, 0.25],
          [293.2, 0.25], [303.2, 0.25], [303.2, 0.25], 
          [266.5, 0.25],
          [263.7, 0.25], [269.3, 0.25], [274.3, 0.25], [273.7, 0.25],
          [270.9, 0.25], [273.2, 0.25],
          [273.2, 0.25], [273.7, 0.25], [273.2, 0.25], 
          [238.7, 0.25], [260.9, 0.25], [253.2, 0.25], [214.3, 0.25]])
    self.sea_0 = np.array([
          [270.9, 0.25], [274.8, 0.25], [272.0, 0.25], [273.2, 0.25],
          [295.4, 0.25],
          [285.4, 0.25], [278.7, 0.25], [282.0, 0.25], [285.9, 0.25],
          [276.5, 0.25], [282.0, 0.25],
          [285.9, 0.25], [294.3, 0.25], [300.9, 0.25],
          [304.3, 0.25],
          [304.3, 0.25], [303.2, 0.25], [302.0, 0.25], [300.9, 0.25],
          [303.2, 0.25], [300.9, 0.25],
          [313.7, 0.25], [305.4, 0.25], [304.3, 0.25],
          [302.6, 0.25],
          [299.8, 0.25], [300.9, 0.25], [298.7, 0.25], [297.6, 0.25],
          [285.9, 0.25], [298.7, 0.25],
          [293.2, 0.25], [303.2, 0.25], [303.2, 0.25],
          [266.5, 0.25],
          [263.7, 0.25], [269.3, 0.25], [274.3, 0.25], [273.7, 0.25],
          [270.9, 0.25], [273.2, 0.25],
          [273.2, 0.25], [273.7, 0.25], [273.2, 0.25],
          [238.7, 0.25], [260.9, 0.25], [253.2, 0.25], [214.3, 0.25]])
    self.region = np.array([
        # Temp, K Albedo Sea  Land
          [270.9, 0.25, 1.00, 0.00], 
          [274.8, 0.25, 0.80, 0.20], [272.0, 0.25, 0.75, 0.25],
          [273.2, 0.25, 0.75, 0.25],
          [295.4, 0.25, 0.10, 0.90],
          [285.4, 0.25, 0.40, 0.60], [278.7, 0.25, 0.90, 0.10],
          [282.0, 0.25, 0.65, 0.35], [285.9, 0.25, 0.15, 0.85],
          [276.5, 0.25, 0.45, 0.55], [282.0, 0.25, 0.95, 0.05],
          [285.9, 0.25, 0.60, 0.40], [294.3, 0.25, 0.05, 0.95],
          [300.9, 0.25, 0.08, 0.92],
          [304.3, 0.25, 0.40, 0.60],
          [304.3, 0.25, 1.00, 0.00], [303.2, 0.25, 1.00, 0.00],
          [302.0, 0.25, 1.00, 0.00], [300.9, 0.25, 0.25, 0.75],
          [303.2, 0.25, 0.80, 0.20], [300.9, 0.25, 1.00, 0.00],
          [313.7, 0.25, 0.00, 1.00], [305.4, 0.25, 0.12, 0.88],
          [304.3, 0.25, 0.50, 0.50],
          [302.6, 0.25, 0.88, 0.12],
          [299.8, 0.25, 0.50, 0.50], [300.9, 0.25, 0.99, 0.01],
          [298.7, 0.25, 1.00, 0.00], [297.6, 0.25, 1.00, 0.00],
          [285.9, 0.25, 0.44, 0.56], [298.7, 0.25, 0.72, 0.28],
          [293.2, 0.25, 1.00, 0.00], [303.2, 0.25, 0.60, 0.40],
          [303.2, 0.25, 1.00, 0.00], 
          [266.5, 0.25, 0.99, 0.01],
          [263.7, 0.25, 1.00, 0.00], [269.3, 0.25, 0.99, 0.01],
          [274.3, 0.25, 1.00, 0.00], [273.7, 0.25, 1.00, 0.00],
          [270.9, 0.25, 0.90, 0.10], [273.2, 0.25, 0.99, 0.01],
          [273.2, 0.25, 1.00, 0.00], [273.7, 0.25, 1.00, 0.00],
          [273.2, 0.25, 1.00, 0.00], 
          [238.7, 0.25, 0.01, 0.99],
          [260.9, 0.25, 0.20, 0.80],
          [253.2, 0.25, 0.10, 0.90],
          [214.3, 0.25, 0.02, 0.98]])
    self.water_albedo = np.array([1.00, # Full reflection at zero sun elevation
                    0.90, 0.83, 0.75, 0.67, 0.60, 0.53, 0.47, 0.42, 0.38, 0.35,
                    0.32, 0.30, 0.27, 0.24, 0.21, 0.19, 0.17, 0.16, 0.15, 0.13,
                    0.12, 0.11, 0.10, 0.10, 0.09, 0.08, 0.08, 0.07, 0.07, 0.06,
                    0.06, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04,
                    0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03,
                    0.03, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
                    0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
                    0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
                    0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02])

  def set_time(self, specified_time):
    self.current_time = specified_time
    self.decimal_hour = (self.current_time.hour +
                         self.current_time.minute / 60.0 +
                         self.current_time.second / 3600.0)
    self.decimal_day = (self.current_time.timetuple().tm_yday +
                        self.decimal_hour / 24)
    self.hour_angle = np.radians(self.longitude +
                                 (self.decimal_hour - self.noon_offset) *
                                 self.rotation_speed)
    self.solar_declination = (
        math.asin(math.sin(
             math.radians(self.inclination_deg) *
                        math.cos(2 * math.pi *
                                 (self.decimal_day +
                                  self.winter_solstice_offset) /
                                 self.length_of_year_in_days +
                                 2 * self.ecc *
                                 math.sin(2 * math.pi *
                                          (self.decimal_day +
                                           self.perigee_offset) /
                                          self.length_of_year_in_days) ))))
    
  def rotate(self, user):
    for j in range(1, 2):
      self.set_time(self.current_time + timedelta(0,user.timestep / 2.0))
      self.shine(user)
      self.set_time(self.current_time + timedelta(0,user.timestep / 2.0))
#      self.convect(user)
#      self.glow(user)
      self.display(user)
        
  def display(self, user):
    self.oldlat = 90
    if interface_output_type == 'terminal':
      print '\n', self.current_time, '\n'
      for i in range(self.num_cells):
        if self.latitude[i] != self.oldlat:
          print '\n'
          self.oldlat = self.latitude[i]
        print '{0:6.2f}'.format(self.solar_energy[i] / 1000000),
      print '\n'
    elif interface_output_type == 'web':
      print "Content-Type: text/html\n\n"
      print '<html>'
      print '<head>'
      print '<link rel="stylesheet" type="text/css" href="ToyEarth.css">'
      print('<link rel="stylesheet" type="text/css" href="//'
            'fonts.googleapis.com/css?family=Open+Sans:800" />')
      print '<title>ToyEarth</title>'
      print('<script src="http://'
            'ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js">')
      print '</script>'
      print '<script>'
      print '$(document).ready(function(){'
      print '    $("button").click(function(){'
      print '})'
      print '})'
      print '</script>'
      print '</head><body>'
      print '<table id="datamap"><colgroup><col width="107px"><col width="107px">'
      print '<col width="107px"><col width="107px"><col width="107px">'
      print '<col width="107px"><col width="107px"><col width="107px">'
      print '<col width="107px"><col width="107px"></colgroup><tr>'
      for i in range(self.num_cells):
        if self.latitude[i] != self.oldlat:
          self.oldlat = self.latitude[i]
          if (self.latitude[i] < 75) and (self.latitude[i] > -75):
            print '</tr><tr>'
          elif self.latitude[i] > 75:
            print '</tr><tr>'
          elif self.latitude[i] < -85:
            print '</tr><tr>'
          else:
            print '</tr><tr>'
        print '<td>{0:.2f} MJ</td>'.format(self.solar_energy[i] / 1000000)
      print '</tr></table>'
      print '</body></html>'
        
    
  def shine(self, user):
    self.solar_elevation = np.arcsin(
        np.add(np.multiply(np.multiply(np.cos(self.hour_angle),
                                       np.cos(np.radians(self.latitude))),
                           math.cos(self.solar_declination)),
               np.multiply(math.sin(self.solar_declination),
                           np.sin(np.radians(self.latitude)))) )
    np.clip(self.solar_elevation, 0, math.pi, out=self.solar_elevation)
    self.solar_energy = np.multiply(
        (self.solar_constant * user.timestep),
        np.sin(self.solar_elevation))
    self.sea_0[0:48, 1] = self.water_albedo[
      np.intp(np.rint(np.degrees(self.solar_elevation)))]

class User:
  timestep = 3600
  paused = False

Bill = User()
Earth = Planet()
Earth.rotate(Bill)
