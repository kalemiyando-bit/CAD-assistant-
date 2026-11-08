# ROBOT CONCEPT — ENGINEERING DESIGN AND SOLIDWORKS MODELLING BRIEF

**Document purpose:** Master submission brief for an AI engineering/design agent  
**Project stage:** Concept definition completed; begin preliminary engineering design and first SolidWorks models  
**Prototype version:** Version 1 (V1)  
**Units:** Millimetres (mm), kilograms (kg), seconds (s), unless stated otherwise

---

# 1. YOUR ROLE AND OVERALL ASSIGNMENT

Act as a multidisciplinary engineering design team consisting of:

- A senior mechanical design engineer
- A mobile robotics engineer
- A mechatronics and control systems engineer
- An industrial/product designer
- A manufacturing engineer
- A technical illustrator and engineering documentation specialist

Your task is to help develop a practical, mechanically coherent, manufacturable small mobile service robot. The robot is a skills-development and concept-demonstration project that will be modelled and assembled in **SolidWorks**.

I need more than attractive concept images. I need engineering sketches, dimensioned drawings, component breakdowns, mechanical explanations, design calculations, assembly relationships and clear instructions that I can follow to create the 3D models myself.

The design must be realistic for a student-built prototype. Prioritise:

1. Mechanical simplicity
2. Affordability and availability of components
3. Manufacturability using common workshop processes
4. Reliability and safe operation
5. Ease of assembly, adjustment and maintenance
6. A compact footprint suitable for indoor environments
7. A design that can be expanded in later versions

Do not design a large industrial warehouse robot. Do not add complexity merely to make the robot look advanced.

**Important:** This is an engineering design task. Do not invent dimensions, motor specifications, gear sizes, load ratings or component capabilities and present them as verified facts. Clearly distinguish between:
- User-provided requirements
- Preliminary design targets
- Your engineering recommendations
- Assumptions requiring calculation or testing
- Dimensions that remain to be determined

If a design decision is uncertain, explain the uncertainty and recommend a practical way to resolve it.

---

# 2. PROJECT PURPOSE AND OPERATING ENVIRONMENT

The robot is intended as a small indoor service and material-handling prototype for:

- Homes
- Small retail stores
- Hospitals and similar indoor facilities

Potential future functions include carrying items, collecting or picking up objects, sorting/packing, stock counting and interacting with an operator.

The V1 prototype is intended to demonstrate the concept and develop practical engineering skills. It is not intended for heavy industrial use, large warehouses or heavy manufacturing environments.

Design for:
- Indoor, generally level floors
- Corridors, rooms, retail aisles and hospital spaces
- Human-accessible environments
- Doorway and turning constraints
- Low-to-moderate payloads
- Slow, controlled movement
- Simple maintenance and accessible components

A future version may be expanded for larger companies, warehouses and heavier loads. Do not design those future capabilities into V1 unless doing so does not add unnecessary cost or complexity.

A ceiling-mounted rail concept has been considered for a possible future version, but **it is not part of the current V1 prototype**.

---

# 3. OVERALL ROBOT ARCHITECTURE

Organise the robot into three main physical sections:

## 3.1 Lower chassis and mobility section

This contains:
- Main structural frame
- Four-wheel mobility system
- Drive motors and transmission
- Battery
- Motor controllers
- Main power distribution
- Relevant sensors
- Mounting points for the loading mechanism

## 3.2 Internal equipment and electronics compartment

This contains:
- Microcontroller or onboard computer
- Motor drivers/controllers
- Battery and power electronics, as appropriate
- Sensor interfaces
- Wiring and cable management
- Communication electronics
- Other control components

The compartment must provide:
- Protection for electronics
- Access for maintenance
- Ventilation where required
- Secure mounting
- Cable routing and strain relief
- Separation from moving mechanical components

## 3.3 Upper carrying tray/platform

The upper tray is the robot's carrying surface and also forms part of its upper structure/enclosure.

It must:
- Support the intended payload
- Prevent objects from sliding off during movement
- Be easy to load and unload
- Have suitable edges, lips or dividers
- Transfer its load into the chassis through a sound structural arrangement

Check the tray's support structure and the effect of its payload on the robot's centre of gravity.

---

# 4. PRELIMINARY V1 DIMENSIONS AND PERFORMANCE TARGETS

Use the following as **initial design targets**, not certified or fully validated specifications. Check whether they are mutually compatible and recommend changes where calculations show they are unsuitable.

| Parameter | Preliminary V1 target |
|---|---:|
| Main chassis length | 800 mm |
| Main chassis width | 450 mm |
| Chassis structural height | 250–300 mm |
| Ground clearance | 30 mm |
| Drive wheel diameter | Approximately 150 mm |
| Drive wheel track / spacing | Investigate 380–400 mm where applicable |
| Passive wheel/caster diameter | Investigate 75–100 mm where applicable |
| Upper tray size | Approximately 600 × 400 mm |
| Tray height above floor | Approximately 700–900 mm |
| Overall robot height | Approximately 900–1000 mm |
| Target robot mass | Approximately 30–40 kg |
| Maximum tray payload | Target 15 kg |
| Normal individual object lifting capacity | Target 3 kg |
| Maximum individual lifted object | Target 5 kg |
| Maximum combined carried payload | Target 15 kg |
| Maximum initial object size | Approximately 300 × 300 × 250 mm |
| Maximum speed | Target 0.6 m/s |
| Normal operating speed | Target 0.3–0.4 m/s |
| Runtime | Target 2–3 hours |
| Maximum floor gradient | Initial target 3° |
| Small threshold capability | Investigate 10–15 mm |
| Turning circle | Target approximately 920 mm, subject to validation |

Additional layout considerations:
- Target doorway compatibility: consider typical home doors around 760–810 mm and wider hospital doors.
- Investigate a practical turning envelope for narrow corridors and retail aisles.
- Use rounded external corners where practical; a 5 mm minimum corner radius is an initial target.
- Keep sensors and mechanical parts protected from accidental impact.
- Check the actual overall width, including wheels, bumpers, attachments and protrusions. The chassis width alone is not the robot's full width.

**Payload distinction:** The tray payload, the weight of an individual object lifted by the shovel and the combined carried payload are different design cases. Do not treat them as interchangeable. Check the robot under combined loading and during front-loader extension.

---

# 5. MOBILITY SYSTEM — FOUR-WHEEL ARRANGEMENT

The current user direction is:

- Four wheels in total.
- One drive mechanism associated with a front wheel and one drive mechanism associated with a rear wheel.
- The other two wheels are passive.
- The wording describes one powered wheel at the front and one powered wheel at the rear. Preserve this requirement as the starting concept; do not silently replace it with a conventional two-central-drive-wheel layout.

The precise geometry and steering method still require engineering development.

## 5.1 Required investigation

Develop a clear wheel-layout proposal and establish:
- Which side of the robot each powered wheel occupies
- Exact front/rear positions
- Whether the powered wheels are independently controlled
- How the passive wheels are mounted
- Whether passive wheels are fixed, swivelling or caster-type
- How the robot steers and turns
- Whether the proposed arrangement can turn in confined indoor spaces
- Whether the wheels scrub, bind or fight each other during turns
- How the drive wheels maintain traction when the front shovel is lifting a load
- How the robot remains stable with an empty tray, loaded tray and extended loader

Do not assume that placing one powered wheel at the front and another at the rear automatically provides practical steering. Evaluate the kinematics and propose a workable configuration. If the intended layout is mechanically unsuitable, explain why and provide the closest practical alternative for the user's approval.

## 5.2 Drive power path

The initial drive concept is:

**Battery → motor controller → electric motor → three-gear reduction train → wheel**

Develop a simple, practical three-gear arrangement where appropriate.

For the gear train, specify and illustrate:
- Gear arrangement and gear sequence
- Number of teeth for each gear
- Module
- Pitch diameter
- Centre distance
- Gear face width
- Shaft diameters
- Bearings and supports
- Reduction ratio
- Input and output speed
- Output torque
- Gear material and manufacturing method
- Direction of rotation
- Mounting and lubrication considerations

Calculate the ratio and check tooth geometry, strength and packaging. Do not choose arbitrary gear dimensions just to fill a drawing.

If a different transmission is more practical for V1, explain the trade-offs and retain the three-gear concept as the requested baseline for comparison.

---

# 6. LOADING MECHANISM — PIVOTING SHOVEL AND HOOK/LOADER

The V1 loading mechanism should be a simple front-mounted, pivoting loader rather than a complex multi-joint industrial robotic arm.

The shovel should follow an **arc** as it rises, similar to a small front-end loader.

The concept includes:
- Fixed mounting structure on the chassis
- Pivoting loader arms
- Shovel/bucket-like attachment
- Retaining hook or lip to stop objects sliding off
- Motor-driven chain or cable hoisting mechanism
- Winch drum
- Pulleys or sprockets as appropriate
- Pivot shafts, pins and bearings
- Mechanical travel stops
- Load measurement provision

## 6.1 Chain/cable lifting concept

The user's preferred concept is a traditional slow, manageable lifting arrangement: a motor pulls a rope/chain to raise the loader, similar in principle to older mechanical hoisting systems.

Investigate a practical arrangement using:
- Geared electric motor
- Winch drum
- Suitable rated chain or steel cable
- Correctly sized pulleys or sprockets
- Secure end attachments
- Guided routing that prevents the line from slipping off
- A mechanical brake or self-locking arrangement
- Mechanical travel limits

Show exactly how the chain/cable pulls the loader arms and how the force is transferred through the pivots into the chassis.

**Safety requirement:** Do not rely on ordinary rope, friction alone or motor holding torque alone to keep a raised load from falling. Include a suitable load-retention/braking method and a safe response to power loss. Select rated lifting components and calculate the loads, including appropriate safety factors.

## 6.2 Shovel and retaining feature

The shovel should be suitable for initial floor-level pickup.

Develop a simple attachment with:
- A low leading edge that can approach and slide under or support an object
- A rear retaining lip/hook
- Sufficient width and depth for the intended object range
- Rounded or protected edges where appropriate
- A practical mounting interface so the shovel can be removed or adjusted

Consider the different shapes of:
- Small boxes
- Sacks
- Bottles

A single flat shovel may not safely handle all three object types. Recommend a practical V1 shovel and identify whether simple interchangeable attachments or a retaining cradle are needed. Do not overcomplicate the first prototype.

## 6.3 Lifting and depositing sequence

Illustrate and explain the intended operating sequence:

1. Robot approaches an object.
2. Shovel is positioned near floor level.
3. Leading edge moves under or supports the object.
4. Retaining lip/hook helps secure it.
5. Winch slowly pulls the chain/cable.
6. Loader arms pivot and raise the shovel along an arc.
7. The mechanism pauses at a stable position.
8. Load is measured.
9. If acceptable, the shovel rises to the tray level.
10. The shovel tilts or releases the object onto the tray.
11. The mechanism returns to its starting position.

Explain how the shovel tilts. If a second actuator or mechanical linkage is required, show the simplest practical solution.

The initial version should prioritise **floor-level pickup**. You may investigate pickup from low surfaces up to approximately 300 mm only if it can be achieved affordably without compromising the basic mechanism. Treat this as an optional capability, not a mandatory V1 feature.

## 6.4 Load measurement

The concept includes measuring the weight of an object while it is being lifted.

Investigate placing a load cell in the force path between the shovel/attachment and lifting structure, or another mechanically valid location.

Explain:
- Where the load cell is installed
- How the load reaches the sensor
- How the attachment's own mass is tared
- How the system avoids misleading measurements caused by friction, acceleration or mechanical binding
- Why a stationary pause after lifting is preferable for the first version
- How an overweight object is rejected or returned safely

Do not claim that a load cell reading during motion is automatically the true object mass. Explain calibration and measurement limitations.

---

# 7. SENSORS, NAVIGATION AND OPERATOR INTERFACE

The robot's intended future functions include:
- Line following
- Obstacle detection and avoidance
- Object/package identification
- Sorting and packing
- Stock counting
- Operator communication

For V1, identify which functions can realistically be demonstrated and which should remain future enhancements.

## 7.1 Smartphone mounting

A smartphone is intended to be mounted at the front of the robot.

It may be used for:
- Camera-based vision experiments
- Object recognition experiments
- Navigation experiments
- Operator communication
- Flashlight/illumination for low-light testing

Design a secure adjustable phone mount:
- Stable under robot vibration
- Adjustable viewing angle
- Protected from accidental impacts
- Accessible for removing the phone
- Positioned so the camera has a useful field of view
- Not obstructing the loader or sensors

Do not assume that the phone alone replaces all required control hardware.

## 7.2 Sensors

Investigate practical sensor positions and mounting arrangements for:
- Line-following sensor array
- Obstacle detection sensors
- Proximity sensors
- Object detection camera
- Load measurement
- Wheel encoders or speed feedback, if required

Initial layout targets:
- Line sensor array approximately 8–12 mm above the floor
- Sensor array width approximately 80–100 mm
- Obstacle sensors around 150 mm above the floor as an initial placement to investigate

Check field of view, blind spots, sensor protection and interference with the loader.

## 7.3 Human-machine interface

Include a simple operator interface:
- LCD or suitable small display
- Physical buttons
- Clear status indication
- Emergency stop
- Basic operator feedback

Show where the interface is mounted and how it can be accessed.

A desktop application may be considered for future monitoring, configuration and communication. Do not let software features distract from completing the mechanical V1 design.

---

# 8. CHASSIS, FRAME, TRAY AND ENCLOSURE

## 8.1 Chassis frame

Investigate a practical frame using:
- 30 × 30 mm aluminium extrusion as an initial frame option
- Crossmembers at approximately 250–300 mm spacing as an initial layout target
- Approximately 3 mm aluminium deck plate as an initial option

Check whether these choices are strong enough for:
- Robot self-weight
- Tray payload
- Loader forces
- Drive motor reaction loads
- Vibration and repeated use

Recommend alternative materials or sections if calculations justify them.

Provide:
- Frame layout
- Crossmember positions
- Plate thickness
- Fastener sizes and locations
- Motor mounting plates
- Loader mounting reinforcements
- Electronics mounting points
- Battery restraint
- Access panels

## 8.2 Tray

Initial target: approximately 600 × 400 mm, with a carrying surface approximately 700–900 mm above the floor.

Design:
- Supporting structure
- Raised edges or retaining lips
- Non-slip surface or other practical anti-slip solution
- Safe loading/unloading access
- Load transfer into the chassis

The tray is relatively large compared with the chassis. Check overhang, support, bending and tipping risk. Do not assume the tray dimensions are final if they compromise stability.

## 8.3 Enclosure

Provide a compact enclosure for the electronics and battery while keeping:
- Moving mechanisms separated
- Ventilation where needed
- Wiring accessible
- Maintenance straightforward
- Sharp edges and pinch points protected

The final external form should be compact, approachable and suitable for homes, small shops and hospitals.

---

# 9. ENGINEERING CALCULATIONS AND DESIGN VERIFICATION

Do not proceed by appearance alone. Perform preliminary calculations and explain the assumptions.

At minimum, investigate:

## 9.1 Mobility
- Required wheel torque
- Motor speed
- Gear reduction ratio
- Acceleration and braking
- Maximum speed
- Gradient capability
- Traction and normal force on each wheel
- Turning behaviour and wheel scrub
- Battery capacity and runtime estimate

## 9.2 Stability
- Centre of gravity when empty
- Centre of gravity with tray payload
- Centre of gravity with shovel extended
- Centre of gravity while lifting the maximum object
- Support polygon
- Forward, rearward and lateral tipping margins
- Drive wheel traction during lifting

## 9.3 Loader
- Object weight and load cases
- Loader arm geometry
- Pivot reactions
- Chain/cable tension
- Winch drum torque
- Motor torque and reduction
- Pulley/sprocket loads
- Shaft and pin sizing
- Bearing selection
- Deflection and structural strength
- Brake or load-retention requirements
- Mechanical travel limits

## 9.4 Structure
- Chassis bending and torsion
- Tray deflection
- Loader mounting loads
- Fastener loading
- Local reinforcement
- Material suitability

## 9.5 Measurement
- Load-cell capacity and location
- Calibration approach
- Tare procedure
- Static weighing accuracy limitations
- Effects of motion and friction

Use appropriate engineering equations and show worked calculations. State when detailed analysis, supplier data or physical testing is still required.

---

# 10. REQUIRED ENGINEERING DRAWINGS AND VISUAL OUTPUTS

Generate a coherent drawing set. Each drawing must have a clear purpose and be consistent with the same robot design.

Required overall drawings:
1. Overall isometric concept view
2. Front elevation
3. Side elevation
4. Top/plan view
5. Rear view where useful
6. Chassis frame drawing
7. Wheel arrangement and underside view
8. Drive motor and transmission arrangement
9. Three-gear reduction train drawing
10. Internal equipment layout
11. Battery and electronics mounting layout
12. Loader assembly side view
13. Loader assembly front view
14. Pivot and bearing detail
15. Chain/cable and winch routing drawing
16. Shovel and retaining lip detail
17. Load-cell installation detail
18. Upper tray drawing
19. Smartphone mount drawing
20. Sensor placement drawing
21. Full exploded assembly
22. Assembly sequence illustrations

For mechanisms, show movement positions and motion direction. Include a clear explanation of how the mechanism works.

## 10.1 Dimensioning requirements

Add dimensions to sketches and technical drawings wherever possible.

Use:
- Millimetres
- Clear dimension lines and extension lines
- Centre lines
- Hole and shaft callouts
- Diameters and radii
- Centre distances
- Angles
- Thicknesses
- Fits and tolerances where relevant
- Material and manufacturing notes

Do not clutter concept illustrations with too many dimensions. Use separate detailed drawings and dimension schedules.

**Critical accuracy rule:** AI-generated text and dimensions inside images can be distorted or incorrect. A separate written dimension schedule and engineering calculation must take precedence over any dimension labels rendered in an image. Never treat an image-generated dimension as verified merely because it appears on a drawing.

Clearly label dimensions as:
- Preliminary
- Calculated
- Supplier-dependent
- To be confirmed
- Finalised after prototype testing

Use recognised engineering drawing conventions and sensible orthographic projection. Keep views consistent.

---

# 11. COMPONENT-BY-COMPONENT DOCUMENTATION

Every major assembly and component must have a written description.

For each image or drawing generated, provide the following directly underneath it:

1. **Drawing title**
2. **Purpose:** What the component or assembly does
3. **Description:** What is shown and how it is arranged
4. **Component breakdown:** Names and functions of the visible parts
5. **How it works:** Mechanical operation or motion
6. **Dimensions:** Dimension schedule, including units and status
7. **Connections:** How it attaches to neighbouring components
8. **Materials:** Recommended material and reason
9. **Manufacturing:** Practical manufacturing method
10. **SolidWorks modelling guidance:** Suggested features and modelling sequence
11. **Assembly guidance:** How parts fit together
12. **Engineering considerations:** Loads, clearances, safety, tolerances and unresolved issues

Do not provide an image without explaining it. Do not provide a component name without explaining its function.

---

# 12. SOLIDWORKS MODELLING WORKFLOW

Develop the design in a logical order so that the parts can be modelled and assembled progressively.

Recommended modelling sequence:

1. Overall layout and master dimensions
2. Main chassis frame
3. Deck plate and structural crossmembers
4. Four-wheel layout
5. Wheel and hub models
6. Motor and transmission mounting
7. Gear train, shafts and bearings
8. Battery and electronics compartment
9. Loader mounting frame
10. Loader arms
11. Pivot shafts, pins and bearings
12. Winch motor and drum
13. Chain/cable routing and pulleys/sprockets
14. Shovel and retaining feature
15. Load-cell mounting
16. Upper tray and supports
17. Smartphone mount
18. Sensor brackets
19. Enclosure and access panels
20. Complete robot assembly

For each part, explain the recommended SolidWorks approach. For example:
- Sketch planes and reference geometry
- Extruded boss/base
- Extruded cut
- Revolved boss/cut
- Sweep and loft where appropriate
- Hole Wizard
- Patterns and mirrors
- Fillets and chamfers
- Mates and subassemblies
- Motion studies for mechanisms

Use a top-down/master-layout approach where it improves alignment and consistency. Identify parts that should be modelled as standard purchased components rather than custom-designed parts.

Provide practical file and folder naming conventions. Keep part names, assembly names and drawing names consistent.

---

# 13. EXPLODED VIEWS, ASSEMBLY AND MOTION

For each major subsystem, produce:
- Exploded view
- Parts list/BOM
- Item numbers
- Assembly order
- Fastener and bearing details
- Motion explanation
- Maintenance access considerations

For motion demonstrations, show:
- Wheel rotation and steering
- Gear train rotation
- Loader arm pivoting
- Winch drum rotation
- Chain/cable movement
- Shovel lift arc
- Shovel tilt/release
- Complete pickup and depositing sequence

Make sure the moving components do not pass through the chassis, tray, wheels, enclosure or one another.

---

# 14. VIDEO GENERATION PROMPTS

For every major mechanism, provide a separate, ready-to-copy prompt that can be used in a video-generation AI.

Each video prompt must state:

- What mechanism is being demonstrated
- The exact starting configuration
- Camera position and view
- Which components move
- The direction and sequence of movement
- What remains stationary
- The mechanical relationship between parts
- The intended end position
- Desired duration and visual style
- Requirements for mechanical continuity and consistent geometry

The video should explain the mechanism, not merely show a cinematic robot animation.

Use realistic engineering animation:
- Plain or neutral background
- Clear component visibility
- Smooth, slow motion
- Useful camera angles
- No decorative science-fiction effects
- No unexplained component changes between frames

Keep the robot's geometry, wheel count, component positions and colours consistent across all images and videos.

---

# 15. SUBSYSTEM-BY-SUBSYSTEM COMPLETION

Do not stop after generating an overall robot concept. Work through the complete design, subsystem by subsystem.

At minimum, cover:
1. Chassis and structural frame
2. Four-wheel mobility system
3. Drive motors and transmission
4. Battery and power distribution
5. Electronics compartment
6. Navigation and sensors
7. Loader mounting structure
8. Pivoting loader arms
9. Chain/cable winch mechanism
10. Shovel and retaining feature
11. Load measurement
12. Upper tray
13. Smartphone mount
14. Human-machine interface
15. Enclosure and protective features
16. Complete assembly and integration

Break complex mechanisms into individual components. Do not hide important mechanical details inside a single opaque assembly.

Maintain a progress tracker using:
- NOT STARTED
- IN PROGRESS
- COMPLETED
- REQUIRES ENGINEERING VALIDATION

If you reach an output or context limit, record:
- What has been completed
- What remains
- Important design decisions
- Current dimensions and assumptions
- The next exact task

Then continue from that point when possible. Do not unnecessarily restart completed work or change already agreed design decisions without explaining why.

---

# 16. DESIGN COORDINATION, SAFETY AND PROTOTYPE READINESS

Maintain a requirements register and an assumptions register.

## 16.1 Requirements register

Track each requirement, its target value, source, verification method and status.

## 16.2 Interface register

Document interfaces between:
- Chassis and wheel modules
- Motors and gearboxes
- Shafts and bearings
- Loader arms and chassis
- Winch and chain/cable
- Shovel and loader arms
- Load cell and lifting structure
- Tray and chassis
- Electronics and sensors
- Battery and power distribution

Record mounting dimensions, bolt patterns, shaft sizes, clearances and cable routes.

## 16.3 Safety

Identify:
- Pinch and crush points
- Exposed gears and chains
- Falling-load hazards
- Unexpected robot movement
- Electrical short-circuit and battery risks
- Sharp edges
- Overturning risks
- Emergency stopping
- Safe maintenance and isolation

Include guards and protective covers where appropriate. Ensure the loader cannot freely descend following power loss.

## 16.4 Prototype testing plan

Prepare practical tests for:
- Static chassis loading
- Tray loading
- Wheel traction
- Turning and manoeuvring
- Threshold crossing
- Braking and stopping
- Loader lifting and lowering
- Load retention after power loss
- Load-cell calibration
- Repeated pickup cycles
- Runtime
- Temperature and vibration
- Stability in worst-case load positions

Define pass/fail criteria where possible. Do not declare a design safe or validated until the relevant calculations and physical tests have been completed.

## 16.5 Revision control

Use revision identifiers for drawings and models. When changing a dimension or mechanism, identify which connected parts and drawings must also be updated.

---

# 17. WORKING METHOD AND DESIGN GATES

The concept stage is complete enough to begin preliminary modelling. Do not repeatedly ask the user to reconfirm decisions already stated in this brief.

However, do not conceal critical ambiguities. If a decision is essential to producing a mechanically valid model, explain the issue and ask one focused question. Otherwise, make a clearly labelled preliminary assumption and continue.

Use the following design gates:

### Gate 1 — Layout and architecture
- Establish the overall layout.
- Resolve the four-wheel steering/drive geometry.
- Establish chassis proportions and component envelopes.
- Check that the loader, tray and wheels can coexist.

### Gate 2 — First mechanical models
- Model the chassis.
- Model the wheel arrangement.
- Model the drive and transmission packaging.
- Model the pivoting loader and winch concept.

### Gate 3 — Mechanical integration
- Assemble the main subsystems.
- Check motion, clearances and interference.
- Check centre of gravity and load paths.
- Revise dimensions where necessary.

### Gate 4 — Detailed engineering
- Complete calculations.
- Select realistic motors, bearings, shafts, chains/cables, pulleys and fasteners.
- Prepare dimensioned drawings and BOM.
- Identify purchased versus custom components.

### Gate 5 — Prototype readiness
- Complete safety review.
- Complete manufacturing and assembly instructions.
- Prepare test plan.
- Identify all outstanding engineering validation.

Do not claim that the robot is ready to manufacture until the required checks are complete.

---

# 18. REQUIRED FINAL DELIVERABLES

At completion, provide an organised design package containing:

1. Overall robot design description
2. Requirements and assumptions register
3. Dimensioned overall drawings
4. Subsystem drawings
5. Individual component drawings
6. Written explanation for every drawing/image
7. Mechanical operation descriptions
8. Preliminary engineering calculations
9. Material and manufacturing recommendations
10. Purchased-component recommendations and specifications
11. Bill of Materials (BOM)
12. SolidWorks modelling instructions
13. SolidWorks assembly sequence
14. Exploded views
15. Motion-study/video prompts
16. Safety and risk review
17. Prototype test plan
18. Outstanding issues and engineering validation list
19. Completion/progress report

Organise outputs into a clear project structure, for example:

```text
ROBOT_V1_DESIGN/
├── 00_Project_Brief/
├── 01_Overall_Concept/
├── 02_Chassis/
├── 03_Mobility_and_Drive/
├── 04_Gear_Train/
├── 05_Power_and_Electronics/
├── 06_Sensors_and_Navigation/
├── 07_Loader_Assembly/
├── 08_Winch_and_Lifting/
├── 09_Shovel_and_Load_Measurement/
├── 10_Tray_and_Enclosure/
├── 11_SolidWorks_Parts/
├── 12_SolidWorks_Assemblies/
├── 13_Engineering_Drawings/
├── 14_Calculations_and_BOM/
├── 15_Videos_and_Animations/
└── 16_Testing_and_Validation/
```

---

# 19. FINAL INSTRUCTION

Begin with the overall layout and first chassis/mobility models. Then progress into the loader mechanism and the remaining subsystems.

The objective is to produce a coherent first mechanical design that the user can understand, recreate, assemble and improve in SolidWorks.

Be thorough, technically honest and practical. Explain the engineering reasoning behind important choices. Keep all dimensions and component interfaces consistent across the project.

**Do not prioritise impressive-looking renders over a mechanically workable design. The robot must make sense as a real machine that can be built and tested.**
