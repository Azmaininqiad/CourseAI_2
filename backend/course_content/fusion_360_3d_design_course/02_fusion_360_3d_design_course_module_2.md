```markdown
# Module 2: Core 3D Modeling Techniques in Fusion 360  
*Duration: 10-12 minutes (Beginner Level)*  

---

## Introduction  
Welcome to Module 2! In this module, you’ll transition from basic navigation to **hands-on 3D modeling**. We’ll cover sketching constraints, extrusion/revolve workflows, and parametric modifications—the foundational skills for creating precise designs. By the end, you’ll be able to turn 2D sketches into editable 3D objects.  

### 📺 Recommended Video: [Day 1 of Learn Fusion 360 in 30 Days for Complete Beginners! - 2023 EDITION](https://www.youtube.com/watch?v=d3qGQ2utl2A)  
*Description: Perfect companion to this module - covers interface basics, sketch tools, and constraint fundamentals. (13:07 min)*

---

## Topic 2.1: Sketching Fundamentals & Geometric Constraints  
### Why Constraints Matter  
Constraints are "rules" that define relationships between sketch elements (e.g., parallelism, perpendicularity). They ensure your designs remain stable during edits.  

### Key Constraint Types:  
1. **Horizontal/Vertical**: Forces lines to align with axes.  
2. **Coincident**: Snaps points to edges or other points.  
3. **Dimension**: Assigns numeric sizes (e.g., `10 mm`).  
4. **Equal**: Makes lines/circles identical in size.  

### Practical Tutorial: Constraining a Rectangle  
1. Create a rectangle with the *Rectangle* tool.  
2. Click the top edge → *Horizontal Constraint* (🔒 icon).  
3. Select adjacent edges → *Perpendicular Constraint*.  
4. Add a *Dimension Constraint*: Click opposite corners → Enter `50 mm`.  
![Constraint Workflow](placeholder_image_constraints.jpg)  

> 💡 **Tip**: Over-constrained sketches turn *red*. Delete redundant rules to fix errors.  

---

## Topic 2.2: Creating 3D Geometry – Extrude & Revolve  
### Extrude: Turning 2D → 3D  
Extrusion adds depth to sketches. Use it for parts like brackets or enclosures.  

#### Step-by-Step: Extruding a Cylinder  
1. Sketch a circle (Diameter = `30 mm`).  
2. Click *Create > Extrude*.  
3. Set parameters:  
   - **Distance**: `20 mm`  
   - **Operation**: *New Body*  
4. Click *OK*.  
```  
Extrusion Preview:  
Operation: New Body  
Distance: 20 mm  
Direction: Symmetric  
```  

### Revolve: Creating Rotational Symmetry  
Ideal for wheels, bottles, or bolts.  

#### Example: Designing a Cone  
1. Sketch a right triangle next to a vertical axis line.  
2. Select *Create > Revolve*.  
3. Pick the triangle → Select the axis → Set *Angle* to `360°`.  
![Revolve Demo](placeholder_image_revolve.gif)  

---

## Topic 2.3: Parametric Editing & Basic Modifications  
### Edit History & Timeline  
All actions appear in the bottom *Timeline*. Double-click any step to tweak parameters retroactively.  

### Essential Modify Tools:  
1. **Press Pull**: Adjust face heights dynamically (drag faces interactively).  
2. **Fillet**: Round edges (select edge → set radius to `5 mm`).  
3. **Combine**: Merge or cut bodies (e.g., *Union* two overlapping cubes).  

### Tutorial: Editing an Extruded Block  
1. Extrude a rectangle (`40x20 mm`, height `10 mm`).  
2. Double-click the extrusion in the Timeline → Change height to `15 mm`.  
3. Click *Press Pull* → Select top face → Drag upward by `5 mm`.  
![Parametric Edit](placeholder_image_timeline.jpg)  

> ⚠️ **Note**: Broken sketches? Use *Roll Back* in the Timeline to debug.  

---

## Key Takeaways  
1. Constraints ensure sketch stability.  
2. **Extrude** for linear depth; **Revolve** for rotational forms.  
3. Leverage the **Timeline** for parametric edits.  
4. *Press Pull* and *Fillet* are vital for fast iterations.  

---

## Practice Exercises  
1. Create a constrained sketch of a wrench profile (include 3 parallel lines).  
2. Extrude it to `8 mm` thickness.  
3. Use *Revolve* to model a chess pawn (base: circle, profile: curved line).  
4. Add fillets (`R=2 mm`) to soften edges.  

*Challenge*: Model a simple USB drive (combine extrusion for the body and revolve for the cap).  

---

## Further Reading  
- [Fusion 360 Sketch Constraints Guide](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-4E8C1F6D-4B8A-4A3C-9A3B-7A0AEC7B9A6A)  
- Book: *Parametric Modeling with Autodesk Fusion 360* (Chapter 4)  

### 📺 Video Tutorial: [Day 1 of Learn Fusion 360 in 30 Days for Complete Beginners! - 2023 EDITION](https://www.youtube.com/watch?v=d3qGQ2utl2A)  
*Description: Reinforces sketching fundamentals and extrusion workflows with practical examples. (Channel: Product Design Online)*  

---

## Visual Resources  
### Key Videos:  
- [Day 1 of Learn Fusion 360 in 30 Days for Complete Beginners!](https://www.youtube.com/watch?v=d3qGQ2utl2A) - Beginner-friendly workflow demonstration  

### Reference Images:  
- Constraint Workflow (`placeholder_image_constraints.jpg`)  
- Revolve Demonstration (`placeholder_image_revolve.gif`)  
- Parametric Editing (`placeholder_image_timeline.jpg`)  

---
*Next Module: Advanced Assemblies & Joints*  
```