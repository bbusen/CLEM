def shine(time_is, timestep=1):
	hr_angle_rad = pi * (gmt - longitude  / 15)  / 12
	term1 = 2 * (time_is.timetuple().yday + 10) / Earth.loy
	term2 = 2 * Earth.ecc * sin( 2 * ( time_is.timetuple().yday - 2 ) / Earth.loy )
	solar_declination = -asin(Earth.sin_incl * cos(term1 + term2))
