<img width="881" height="916" alt="Screenshot 2026-07-29 230109" src="https://github.com/user-attachments/assets/59d5c781-f56a-4c49-bafe-7257480fd6a0" />


 
 
 ### **Orbital**
  
  Orbital is a 2D gravitational physics sandbox created entirely in Python using only standard library modules (turtle and tkinter). Orbits of the Orbitals, the planet-like bodies, are not hardcoded; they emerge dynamically from Newton’s Law of Universal Gravitation calculated between every single body frame-by-frame.

You can interactively slingshot planets into orbit, pan a camera infinitely around the universe using WASD if ur a gamer or using the Arrow keys, you can also increase the gravitational constant by clicking the 'G' key.

### Some bugs now squashed:
    
    The Coordinates Separation: Early on, a planet’s physics position was its drawing position. To build a panning camera, I had to decouple them—creating a 9-element list structure to track world coordinates privately while subtracting camera offsets only for rendering.
    
    The “Tunneling” Bug: Fast slingshotted planets would frequently phase straight through the central star between frames. I solved this by implementing Continuous Collision Detection (CCD)—using vector dot-product projection to check if the line segment traveled during a frame intersected the star.
    
    Singularity Prevention: As merging planets got really close, the gravity force equation approached divide-by-zero, creating infinite force that would sling bodies off screen at lightspeed. I had to write = logic to disable gravity between two bodies the exact frame they overlap.


### Some cool stuff:

    Conserving Density: When two bodies merge, the new object’s size is calculated using sqrt(r1² + r2²) rather than just adding the radii. This ensures area is conserved, keeping physical density mathematically consistent and real.
    
    Conservation of Momentum: If you launch two equal-mass planets head-on at the same speed, they will perfectly cancel out and stop dead in space upon impact, exactly as real-world physics dictates.

### What to know:

    Slingshot: Click, drag, and release to fling planets
    Navigation: Use WASD or Arrow keys to move around
    Rebuilding: Press R to wipe the board and start a clean universe.
    
    Even if you dont have python you can use the releases!



