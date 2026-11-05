# Blender 5.1 - swarm_tetra_visualizer.py
import bpy
import json
import math
import os

def load_swarm_data():
    """Load the swarm state JSON file, checking standard paths."""
    paths_to_check = [
        "C:/Users/SUBU/Documents/1MY_APPs/SwarmSystem/swarm_tetra_state.json",
        "swarm_tetra_state.json",
        "./swarm_tetra_state.json",
        "../SwarmSystem/swarm_tetra_state.json"
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            print(f"📂 Found telemetry data at: {path}")
            with open(path, "r") as f:
                return json.load(f)
                
    raise FileNotFoundError("Could not find swarm_tetra_state.json. Run the Warp simulation first!")

def clean_scene():
    """Clean all objects, meshes, and materials in the current scene."""
    # Switch to object mode if not already
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
        
    # Select and delete all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Purge orphan meshes and materials to free up memory
    for mesh in bpy.data.meshes:
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    for mat in bpy.data.materials:
        if mat.users == 0:
            bpy.data.materials.remove(mat)
    for light in bpy.data.lights:
        if light.users == 0:
            bpy.data.lights.remove(light)

def create_wavy_spindle(radius_cm, length_cm, amp_cm, freq):
    """Generate a highly aesthetic mathematically precise wavy cylinder spindle along the Y-axis."""
    R0 = radius_cm / 100.0   # Convert to meters
    L = length_cm / 100.0
    A = amp_cm / 100.0
    
    slices = 80
    segments = 36
    
    vertices = []
    faces = []
    
    # 1. Generate vertices
    for j in range(slices + 1):
        y = -L * 0.5 + j * (L / slices)
        # Wavy sine-wave radius
        phase = (y / L) * 2.0 * math.pi * freq
        r = R0 + A * math.sin(phase)
        
        for i in range(segments):
            theta = i * 2.0 * math.pi / segments
            x = r * math.cos(theta)
            z = r * math.sin(theta)
            vertices.append((x, y, z))
            
    # Add bottom and top endcaps for closed manifold geometry
    bottom_cap_idx = len(vertices)
    vertices.append((0.0, -L * 0.5, 0.0))
    top_cap_idx = len(vertices)
    vertices.append((0.0, L * 0.5, 0.0))
    
    # 2. Generate side quad faces
    for j in range(slices):
        for i in range(segments):
            next_i = (i + 1) % segments
            v0 = j * segments + i
            v1 = j * segments + next_i
            v2 = (j + 1) * segments + next_i
            v3 = (j + 1) * segments + i
            faces.append((v0, v1, v2, v3))
            
    # 3. Generate endcap triangles
    for i in range(segments):
        next_i = (i + 1) % segments
        # Bottom cap
        faces.append((bottom_cap_idx, next_i, i))
        # Top cap
        v_top_curr = slices * segments + i
        v_top_next = slices * segments + next_i
        faces.append((top_cap_idx, v_top_curr, v_top_next))
        
    mesh = bpy.data.meshes.new("SpindleMesh")
    obj = bpy.data.objects.new("Reference_Spindle", mesh)
    
    bpy.context.collection.objects.link(obj)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    
    # Set smooth shading
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    return obj

def build_regular_tetrahedron_mesh(edge_length):
    """Return a custom Blender mesh representing a mathematically perfect regular tetrahedron."""
    a = edge_length
    
    # Exact coordinates relative to barycenter
    vertices = [
        (0.0, 0.0, (math.sqrt(6.0) / 4.0) * a),
        (0.0, (math.sqrt(3.0) / 3.0) * a, -(math.sqrt(6.0) / 12.0) * a),
        (-a * 0.5, -(math.sqrt(3.0) / 6.0) * a, -(math.sqrt(6.0) / 12.0) * a),
        (a * 0.5, -(math.sqrt(3.0) / 6.0) * a, -(math.sqrt(6.0) / 12.0) * a)
    ]
    
    # 4 triangular faces
    faces = [
        (0, 1, 2),
        (0, 2, 3),
        (0, 3, 1),
        (1, 3, 2)
    ]
    
    mesh = bpy.data.meshes.new("Tetrahedron_Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    return mesh

def setup_materials():
    """Create and return standard sleek metallic, glass, and emissive materials."""
    def set_socket(node, possible_names, value):
        if isinstance(possible_names, str):
            possible_names = [possible_names]
        for name in possible_names:
            if name in node.inputs:
                node.inputs[name].default_value = value
                return True
        return False

    # 1. Spindle Material (Sleek dark metal/glass mix)
    spindle_mat = bpy.data.materials.new(name="SpindleMat")
    spindle_mat.use_nodes = True
    nodes = spindle_mat.node_tree.nodes
    principled = nodes.get("Principled BSDF")
    if principled:
        set_socket(principled, "Base Color", (0.05, 0.08, 0.15, 1.0)) # Deep dark navy
        set_socket(principled, "Metallic", 0.9)
        set_socket(principled, "Roughness", 0.2)
        
    # 2. Transparent Dark Glass Tetrahedron Material
    glass_mat = bpy.data.materials.new(name="TetraGlassMat")
    glass_mat.use_nodes = True
    nodes = glass_mat.node_tree.nodes
    principled = nodes.get("Principled BSDF")
    if principled:
        # High transmission glass look
        set_socket(principled, "Base Color", (0.2, 0.5, 0.8, 1.0)) # Cool Ice Blue
        set_socket(principled, "Roughness", 0.1)
        set_socket(principled, "IOR", 1.45)
        set_socket(principled, ["Transmission Weight", "Transmission"], 0.95)
        
    # 3. Glowing LED Core Material (Microcontroller transmitter)
    glow_mat = bpy.data.materials.new(name="NeonCoreMat")
    glow_mat.use_nodes = True
    nodes = glow_mat.node_tree.nodes
    principled = nodes.get("Principled BSDF")
    if principled:
        # High-intensity emission
        set_socket(principled, "Base Color", (0.0, 1.0, 0.4, 1.0)) # Neon Mint Green
        set_socket(principled, ["Emission Color", "Emission"], (0.0, 1.0, 0.4, 1.0))
        set_socket(principled, "Emission Strength", 10.0)
        set_socket(principled, "Roughness", 0.1)
        
    return spindle_mat, glass_mat, glow_mat

def setup_studio_lighting_and_camera():
    """Configure modern studio three-point lighting and an active focused camera."""
    # 1. Active Camera
    cam_data = bpy.data.cameras.new("StudioCamera")
    cam_obj = bpy.data.objects.new("Camera", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    
    # Position camera looking down-angled at the wavy cylinder spindle
    cam_obj.location = (1.1, -1.5, 0.7)
    cam_obj.rotation_euler = (math.radians(65), 0, math.radians(35))
    
    # 2. Three-Point Lighting Setup
    # Key Light (Warm, high power)
    key_light_data = bpy.data.lights.new("KeyLight", type='AREA')
    key_light_data.energy = 250.0
    key_light_data.color = (1.0, 0.9, 0.8) # Warm sun
    key_light_data.size = 0.5
    key_obj = bpy.data.objects.new("KeyLight", key_light_data)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (1.2, -0.8, 1.2)
    key_obj.rotation_euler = (math.radians(45), 0, math.radians(45))
    
    # Fill Light (Cool, soft)
    fill_light_data = bpy.data.lights.new("FillLight", type='AREA')
    fill_light_data.energy = 80.0
    fill_light_data.color = (0.7, 0.85, 1.0) # Cool blue
    fill_light_data.size = 0.8
    fill_obj = bpy.data.objects.new("FillLight", fill_light_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-1.2, -0.6, 0.8)
    fill_obj.rotation_euler = (math.radians(45), 0, math.radians(-45))
    
    # Rim Light / Accent (Back-light to pop glass edges and neon cores)
    rim_light_data = bpy.data.lights.new("RimLight", type='POINT')
    rim_light_data.energy = 150.0
    rim_light_data.color = (0.0, 1.0, 0.5) # Neon accent match
    rim_obj = bpy.data.objects.new("RimLight", rim_light_data)
    bpy.context.collection.objects.link(rim_obj)
    rim_obj.location = (0.0, 1.3, 0.3)

def generate_swarm_mesh():
    """Main execution function inside Blender."""
    print("=" * 60)
    print("🛸 WEXXY SWARM TETRAHEDRAL MESH VISUALIZER — BLENDER 5.1")
    print("=" * 60)
    
    # 1. Clean Scene
    clean_scene()
    
    # 2. Load Swarm Telemetry
    data = load_swarm_data()
    num_agents = data["num_agents"]
    cyl_cfg = data["cylinder"]
    
    # 3. Create Wavy Spindle
    spindle = create_wavy_spindle(
        radius_cm=cyl_cfg["radius_cm"],
        length_cm=cyl_cfg["length_cm"],
        amp_cm=cyl_cfg["amplitude_cm"],
        freq=cyl_cfg["frequency"]
    )
    
    # 4. Setup Materials
    spindle_mat, glass_mat, glow_mat = setup_materials()
    spindle.data.materials.append(spindle_mat)
    
    # 5. Calculate Edge Length for Exactly 1 cm³ Regular Tetrahedron
    # V = a^3 / (6 * sqrt(2)) => a = (6 * sqrt(2) * V)^(1/3)
    # V = 1 cm^3 = 0.000001 m^3
    volume_m3 = 1e-6
    edge_length_m = math.pow(6.0 * math.sqrt(2.0) * volume_m3, 1.0 / 3.0)
    
    # Build shared tetrahedron mesh container to optimize memory
    tetra_mesh = build_regular_tetrahedron_mesh(edge_length_m)
    
    # 6. Generate Agents
    # Microcontroller sphere mesh
    sphere_mesh = bpy.data.meshes.new("CoreSphereMesh")
    # Quick low-poly uv sphere to keep viewport extremely fast and responsive
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0022, segments=12, ring_count=8)
    active_obj = bpy.context.active_object
    sphere_mesh = active_obj.data.copy()
    bpy.ops.object.delete() # Remove the temporary template object
    
    for i, agent in enumerate(data["agents"]):
        pos = agent["position"]
        rot = agent["quaternion"] # w, x, y, z
        
        # Scale centimeters to Blender meters
        loc = (pos[0] / 100.0, pos[1] / 100.0, pos[2] / 100.0)
        
        # A. Create Tetrahedron Object using shared mesh
        tet_obj = bpy.data.objects.new(f"Tetra_Agent_{i:04d}", tetra_mesh)
        tet_obj.location = loc
        tet_obj.rotation_mode = 'QUATERNION'
        tet_obj.rotation_quaternion = (rot[0], rot[1], rot[2], rot[3]) # w, x, y, z
        tet_obj.data.materials.append(glass_mat)
        bpy.context.collection.objects.link(tet_obj)
        
        # B. Create Embedded Sphere (Microcontroller) parented to Tetrahedron
        sphere_obj = bpy.data.objects.new(f"Core_{i:04d}", sphere_mesh)
        # Position at (0, 0, 0) relative to parent tetrahedron's center
        sphere_obj.location = (0.0, 0.0, 0.0)
        sphere_obj.parent = tet_obj
        sphere_obj.data.materials.append(glow_mat)
        bpy.context.collection.objects.link(sphere_obj)
        
    # 7. Lighting & Camera Setup
    setup_studio_lighting_and_camera()
    
    # Refresh view
    bpy.context.view_layer.update()
    
    print()
    print("=" * 60)
    print(f"✅ SUCCESS: Created {num_agents} intelligent tetrahedral agents with embedded glowing microcontrollers.")
    print("   Reference spindle and studio-lighting configured.")
    print("=" * 60)

if __name__ == "__main__":
    generate_swarm_mesh()
