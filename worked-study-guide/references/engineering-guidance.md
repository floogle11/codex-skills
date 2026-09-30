# Engineering derivation checks

Read the relevant subject notes, not all examples by default. These capture useful distinctions from previous guides; the assignment determines which models apply.

## Fluid mechanics

- Begin mass conservation with accumulation plus net outward mass flux. For a moving/deforming control volume, use velocity relative to the control surface in the flux. Constant plunger speed does not make a shrinking fluid inventory constant.
- Steady flow in a fixed control volume removes accumulation. Impermeable boundaries remove normal flux. A common constant density can cancel; different stream densities cannot. Adding mixture volume rates is an extra assumption, not a consequence of mass conservation alone.
- Average velocity suffices for mass flow by definition. Momentum flux generally needs the velocity-profile integral or a stated correction factor.
- In a moving control volume, mass crosses at relative velocity, but transported momentum uses absolute velocity. Define both frames.
- State Bernoulli's steady, incompressible, inviscid, along-a-streamline conditions and work/loss restrictions. Show which pressure, elevation, and velocity terms cancel. Do not use lossless Bernoulli through a dissipative hydraulic jump.
- Use signed momentum components and consistent pressure forces. Distinguish fluid force on hardware from anchor force. If width is absent in a two-dimensional problem, report force per unit width.

## Machine design and mechanics of materials

- Define coordinates and take moments from actual force position vectors before computing stress. Separate axial force, transverse force, torsion, and bending about both axes.
- Declare the cut-face convention. Wall reactions and resultants on the opposite face require opposite signs.
- Explain normal stress through section force/moment integrals and the elastic linear stress field; use centroidal symmetry to remove cross terms. Explain circular-shaft torsion through the torque integral and tangential stress field.
- Neglecting transverse shear does not remove bending caused by transverse forces or torsional shear.
- Evaluate bending at each point's coordinates. Resultant bending magnitude gives the extremum somewhere around the rim, not necessarily at a labeled point.
- Give signed shear components and magnitudes distinctly. Draw complementary shear and opposite-face directions consistently.
- For Mohr's circle, define the plotting convention; label face states, center, radius, principal intercepts, and maximum shear. Include the out-of-plane principal stress and sort all three. Label a symbolic schematic when an input is missing.

## Thermodynamics

- Define the system and signs before the first law. A fixed-mass piston-cylinder is closed even as its volume changes.
- Begin boundary work with delta W_b = P_boundary dV. Quasi-equilibrium mechanical motion allows system pressure in the integral. Derive constant-pressure or isothermal ideal-gas shortcuts from that integral.
- Keep V versus v, W versus w, and energy per mass versus total energy explicit. P-v area is specific work; P-V gives total work.
- Classify compressed liquid, saturated mixture, or superheated vapor before table lookup. Quality is vapor mass fraction, meaningful only in the two-phase region.
- Convert 'two-thirds of the initial liquid vaporizes' into phase masses before calculating final quality.
- Start the first law with relevant heat/work modes and changes in U, KE, and PE. Stirring can add internal energy without an endpoint change in bulk kinetic energy.
- Derive H = U + PV and dH = dU + P dV + V dP. Constant pressure removes V dP and combines boundary work with internal energy. Do not add boundary work again after using enthalpy. Heat equals delta H only when other work and KE/PE changes are absent.
- A freely moving, constant-load piston can justify constant pressure. State that model when wording gives only initial pressure; springs or stops may change the path.
- Include requested T-v and P-v diagrams, phase boundaries, endpoints, and arrows. A two-phase path at fixed pressure is isothermal; liquid warming and vapor superheating need not be. Label schematic domes and shade only the specified volume interval for work.
