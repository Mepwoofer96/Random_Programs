 ## Imports

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
    "saturn":  Body(mu=37941000,     r=58232,  mass=5.68*10**26,        a=9.5388,       color = 'xkcd:brownish yellow'),   
    "jupiter": Body(mu=126713000,    r=69911,  mass=1.9*10**26,         a=9.5388,       color = 'xkcd:brownish yellow'),
    "uranus":  Body(mu=5794500,      r=25362,  mass=8.68*10**25,        a=19.1914,      color = 'xkcd:purplish blue'),
    "neptune": Body(mu=6836500,      r=24622,  mass=1.02*10**26,        a=30.0611,      color = 'xkcd:ultramarine'),
    "pluto":   Body(mu=981.6,        r=1188,   mass=1.3*10**22,         a=39.5294,      color = 'xkcd:grey'),
}




# Functions

def au_to_km(au):
    return au*1.495979*10**8

def soi(mass2,mass1="sun"):
    b1 = bodies[mass1]
    b2 = bodies[mass2]

    return au_to_km(b2.a)*(b2.mass/b1.mass)**(2/5)

def vis_viva(mu, r, a):
    return np.sqrt(mu * (2/r - 1/a))

def orbital_period(planet):
    b = bodies[planet]
    return 2 * 3.14159 * (b.r**3 / b.mu)**0.5

def calc_orbit_e(planet,e,r_p):
    b = bodies[planet]
    r_p = r_p+b.r
    p = r_p*(1+e)
    if planet != "sun":
        r_soi = soi(planet)
    else:
        other_one = bodies["pluto"]
        r_soi = au_to_km(other_one.a)    
    
    if e != 0 or e >=1:
        soi_max = np.arccos(((p/r_soi)-1)/e)

    if e < 1:
        theta_star = np.linspace(0, 2*np.pi, 361)
        r_a = p/(1-e)

    elif e == 1:
        theta_star = np.linspace(-soi_max*.88, soi_max*.88, 361)

    elif e > 1:
        r_a = 0
        theta_star = np.linspace(-soi_max*.90, soi_max*.90, 361)
  
    r = p/(1+e*np.cos(theta_star))
    x = r*np.cos(theta_star)
    y = r*np.sin(theta_star)

    if e != 1 :
        a = p / (1-e**2)
        v_max = np.sqrt(b.mu*((2/r_p)-(1/a)))
    else : 
        v_max = np.sqrt(b.mu*(2/r_p))
    
    return x,y,v_max,r_a

def transfer_orbit(r_p, r_a, planet):
    b=bodies[planet]
    r_p += b.r
    if r_a < r_p:
        r_p, r_a = r_a, r_p

    a = (r_p + r_a) / 2
    e = r_a / a - 1
    p = a * (1 - e**2)

    theta_star = np.linspace(0, 2*np.pi, 361)
    r = p / (1 + e*np.cos(theta_star))
    x = r*np.cos(theta_star)
    y = r*np.sin(theta_star)
    v_a = np.sqrt(((2*b.mu)/r_a)-(b.mu/a))
    v_p = np.sqrt(((2*b.mu)/r_p)-(b.mu/a))

    return x, y, e, r_p, v_a, v_p

def transfer_dv(planet,r_a1,r_a2,r_p1,r_p2):
    mu = bodies[planet].mu
    r_start , r_end = r_p1,r_a2

    a1 = (r_p1+r_a1)/2
    a2 = (r_p2+r_a2)/2
    at = (r_start+r_end)/2

    dv1 = abs(vis_viva(mu, r_start, at) - vis_viva(mu, r_start, a1))
    dv2 = abs(vis_viva(mu, r_end,   a2) - vis_viva(mu, r_end,   at))
    return dv1, dv2, dv1 + dv2

def animattion(x,y):
    # Animation

    # padding so the orbiting object doesn't clip the edges
    pad = 0.1 * max(np.max(np.abs(x)), np.max(np.abs(y)))
    ax.set_xlim(np.min(x) - pad, np.max(x) + pad)
    ax.set_ylim(np.min(y) - pad, np.max(y) + pad)

    orbiter, = ax.plot([], [], 'o', color='red', markersize=6)

    def init():
        orbiter.set_data([], [])
        return orbiter,

    def update(frame):
        orbiter.set_data([x[frame]], [y[frame]])
        return orbiter,

    ani = FuncAnimation(
        fig, update, frames=len(x),
        init_func=init, interval=20, blit=True, repeat=True
    )

    plt.show()

def plot_1planet(planet,ax):
    b = bodies[planet]
    circle = plt.Circle((0, 0), radius=b.r, facecolor=b.color, edgecolor='black', linewidth=1)
    ax.add_patch(circle)
    return ax


def plot_orbit(ax,x, y, e, r_p):
    ax.plot(x, y, linewidth=1)
    ax.set_aspect('equal', adjustable='box')

    ax.text(x[0]*1.001, y[0]*1.15, "PE", fontsize=12, color="darkblue")
    ax.add_patch(plt.Circle((x[0], y[0]), radius=r_p*.05, facecolor="xkcd:hot pink"))

    if e < 1:
        ax.text(x[180]*.999, y[180]*1.15, "AP", fontsize=12, color="darkblue")
        ax.add_patch(plt.Circle((x[180], y[180]), radius=r_p*.05, facecolor="xkcd:lime green"))

    return fig, ax








## Mode select

select = 1
while select == 1 :

    print(" Welcome.\n Select Mode:\n 1. 1 Planet\n 2. 2 Planet")
    planet_n =int (input())
    mode = 1
    if planet_n == 1:
        print(" Select Orbits\n 1. 1 Orbit\n 2. 2 Orbit")
        mode =int (input())
        if mode == 1 or 2:
            select = 0

    elif planet_n == 2:
        select = 0
    else:
        print("Try again")




if mode == 1 and planet_n == 1 : ## Single orbit mode
# User inputs
    usr_planet=input("Planet (lowercase):")
    usr_e = float(input("Enter Eccentricity (e<3 and e>=0):"))
    usr_r_p = float(input("Radius of periapsis (do not include planet r, in Km):"))
    b = bodies[usr_planet]
    x,y,v,_ = calc_orbit_e(usr_planet ,usr_e ,usr_r_p)
    p = orbital_period(usr_planet)

    if usr_planet != "sun":
        s_oi = soi(usr_planet)
        print(f"soi = {s_oi}")
 
    print(f"V_max = {v}")
    print(f"Planet orbital period = {p}")
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    plot_orbit(ax, x, y, usr_e, usr_r_p)
    plot_1planet(usr_planet,ax)
    plt.show()


elif mode == 2: ## 2 orbit mode (Transfer orbit)
    usr_planet=input("Planet (lowercase):")
    usr_e1 = float(input("Enter Eccentricity 1 (e<1 and e>=0):"))
    usr_r_p1 = float(input("Radius of periapsis 1 (do not include planet r, in Km):"))
    usr_e2 = float(input("Enter Eccentricity 2 (e<1 and e>=0):"))
    usr_r_p2 = float(input("Radius of periapsis 2 (do not include planet r, in Km):"))
    b = bodies[usr_planet]
    x1,y1,v1,r_a1 = calc_orbit_e(usr_planet ,usr_e1 ,usr_r_p1)
    x2,y2,v2,r_a2 = calc_orbit_e(usr_planet ,usr_e2 ,usr_r_p2)
    xt,yt,et,r_pt,v_at,v_pt = transfer_orbit(usr_r_p1,r_a2,usr_planet)
    p = orbital_period(usr_planet)
    dv1,dv2,deltav = transfer_dv(usr_planet,r_a1,r_a2,usr_r_p1,usr_r_p2)

    
    
    if usr_planet != "sun":
        s_oi = soi(usr_planet)
        print(f"soi = {s_oi}")

    print(f"total Delta-v:{deltav}")
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    plot_orbit(ax, x1, y1, usr_e1, usr_r_p1)
    plot_orbit(ax, x2, y2, usr_e2, usr_r_p2)
    plot_orbit(ax, xt, yt, et, r_pt)
    plot_1planet(usr_planet,ax)
    plt.show()
elif mode == 3: ## Interplanetary mode
    twelve = 2






