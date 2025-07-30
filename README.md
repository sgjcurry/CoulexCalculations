# Safe-Coulex

Code to determine wether or not a Coulomb excitation experiment will be safe or unsafe. Output parameters include Clines safe distance, Minimum Distance of Approach between the projectile and target nuclei, and wether the collision will be safe or not. Input parameters are listed below. An output plot shows the distance of closest approach as a function of recoil particle detection angle. 

To Run directly:
```
python coulcalc.py
```

Inputs: 
```
Projectile mass number A_p: 
Projectile atomic number Z_p: 
Target mass number A_t: 
Target atomic number Z_t: 
Beam energy per nucleon (MeV/u): 
Minimum scattering angle (degrees): 
Maximum scattering angle (degrees): 
Logarithmic y-scale? (y/n): 
Y-axis maximum (fm): 
X-axis maximum (degrees): 
```
