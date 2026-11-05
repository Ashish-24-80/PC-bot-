bl_info = {
    "name": "Swarm Tetra Control",
    "author": "Antigravity",
    "version": (1, 0),
    "blender": (5, 1, 0),
    "location": "View3D > Sidebar > Swarm",
    "description": "Real-time UDP control for Warp tetrahedral swarm",
    "warning": "",
    "doc_url": "",
    "category": "Animation",
}

import bpy
import socket
import json
import struct
import math
import numpy as np
from mathutils import Vector, Quaternion

# Global State
sock_recv = None
sock_send = None
timer_running = False
agents = []

def init_sockets():
    global sock_recv, sock_send
    
    if sock_recv is None:
        sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_recv.bind(("127.0.0.1", 5011))
        sock_recv.setblocking(False)
        
    if sock_send is None:
        sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def close_sockets():
    global sock_recv, sock_send
    if sock_recv:
        sock_recv.close()
        sock_recv = None
    if sock_send:
        sock_send.close()
        sock_send = None

def get_or_create_materials():
    if "Swarm_Glass" not in bpy.data.materials:
        mat = bpy.data.materials.new("Swarm_Glass")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.01, 0.05, 0.1, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.05
            bsdf.inputs["IOR"].default_value = 1.45
            if "Transmission Weight" in bsdf.inputs:
                bsdf.inputs["Transmission Weight"].default_value = 1.0
            elif "Transmission" in bsdf.inputs:
                bsdf.inputs["Transmission"].default_value = 1.0
    
    if "Swarm_Core" not in bpy.data.materials:
        mat = bpy.data.materials.new("Swarm_Core")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.0, 1.0, 0.8, 1.0)
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = (0.0, 1.0, 0.8, 1.0)
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = 15.0
                
    return bpy.data.materials["Swarm_Glass"], bpy.data.materials["Swarm_Core"]

def create_agent_mesh():
    # 1 cm^3 tetrahedron -> edge length ~ 0.020396m
    a = 0.020396
    v0 = (0, 0, math.sqrt(6)/4 * a)
    v1 = (0, math.sqrt(3)/3 * a, -math.sqrt(6)/12 * a)
    v2 = (-a/2, -math.sqrt(3)/6 * a, -math.sqrt(6)/12 * a)
    v3 = (a/2, -math.sqrt(3)/6 * a, -math.sqrt(6)/12 * a)
    verts = [v0, v1, v2, v3]
    faces = [(0,1,2), (0,2,3), (0,3,1), (1,3,2)]
    
    mesh = bpy.data.meshes.new("TetraMesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return mesh

def spawn_agents(count):
    global agents
    collection = bpy.data.collections.get("SwarmAgents")
    if not collection:
        collection = bpy.data.collections.new("SwarmAgents")
        bpy.context.scene.collection.children.link(collection)
        
    glass_mat, core_mat = get_or_create_materials()
    tetra_mesh = create_agent_mesh()
    
    # Pre-spawn agents
    current_count = len(agents)
    if current_count < count:
        for i in range(current_count, count):
            obj = bpy.data.objects.new(f"Agent_{i:04d}", tetra_mesh)
            obj.data.materials.append(glass_mat)
            obj.rotation_mode = 'QUATERNION'
            collection.objects.link(obj)
            
            core = bpy.data.objects.new(f"Core_{i:04d}", bpy.data.meshes.new("CoreMesh"))
            # Just give it a single vertex or minimal shape if we don't want to build a sphere from scratch, 
            # but actually it's easier to just use an empty or copy an existing sphere. 
            # Even better, let's just make the tetrahedron emissive directly if we want, or create a simple icosphere data.
            # To be safe, let's just parent an empty or simple mesh. Actually, we can just skip the sphere and make the tetra glass+core,
            # but to keep the core, we can just make a small cube programmatically:
            c_mesh = bpy.data.meshes.new("CoreCube")
            c_verts = [(-.002,-.002,-.002), (.002,-.002,-.002), (.002,.002,-.002), (-.002,.002,-.002),
                       (-.002,-.002,.002), (.002,-.002,.002), (.002,.002,.002), (-.002,.002,.002)]
            c_faces = [(0,1,2,3), (4,5,6,7), (0,1,5,4), (1,2,6,5), (2,3,7,6), (3,0,4,7)]
            c_mesh.from_pydata(c_verts, [], c_faces)
            c_mesh.update()
            
            core.data = c_mesh
            core.data.materials.append(core_mat)
            core.parent = obj
            collection.objects.link(core)
            
            agents.append(obj)

def udp_update_timer():
    global sock_recv, agents, timer_running
    
    if not timer_running or sock_recv is None:
        return None
        
    try:
        data = None
        while True:
            # Drain socket buffer to get the latest packet
            try:
                packet, addr = sock_recv.recvfrom(65536)
                data = packet
            except BlockingIOError:
                break
                
        if data:
            # Packet format: num_agents(i), offset(i), count(i), [x,y,z, qw,qx,qy,qz]...
            header = struct.unpack_from("iii", data, 0)
            total_agents, offset, count = header
            
            # Make sure we have enough Blender objects
            if len(agents) < total_agents:
                spawn_agents(total_agents)
                
            payload_size = count * 10
            floats = struct.unpack_from(f"{payload_size}f", data, 12)
            
            idx = 0
            for i in range(count):
                agent_idx = offset + i
                if agent_idx < len(agents):
                    obj = agents[agent_idx]
                    obj.location = (floats[idx], floats[idx+1], floats[idx+2])
                    obj.rotation_quaternion = (floats[idx+3], floats[idx+4], floats[idx+5], floats[idx+6])
                    obj.scale = (floats[idx+7], floats[idx+8], floats[idx+9])
                idx += 10
                
    except Exception as e:
        print(f"UDP Recv Error: {e}")
        
    return 0.02 # 50 fps

class SWARM_OT_start_sync(bpy.types.Operator):
    bl_idname = "swarm.start_sync"
    bl_label = "Start Live Sync"
    
    def execute(self, context):
        global timer_running
        if not timer_running:
            init_sockets()
            timer_running = True
            bpy.app.timers.register(udp_update_timer)
            self.report({'INFO'}, "Swarm Sync Started")
        return {'FINISHED'}

class SWARM_OT_stop_sync(bpy.types.Operator):
    bl_idname = "swarm.stop_sync"
    bl_label = "Stop Live Sync"
    
    def execute(self, context):
        global timer_running
        if timer_running:
            timer_running = False
            close_sockets()
            bpy.app.timers.unregister(udp_update_timer)
            self.report({'INFO'}, "Swarm Sync Stopped")
        return {'FINISHED'}

class SWARM_OT_send_target(bpy.types.Operator):
    bl_idname = "swarm.send_target"
    bl_label = "Send Picked Target"
    
    def execute(self, context):
        global sock_send
        target_obj = context.scene.swarm_target
        if not target_obj or target_obj.type != 'MESH':
            self.report({'ERROR'}, "Select a valid Mesh object")
            return {'CANCELLED'}
            
        depsgraph = context.evaluated_depsgraph_get()
        eval_obj = target_obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        
        # Get world space vertices
        verts = [(eval_obj.matrix_world @ v.co).to_tuple() for v in mesh.vertices]
        eval_obj.to_mesh_clear()
        
        if sock_send is None:
            init_sockets()
            
        payload = json.dumps({"vertices": verts})
        try:
            sock_send.sendto(payload.encode('utf-8'), ("127.0.0.1", 5012))
            self.report({'INFO'}, f"Sent {len(verts)} vertices to Swarm")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to send: {e}")
            
        return {'FINISHED'}

class SWARM_PT_panel(bpy.types.Panel):
    bl_label = "Swarm Tetra Control"
    bl_idname = "SWARM_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Swarm'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene, "swarm_target", text="Target Mesh")
        layout.operator("swarm.send_target", icon='EXPORT')
        
        layout.separator()
        
        global timer_running
        if timer_running:
            layout.operator("swarm.stop_sync", icon='PAUSE')
        else:
            layout.operator("swarm.start_sync", icon='PLAY')

def register():
    bpy.types.Scene.swarm_target = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.utils.register_class(SWARM_OT_start_sync)
    bpy.utils.register_class(SWARM_OT_stop_sync)
    bpy.utils.register_class(SWARM_OT_send_target)
    bpy.utils.register_class(SWARM_PT_panel)

def unregister():
    bpy.utils.unregister_class(SWARM_PT_panel)
    bpy.utils.unregister_class(SWARM_OT_send_target)
    bpy.utils.unregister_class(SWARM_OT_stop_sync)
    bpy.utils.unregister_class(SWARM_OT_start_sync)
    del bpy.types.Scene.swarm_target
    
    global timer_running
    if timer_running:
        timer_running = False
        bpy.app.timers.unregister(udp_update_timer)
    close_sockets()

if __name__ == "__main__":
    register()
