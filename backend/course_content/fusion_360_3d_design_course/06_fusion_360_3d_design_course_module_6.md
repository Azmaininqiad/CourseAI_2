```markdown
# Module 6: Foundations of Parametric Design in Fusion 360

## Introduction  
Welcome to Module 6! Here, you’ll unlock the core principles of parametric 3D design. Unlike static modeling, **parametric design** lets you create intelligent, editable models by defining **dimensions**, **constraints**, and **relationships** between features. By the end, you’ll:  
✔️ Master sketch-based workflows  
✔️ Create 3D shapes from 2D sketches  
✔️ Design adaptive models that update dynamically  

---

## Topic 6.1: Parametric Modeling Fundamentals  

### What is Parametric Design?  
Parametric modeling uses **mathematical parameters** (e.g., dimensions, angles) to control geometry. Change a parameter → the entire model updates automatically.  

**Key Concepts**:  
- **Parameters**: Numeric variables (e.g., `Width = 50 mm`).  
- **Constraints**: Rules that govern geometry (e.g., "these lines must stay parallel").  
- **Feature Dependency**: Features (like holes or fillets) update when base sketches change.  

**Why Use Parametrics?**  
- **Design Flexibility**: Edit dimensions anytime without rebuilding.  
- **Error Reduction**: Constraints prevent invalid geometries.  
- **Efficiency**: Automate repetitive elements.  

### Practical Example: Smart Bracket  
Imagine designing a mounting bracket:  
1. Define `hole_diameter` and `bracket_thickness` as parameters.  
2. If you later change `bracket_thickness` from 5mm to 8mm:  
   - All holes/resize automatically.  
   - Mounting slots stay centered.  

🛠️ **Fusion 360 Workflow**:  
Parameters are managed in **Modify > Change Parameters**.  

```python
# Example: Defining parameters in Fusion 360  
# Access via ‘Modify’ tab > ‘Change Parameters’  
User Parameters:  
  bracket_thickness = 5 mm  # Edit this to update the entire model  
```

### 📺 Related Video: [Joints in Fusion 360: A Comprehensive Tutorial! FF117](https://www.youtube.com/watch?v=Bw08O6XsfDI)  
*Description: Learn how joints extend parametric principles to assemblies. This tutorial demonstrates constraint-based relationships between parts (Duration: 16:50 | Views: 334K+ | NYC CNC).*

---

## Topic 6.2: Sketch Creation & Editing  

### Creating Robust Sketches  
Sketches are 2D blueprints for 3D features. Follow these principles:  

**Critical Tools**:  
- **Line/Circle/Rectangle**: Basic shape tools.  
- **Constraints**: 
  - `Horizontal/Vertical` (🔗 lock orientation)  
  - `Coincident` (✅ join points)  
  - `Equal` (⬌ match sizes).  
- **Dimensions**: Assign numeric values with `D` hotkey.  

### Step-by-Tutorial: Constrained Sketch  
**Goal**: Draw a fully constrained wrench head.  
1. **Create Sketch**: Select XY plane → **Rectangle Tool** (hotkey `R`).  
2. **Add Constraints**:  
   - Apply `Equal` constraint to opposing sides.  
   - Use `Midpoint` constraint to center a circle.  
3. **Dimension**:  
   - Set `width = 30 mm`, `circle_diameter = 10 mm`.  
4. **Edit**: Double-click any dimension to modify → sketch updates.  

[IMAGE: Side-by-side: Unconstrained vs. constrained sketch]  

**Pro Tip**: A fully constrained sketch turns *blue* in Fusion 360. If *orange*, add more constraints!  

---

## Topic 6.3: From Sketch to 3D Model  

### Extrusion & Revolution  
Convert 2D sketches into 3D using:  
- **Extrude** (`E` hotkey): Pulls sketches into 3D volumes.  
- **Revolve**: Rotates a profile around an axis.  

### Tutorial: Create a Parametric Gear  
**Step 1: Sketch Gear Profile**  
- Draw a circle (`Diameter = 40 mm`).  
- Add teeth using **Line Tool** with `Equal` constraints.  

**Step 2: Extrude**  
- Select sketch → **Extrude** (`E`) → `Distance = 10 mm`.  
- Rename feature as `Gear_Base` in the timeline.  

**Step 3: Modify Parametrically**  
1. Open `Parameters` → Add `gear_thickness = 10 mm`.  
2. Edit `Extrude1` → Set distance to `gear_thickness`.  
3. Change `gear_thickness` to `15 mm` → Model updates instantly!  

```python
// Example: Fusion 360 Revolve for a Wheel  
1. Sketch half of a tire profile.  
2. Revolve Tool > Select profile + axis (centerline).  
3. Angle = 360° → Creates rotationally symmetric 3D shape.  
```

[IMAGE: Gear extrude vs. wheel revolve comparison]  

---

## Key Takeaways  
- 🎯 **Parametric design** uses rules/dimensions to create editable models.  
- 🔗 **Constraints** ensure sketches behave predictably.  
- ♻️ Always name features/timeline entries for easy editing.  
- ⚙️ **Extrude** and **Revolve** are foundational 3D tools.  

## Practice Exercises  
1. **Adaptive Keychain**:  
   - Create rectangle sketch with centered text.  
   - Add parameters for `length`, `width`, `text_size`.  
   - Change `length` → verify text resizes proportionally.  
2. **Parametric Cup**:  
   - Sketch a cup profile → **Revolve** at 360°.  
   - Add parameters for `height`, `diameter`, `wall_thickness`.  

## References & Further Reading  
- **Fusion 360 Help**: [Parameters & Constraints](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-4E8C4F90-8F44-47D0-8515-4CBC9BD43F94)  
- **Book**: *Parametric Design with Fusion 360* by Jesse Harrington  
- **Video**: "Mastering Sketch Constraints" (LinkedIn Learning)  
- **Video**: [Joints in Fusion 360: A Comprehensive Tutorial! FF117](https://www.youtube.com/watch?v=Bw08O6XsfDI) (Advanced constraint applications)  

---

## Visual Resources  
### 📺 Related Video: [Joints in Fusion 360: A Comprehensive Tutorial! FF117](https://www.youtube.com/watch?v=Bw08O6XsfDI)  
*Description: This video is a comprehensive tutorial on how to create and use Joints in Fusion 360! Traditional modeling requires 3 constraints. Learn to apply parametric principles to multi-part assemblies (Duration: 16:50 | Views: 334K+).*
```