# Coulex Calculation Code

This program calculates and visualizes the safe distance of closest approach in a Coulomb excitation experiment between a projectile and a target nucleus. Given inputs such as projectile and target masses, charges, beam energy, and scattering angle range, it determines whether the experimental setup maintains a safe distance to avoid nuclear contact. It also optionally computes and plots the Rutherford scattering differential cross-section and impact parameter related to the scattering angles, helping users understand the interaction dynamics and experimental constraints.

To Run directly in terminal:
```
python coulcalc.py
```
or using a command line tool:
```
mv coulcalc.py COMMAND
```
execute
```
chmod +x COMMAND
```
move to PATH
```
sudo mv COMMAND PATH
```
to run anywhere:
```
COMMAND
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
```
