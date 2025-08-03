```markdown
# Module 5: Assemblies and Motion in Fusion 360  
**Difficulty**: Beginner  
**Estimated Reading Time**: 12 minutes  

## Introduction  
Welcome to Module 5! Now that you've mastered basic modeling, we'll explore assembling multiple components and creating mechanical motion. Whether designing robotic arms or folding furniture, this module teaches how to combine parts using Joints, analyze movement, and manage complex assemblies. By the end, you'll turn static models into dynamic systems.  

---

### Topic 5.1: Creating and Managing Assemblies  
**Objective**: Learn to build multi-component designs using bodies and components.  

#### Key Concepts  
- **Components vs. Bodies**:  
  Components are independent objects (e.g., screws, gears). Bodies are shapes within a component (e.g., teeth of a gear). Tip: Always create new components for moving parts.  
- **Grounding**:  
  Fixes a component in place (right-click > Ground). Ground the base part first!  

#### Step-by-Step Tutorial: Gearbox Assembly  
1. **Insert Components**:  
   - Go to `Design > Insert > Insert into Current Design`.  
   - Import `Gear_1`, `Gear_2`, and `Baseplate` (created in Module 4).  
   ![Screenshot of Insert menu](https://via.placeholder.com/700x400?text=Insert+Menu+Screenshot+Fusion+360)  

2. **Position Components**:  
   - Use `Modify > Align` to roughly position gears.  
   - Select gear shafts and baseplate holes:  
   ```  
   Steps:  
   1. Click `Modify > Align`  
   2. Select gear shaft → baseplate hole  
   3. Repeat for all parts  
   ```  
   ![Aligned gears on baseplate](https://via.placeholder.com/700x400?text=Aligned+Gears+on+Baseplate)  

3. **Ground the Baseplate**:  
   Right-click `Baseplate` > `Ground`.  

---

### Topic 5.2: Applying Joints for Motion  
**Objective**: Use joints to define relationships and motion between components.  

#### Joint Types  
| Joint        | Use Case                | Example              |  
|--------------|-------------------------|----------------------|  
| **Revolute** | Rotation around an axis | Gears, hinges        |  
| **Slider**   | Linear movement         | Piston, drawer slides|  
| **Cylindrical**| Rotation + Slide       | Screw threads        |  

#### Practical Example: Rotating Gears  
1. **Apply Revolute Joint**:  
   - Navigate to `Assemble > Joint`.  
   - For `Gear_1`:  
     - **Motion Type**: Revolute  
     - **Component 1**: Select `Gear_1`’s shaft face  
     - **Component 2**: Select `Baseplate` hole face  

### 📺 Related Video: [Creating an assembly in Fusion 360](https://www.youtube.com/watch?v=O1p7Sn1eMmE)  
*Description: This video shows the first steps to combine components into one assembly, demonstrating component insertion, alignment, and grounding (5:02).*  

2. **Gear Connection**:  
   - Under `Motion` tab, select `Gear` relation.  
   - Set `Gear Ratio` (e.g., 2:1 for speed reduction).  
   ```  
   Pro Tip: Enable "Contact Sets" to detect collisions!  
   ```  

3. **Test Motion**:  
   Drag `Gear_1` to see `Gear_2` rotate.  

---

### Topic 5.3: Motion Study and Analysis  
**Objective**: Simulate and validate mechanical movement.  

#### Workflow: Animate an Assembly  
1. **Enter Motion Study**:  
   Switch workspace: `Workspace > Animation`.  

2. **Record Motion**:  
   - Click `Create Animation Storyboard`.  
   - Drag timeline slider → reposition components → add keyframes.  
   ![Animation timeline with keyframes](https://via.placeholder.com/700x400?text=Animation+Timeline+with+Keyframes)  

3. **Analyze Clearance**:  
   Use `Inspect > Analysis > Interference` to check collisions.  

#### Assembly Best Practices  
- **Naming**: Rename components (e.g., `Drive_Gear` instead of `Component1`).  
- **Subassemblies**: Group related parts (select parts → right-click → Create Subassembly).  
- **Degrees of Freedom (DOF)**: Verify excess DOF (unexpected movement) using `Assemble > Degrees of Freedom`.  

---

## Key Takeaways  
1. Components enable independent movement; bodies define shapes.  
2. `Revolute`, `Slider`, and `Cylindrical` joints cover 90% of mechanical motion.  
3. Always ground fixed parts first.  
4. Use motion studies to prevent real-world failures.  

## Practice Exercises  
1. **Assembly Challenge**:  
   Build a simple vise:  
   - Import `Base`, `Screw`, and `Jaw`.  
   - Use `Cylindrical` joint for screw rotation + linear motion.  

2. **Debugging Task**:  
   An assembly has overlapping gears. Use `Interference Analysis` to identify collisions and reposition parts.  

3. **Quiz**:  
   Q: What joint type lets a component rotate AND slide?  
   A: Cylindrical  

## Visual Resources  
### 📺 Videos  
- [Creating an assembly in Fusion 360](https://www.youtube.com/watch?v=O1p7Sn1eMmE) - Covers component insertion, alignment, and grounding (5:02).  

### 🖼️ Images  
- `Insert Menu Screenshot` (700×400)  
- `Aligned Gears on Baseplate` (700×400)  
- `Animation Timeline with Keyframes` (700×400)  

*Final course materials will replace placeholder images with high-resolution screenshots.*  

## References & Further Reading  
- **Fusion 360 Help**: [Joints and Motion](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-4E2B8F8E-5693-4F42-B6D4-E844B4C5CA92)  
- **Book**: *Mastering Autodesk Fusion 360* by Brian Culp (Chapter 8)  
- **Video**: "Advanced Assembly Techniques" (LinkedIn Learning)  
```