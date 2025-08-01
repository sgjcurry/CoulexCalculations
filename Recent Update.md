# Update 0.1.1 (01.08.25)
# Summary of Major Changes & Additions

1. **Command-line style input with optional flags:**
   - All parameters input in a single line.
   - Added user help, and optional flag output descriptions.
   - Optional flags control linear/log y-scale, safe angle calculation, and impact parameter calculation.

2. **Modified input parsing:**
   - Cleaner logic with default flag values.
   - Separate help and optional flags messages.

3. **New calculations:**
   - Finds 'safe' max angle where experimental and theoretical dmin match.
   - Calculates impact parameter.
   - Optional plot of differential cross-section vs scattering angle.

4. Improved efficiency of code, and general small changes.
