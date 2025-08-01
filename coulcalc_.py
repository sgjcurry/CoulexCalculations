#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

print("\n=== Coulomb Excitation Distance Calculator ===")


help_message = """
Usage: A_p Z_p A_t Z_t E_B theta_min theta_max [optional_flags]

Flags:
  A_p  [int]                 = Projectile mass number
  Z_p  [int]                 = Projectile atomic number 
  A_t  [int]                 = Target mass number 
  Z_t  [int]                 = Target atomic number
  E_B  [int]                 = Beam energy per nucleon in MeV/u
  Angle range  [int][int]    = COM scattering angle range in degrees

"""
optional_flags_message = """
Optional flags (default: '0'):
    [linear]            [bool]   = '1' for linear y-scale, '0' for logarithmic scale
    [safe angle]        [bool]   = '1' to determine safe angle range, '0' to skip
    [impact parameter]  [bool]   = '1' to calculate impact parameter information, '0' to skip

"""




# --- Loop until valid input ---
while True:
    user_input = input("Enter values ('h' for help, or 'o' for optional flags): ").strip()

    if user_input.lower() in ('h'):
        print(help_message)
        continue
    if user_input.lower() in ('o'):
        print(optional_flags_message)
        continue

    parts = user_input.split()
    if len(parts) < 7 or len(parts) > 10:
        print("\n[ERROR] Incorrect number of inputs.\n")
        continue

    try:
        A_p = int(parts[0])
        Z_p = int(parts[1])
        A_t = int(parts[2])
        Z_t = int(parts[3])
        E_B = float(parts[4])
        theta_min = np.radians(float(parts[5]))
        theta_max = np.radians(float(parts[6]))

        # Defaults
        linear_option = False
        angle_option = False
        b_option = False

        # Optional flags
        optional_flags = parts[7:]
        if len(optional_flags) > 0:
            linear_option = optional_flags[0] == '1'
        if len(optional_flags) > 1:
            angle_option = optional_flags[1] == '1'
        if len(optional_flags) > 2:
            b_option = optional_flags[2] == '1'
        break

    except ValueError:
        print("\n[ERROR] Invalid input types.\n")
        continue








# --- Nuclear radius function ---
def radius(A):
    return r0 * A**(1/3)

# --- Constants ---
r0 = 1.25
E_B_MeV = E_B * A_p
k = 1.44
R_p = radius(A_p)
R_t = radius(A_t)
dmin_theory = R_p + R_t + 5  # fm





def d_function(theta, Z_p, Z_t, A_p, A_t, E_B_MeV):
    d = 0.72 * ((Z_p * Z_t) / E_B_MeV) * ((A_p + A_t) / A_t) * (1 + (1 / np.sin(theta/2)))
    return d
def b_function(theta, d):
    b = (0.5 * d) / np.tan(theta / 2)
    return b



# distance of closest approach single equation using the theta max value
# to determine the minimum experimental distance of approach.
dmin_experimental = d_function(theta_max, Z_p, Z_t, A_p, A_t, E_B_MeV)


difference = abs(dmin_experimental - dmin_theory) / dmin_theory
diff_percent = difference * 100  # Convert to percentage

if dmin_experimental < dmin_theory:
    print("\n[WARNING] Unsafe Coulomb Excitation distance, consider adjusting parameters: \n"
          f"{difference:.2f} fm too close.\n"
          "- Reduce the maximum angular range\n"
          "- Decrease the beam energy\n"
          "- Or proceed with unsafe Coulex.\n")
elif diff_percent < 5:
    print(f"\n[CAUTION] Coulomb Excitation distance is just safe, {difference:.2f} fm margin.\n")
else:
    print(f"\n[OK] Safe Coulomb Excitation distance is maintained, {difference:.2f} fm margin.\n")


print(f"Experimental Minimum Distance of Approach = {dmin_experimental:.2f} fm")
print(f"Safe Minimum Distance of Approach = {dmin_theory:.2f} fm")






theta_arr_deg = np.linspace(1, 179, 1000)
theta_arr_rad = np.radians(theta_arr_deg)

# distance of closest approach function using the theta array values
# to determine the experimental distance of approach curve of values.
d = d_function(theta_arr_rad, Z_p, Z_t, A_p, A_t, E_B_MeV)
b = b_function(theta_arr_rad, d)



plt.figure(figsize=(8, 6))
plt.plot(theta_arr_deg, d, label='Projectile', color='red')
mask = (theta_arr_deg >= np.degrees(theta_min)) & (theta_arr_deg <= np.degrees(theta_max))
plt.fill_between(theta_arr_deg, d, dmin_theory, where=(d > dmin_theory) & mask, color='blue', alpha=0.2, label='Safe Region')
plt.axvline(x=np.degrees(theta_max), color='k', linestyle='--', label='Detector Range')
plt.axvline(x=np.degrees(theta_min), color='k', linestyle='--')
plt.axhline(y=dmin_theory, color='k', linestyle='-', label=f"Safe Distance: {dmin_theory:.2f} fm")
plt.plot([], [], ' ', label=f"Beam Energy = {E_B:.2f} MeV/u")
plt.xlabel('Scattering Angle $θ_{COM}$ (degrees)')
plt.ylabel('Distance of Approach (fm)')
plt.yscale('linear' if linear_option else 'log')
plt.xlim(0,179)
plt.ylim(10,1000)
plt.legend(frameon=0)
plt.tight_layout()







def d_of_theta(theta):
    return d_function(theta, Z_p, Z_t, A_p, A_t, E_B_MeV) - dmin_theory

    # finds the angle at which d = dmin_theory correspondinng to a safe angle. 
safe_angle = brentq(d_of_theta, 0.01, np.pi - 0.01)
b_safe = b_function(safe_angle, dmin_theory)

if angle_option:
    print(f"Safe maximum scattering angle: {np.degrees(safe_angle):.2f}°")
if b_option:
    print(f"Safe impact parameter b ≈ {b_safe:.2f} fm\n\n\n")


    def rutherford_equation(theta, Z_p, Z_t, E, k):
        dsigma_fmsr = ((Z_p * Z_t * k) / (4 * E))**2 / (np.sin(theta/2)**4)
        dsigma_barn = dsigma_fmsr / 100
        return dsigma_barn

    dsigma = rutherford_equation(theta_arr_rad, Z_p, Z_t, E_B_MeV, k)

    plt.figure(figsize=(8,6))
    plt.plot(theta_arr_deg, dsigma, color='red', label='Differential σ(θ)')
    plt.xlabel('Scattering Angle θ (degrees)')
    plt.ylabel('Differential Rutherford Cross-Section σ(θ) (b)')
    plt.axvline(x=np.degrees(theta_max), color='k', linestyle='--', label='Detector Range')
    plt.axvline(x=np.degrees(theta_min), color='k', linestyle='--')
    plt.yscale('log')
    plt.xlim(0, 180)
    plt.ylim(0.01,max(dsigma))
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

else:
    print("\n")

plt.show()
