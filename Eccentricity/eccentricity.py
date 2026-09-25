 ## Imports

import numpy as np

import matplotlib.pyplot as plt

from dataclasses import dataclass

@dataclass
class Body:
    mu: float
    r: float
    mass: float
    a: float
    color: str

bodies = {
    "sun":     Body(mu=132712440000, r=696000, mass=1.988416*10**30,    a=0,            color = 'xkcd:lemon yellow'),
    "earth":   Body(mu=398600,       r=6378,   mass=5.97*10**24,        a=1 ,           color = 'darkblue'),
    "moon":    Body(mu=4902.8,       r=1737,   mass=7.346*10**22,       a=0.0025718815, color = '0.8'),
    "mercury": Body(mu=22032,        r=2440,   mass=3.3*10**23,         a=.3871,        color = 'xkcd:tan'),
    "venus":   Body(mu=324860,       r=6052,   mass=4.87*10**24,        a=.7233,        color = 'xkcd:goldenrod'),
    "mars":    Body(mu=42828,        r=3390,   mass=6.42*10**23,        a=1.5273,       color = 'xkcd:dirty orange'),
    "jupiter": Body(mu=126713000,    r=69911,  mass=1.9*10**27,         a=5.2028,       color = 'xkcd:burnt siena'),
    "saturn":  Body(mu=37941000,     r=58232,  mass=5.68*10**26,        a=9.5388,       color = 'xkcd:brownish yellow'),
    "uranus":  Body(mu=5794500,      r=25362,  mass=8.68*10**25,        a=19.1914,      color = 'xkcd:purplish blue'),
    "neptune": Body(mu=6836500,      r=24622,  mass=1.02*10**26,        a=30.0611,      color = 'xkcd:ultramarine'),
    "pluto":   Body(mu=981.6,        r=1188,   mass=1.3*10**22,         a=39.5294,      color = 'xkcd:grey'),
}


def au_to_km(au):
    return au*1.495979*10**8

def soi(mass2,mass1="sun"):
    b1 = bodies[mass1]
    b2 = bodies[mass2]

    return au_to_km(b2.a)*(b2.mass/b1.mass)**(2/5)

     
    
def orbital_period(planet):
    b = bodies[planet]
    return 2 * 3.14159 * (b.r**3 / b.mu)**0.5

def calc_orbit(planet,e,r_p):
    b = bodies[planet]
    r_p = r_p+b.r
    p = r_p*(1+e)
    if planet != "sun":
        r_soi = soi(planet)
    else:
        other_one = bodies["pluto"]
        r_soi = other_one.r*2    
    
    if e != 0 :
        soi_max = np.arccos(((p/r_soi)-1)/e)

    if e < 1:
        theta_star = np.linspace(0, 2*np.pi, 361)

    elif e == 1:
        theta_star = np.linspace(-soi_max, soi_max, 361)

    elif e > 1:
        r_a = 0
        theta_star = np.linspace(-soi_max, soi_max, 361)
  
    r = p/(1+e*np.cos(theta_star))
    x = r*np.cos(theta_star)
    y = r*np.sin(theta_star)
    if e <= 1:
        r_a = r[180]

    a = (r_p+r_a)/2
    v_max = np.sqrt(b.mu*((2/r_p)-(1/a)))

    return x,y,v_max


usr_planet=input("Planet (lowercase):")
usr_e = float(input("Enter Eccentricity (e<3 and e>=0):"))
usr_r_p = float(input("Radius of periapsis (do not include planet r, in Km):"))
b = bodies[usr_planet]
x,y,v = calc_orbit(usr_planet ,usr_e ,usr_r_p)
p = orbital_period(usr_planet)

if usr_planet != "sun":
    s_oi = soi(usr_planet)
    print(f"soi = {s_oi}")
 


print(f"V_max = {v}")
print(f"Planet orbital period = {p}")

fig, ax = plt.subplots()
ax.plot(x, y)
circle = plt.Circle((0, 0), radius=b.r, facecolor=b.color, edgecolor='black', linewidth=1)

ax.add_patch(circle)
plt.gca().set_aspect('equal', adjustable='box') 

plt.show()


