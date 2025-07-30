import numpy as np
import matplotlib.pyplot as plt

# --- User input ---
print("\n=== Coulomb Excitation Distance Calculator ===")
A_p = int(input("Projectile mass number A_p: "))
Z_p = int(input("Projectile atomic number Z_p: "))
A_t = int(input("Target mass number A_t: "))
Z_t = int(input("Target atomic number Z_t: "))
E_B = float(input("Beam energy per nucleon (MeV/u): "))
E_B_MeV = E_B * A_p  # Convert to total beam energy
theta_min = np.radians(float(input("Minimum scattering angle (degrees): ")))
theta_max = np.radians(float(input("Maximum scattering angle (degrees): ")))
log_input = input("Logarithmic y-scale? (y/n): ").strip().lower()
log = log_input == 'y'
y_max = float(input("Y-axis maximum (fm): "))
x_max = float(input("X-axis maximum (degrees): "))

# --- Constants ---
r0 = 1.25
y_min = 0
x_min = 0

# --- Nuclear radius function ---
def radius(A):
    return r0 * A**(1/3)

R_p = radius(A_p)
R_t = radius(A_t)

# --- Minimum safe distance ---
d_min = R_p + R_t + 5  # fm

# --- Distance of closest approach ---
d_app = 0.72 * ((Z_p * Z_t) / E_B_MeV) * ((A_p + A_t) / A_t) * (1 + (1 / np.sin(theta_max/2)))

# --- Print results ---
diff_percent = abs(d_app - d_min) / d_min * 100

if d_app < d_min:
    print("\n[WARNING] Unsafe Coulomb Excitation distance, consider adjusting parameters: \n"
          "- Reduce the maximum angular range\n"
          "- Decrease the beam energy\n"
          "- Or proceed with unsafe Coulex.")
elif diff_percent < 5:
    print(f"\n[CAUTION] Coulomb Excitation distance is marginally safe ({diff_percent:.2f}%).")
else:
    print("\n[OK] Safe Coulomb Excitation distance is maintained.")

print(f"Cline's Safe Distance = {d_min:.2f} fm")
print(f"Minimum Distance of Approach = {d_app:.2f} fm")

# --- dmin function ---
def dmin_function(theta, Z_p, Z_t, A_p, A_t, E_B_MeV):
    d = 0.72 * ((Z_p * Z_t) / E_B_MeV) * ((A_p + A_t) / A_t) * (1 + (1 / np.sin(theta/2)))
    b = (0.5 * d) / np.tan(theta / 2)
    return b, d

# --- Angles array ---
theta_arr_deg = np.linspace(1, 179, 1000)
theta_arr_rad = np.radians(theta_arr_deg)
impact_param, d_projectile = dmin_function(theta_arr_rad, Z_p, Z_t, A_p, A_t, E_B_MeV)

# --- Plotting ---
plt.figure(figsize=(8, 6))
plt.plot(theta_arr_deg, d_projectile, label='Projectile', color='red')
mask = (theta_arr_deg >= np.degrees(theta_min)) & (theta_arr_deg <= np.degrees(theta_max))
plt.fill_between(theta_arr_deg, d_projectile, d_min, where=(d_projectile > d_min) & mask, color='blue', alpha=0.2, label='Safe Region')
plt.axvline(x=np.degrees(theta_max), color='k', linestyle='--', label='Detector Range')
plt.axvline(x=np.degrees(theta_min), color='k', linestyle='--')
plt.axhline(y=d_min, color='k', linestyle='-', label=f"Safe Distance: {d_min:.2f} fm")
plt.plot([], [], ' ', label=f"Beam Energy = {E_B:.1f} MeV/u")

plt.xlabel('Scattering Angle $θ_{COM}$ (degrees)')
plt.ylabel('Distance of Approach (fm)')

plt.yscale('log' if log else 'linear')
plt.ylim(y_min, y_max)
plt.xlim(x_min, x_max)
plt.legend(frameon=0)
plt.tight_layout()
plt.show()
