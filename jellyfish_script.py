import bpy
import time
import datetime
import threading
import requests
import json
from numpy import interp

# URLs
URL_GET_ATTENDEES_INFO = "http://localhost:3000/api/blender/get_attendees_info"
URL_GET_LATEST_SPEEKING_INFO = "http://localhost:3000/api/blender/get_latest_speaking_info"

# Global vars
MEETING_ID = ""
MEETING_START_TIME = ""
UPDATE_INTERVAL_SECONDS = 86300 * 2 # TODO: chang to 60 seconds

# pre-defined data
material_array = ["Jelly_Blue", "Jelly_Pink", "Jelly_Yellow"]
material_aquarium = ["Bottle_Body_Blue", "Bottle_Body_Pink", "Bottle_Body_Yellow"]
material_lamp = ["Lamp_Blue", "Lamp_Pink", "Lamp_Yellow"]
material_bottom = ["Bottom_Seabed", "Bottom_Rock", "Bottom_Grass_Little", "Bottom_Grass"]


def show_objects(object_array):
    for object in object_array:
        bpy.context.scene.objects[object].hide_set(False)

def hide_objects(object_array):
    for object in object_array:
        bpy.context.scene.objects[object].hide_set(True)

def duplicate_move_object(x_position):
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(x_position, -0, -0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    
def relocate_collection(object_name):
    bpy.data.collections['Users'].objects.link(bpy.context.scene.objects[object_name])
    bpy.data.collections['Base'].objects.unlink(bpy.context.scene.objects[object_name]) 

def stop_playback(scene):
    if(scene.frame_current == scene.frame_end):
        bpy.ops.screen.animation_cancel(restore_frame=False)
        bpy.ops.screen.frame_jump(end=False)

def if_setup_ready():
    for collection in bpy.data.collections:
        if collection.name == "Users":
            if len(collection.objects) > 0:
                return True
            else:
                return False

def update_jellyfish_particle(attendee_name, tentacles_num, tentacles_length):
    jellyfish = "Jellyfish_{}".format(attendee_name)
    p = bpy.context.scene.objects[jellyfish].particle_systems
    particle_tentacles = p[0].settings.name
    bpy.data.particles[particle_tentacles].count = tentacles_num
    bpy.data.particles[particle_tentacles].hair_length = tentacles_length
    
def update_jellyfish_animation_path(attendee_name, level):
    jellyfish = "Jellyfish_{}".format(attendee_name)
    new_animation_path = "Anim_Path_{}_{}".format(level, attendee_name)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[jellyfish]
    bpy.context.object.constraints["Follow Path"].target = bpy.data.objects[new_animation_path]
    bpy.ops.constraint.followpath_path_animate(constraint="Follow Path", owner='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

def update_jellyfish_body_size(attendee_name, animation_path_level):
    jellyfish = "Jellyfish_{}".format(attendee_name)
    ratio = interp(animation_path_level, [1,5], [1,2])
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects[jellyfish].select_set(True)
    bpy.ops.transform.resize(value=(ratio, ratio, ratio), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    
def update_particle_plate(attendee_name, bubbles_count, bubbles_instance, corals_count):
    particles_plate = "Particles_Plate_{}".format(attendee_name)
    p = bpy.context.scene.objects[particles_plate].particle_systems
    particle_bubbles = p[0].settings.name
    particle_corals = p[1].settings.name
    bpy.data.particles[particle_bubbles].count = bubbles_count
    bpy.data.particles[particle_bubbles].instance_object = bpy.data.objects[bubbles_instance]
    bpy.data.particles[particle_corals].count =  corals_count

def update_bottom_material(attendee_name, material_stage_level):
    bottom = "Sand_{}".format(attendee_name)
    material = material_bottom[material_stage_level]
    bpy.context.scene.objects[bottom].data.materials[0] = bpy.data.materials[material]
        
def setup_environment():
    """
        Get attendees info and create necessary objects for each person
    """
    
    attendees_info = requests.get(URL_GET_ATTENDEES_INFO)
    attendees_info_array = attendees_info.json()

    MEETING_ID = attendees_info_array["meeting_id"]
    MEETING_START_TIME = datetime.datetime.strptime(attendees_info_array["datetime_start"], '%Y-%m-%d %H:%M:%S')


    for i, d in enumerate(attendees_info_array["attendees_list"]):
        # get attendee's info
        attendee_id = d["attendee_id"]
        attendee_name = d["attendee_name"]
        is_host = d["is_host"]
        
        # show necessaary objects
        show_objects(["Jellyfish", "Name", "Anim_Path_1", "Anim_Path_2", "Anim_Path_3", "Anim_Path_4", "Anim_Path_5", "Aquarium", "Sand", "Spot", "Lamp", "Bubble", "Particles_Plate"])

        ## create aquarium
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects["Aquarium"].select_set(True)
        bpy.context.scene.objects["Sand"].select_set(True)
        bpy.context.scene.objects["Spot"].select_set(True)
        bpy.context.scene.objects["Lamp"].select_set(True)
        bpy.context.scene.objects["Particles_Plate"].select_set(True)
        duplicate_move_object(3*i)
        
        # add materials
        bpy.context.scene.objects["Aquarium.001"].material_slots[1].material = bpy.data.materials[material_aquarium[i]]
        bpy.context.scene.objects["Lamp.001"].material_slots[0].material = bpy.data.materials[material_lamp[i]]
        
        bpy.context.scene.objects["Aquarium.001"].name = "Aquarium_{}".format(attendee_name)
        bpy.context.scene.objects["Sand.001"].name = "Sand_{}".format(attendee_name)
        bpy.context.scene.objects["Spot.001"].name = "Spot_{}".format(attendee_name)
        bpy.context.scene.objects["Lamp.001"].name = "Lamp_{}".format(attendee_name)
        bpy.context.scene.objects["Particles_Plate.001"].name = "Particles_Plate_{}".format(attendee_name)

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active =        bpy.context.scene.objects["Particles_Plate_{}".format(attendee_name)]
        bpy.ops.particle.duplicate_particle_system(use_duplicate_settings=True)
        bpy.ops.particle.target_move_up()
        bpy.ops.object.particle_system_remove() 
        bpy.ops.object.particle_system_remove() 
        
        relocate_collection("Aquarium_{}".format(attendee_name))
        relocate_collection("Sand_{}".format(attendee_name))
        relocate_collection("Spot_{}".format(attendee_name))
        relocate_collection("Lamp_{}".format(attendee_name))
        relocate_collection("Particles_Plate_{}".format(attendee_name))
        
        ## create animation path
        for j in range(1, 6):
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects["Anim_Path_{}".format(j)].select_set(True)
            duplicate_move_object(3*i)
            path_name = "Anim_Path_{}_{}".format(j, attendee_name)
            bpy.context.scene.objects["Anim_Path_{}.001".format(j)].name = path_name
            relocate_collection(path_name)


        # create a object for each attendee 
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects["Jellyfish"].select_set(True)
        duplicate_move_object(0)

        ## rename object
        jellyfish_name = "Jellyfish_{}".format(attendee_name)
        bpy.context.scene.objects["Jellyfish.001"].name = jellyfish_name
        
        ## attach animation path
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.context.scene.objects[jellyfish_name]
        bpy.context.scene.cursor.location = (3*i, 0.0, 0.0)
        path_name = "Anim_Path_1_{}".format( attendee_name)
        bpy.ops.object.constraint_add(type='FOLLOW_PATH')
        bpy.context.object.constraints["Follow Path"].target = bpy.data.objects[path_name]
        bpy.context.object.constraints["Follow Path"].use_fixed_location = False
        bpy.ops.constraint.followpath_path_animate(constraint="Follow Path", owner='OBJECT')
        
        bpy.ops.transform.translate(value=(3*i, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        
        ## add wave modifier
        bpy.ops.object.modifier_add(type='WAVE')
        bpy.context.object.modifiers["Wave"].use_x = False
        bpy.context.object.modifiers["Wave"].use_y = False
        bpy.context.object.modifiers["Wave"].use_normal = True
        bpy.context.object.modifiers["Wave"].use_normal_x = False
        bpy.context.object.modifiers["Wave"].use_normal = True
        bpy.context.object.modifiers["Wave"].speed = 0.03


        ## give material
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects[jellyfish_name].select_set(True)
        material_name = material_array[i]
        material = bpy.data.materials[material_name]
        bpy.context.scene.objects[jellyfish_name].data.materials.append(material)
        relocate_collection(jellyfish_name)
        
        # duplicate particle setting of jellyfish
#        bpy.ops.object.select_all(action='DESELECT')
#        bpy.context.view_layer.objects.active = bpy.context.scene.objects[jellyfish_name]
        bpy.ops.particle.duplicate_particle_system(use_duplicate_settings=True)
        bpy.ops.particle.target_move_up()
        bpy.ops.object.particle_system_remove() 
#        bpy.ops.object.particle_system_remove() 
        
        # add text to show the attendee's name
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects["Name"].select_set(True)
        duplicate_move_object(3*i)
        
        ## rename Name object
        new_name = "Name_{}".format(attendee_name)
        bpy.context.scene.objects["Name.001"].name = new_name
        ## show attendee's name
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.context.scene.objects[new_name]
        bpy.ops.object.editmode_toggle()
        for i in range(0, 4):
            bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
        bpy.ops.font.text_insert(text=attendee_name, accent=False)
        bpy.ops.object.editmode_toggle()  
        
        bpy.context.scene.objects[new_name].select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
        if(i>0):
            bpy.ops.transform.translate(value=(-0.5, -0, -0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)    
        relocate_collection(new_name)   

        # deselect all 
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)

    hide_objects(["Jellyfish", "Name", "Anim_Path_1", "Anim_Path_2", "Anim_Path_3", "Anim_Path_4", "Anim_Path_5", "Aquarium", "Sand", "Spot", "Lamp", "Bubble", "Particles_Plate"])
        
if (if_setup_ready()):
    bpy.ops.screen.animation_cancel(restore_frame=False)
    bpy.ops.screen.frame_jump(end=False)
    
    # TODO: get meeting info and update objects
    payload = {'update_interval_seconds': UPDATE_INTERVAL_SECONDS}
    output = requests.get(URL_GET_LATEST_SPEEKING_INFO, params=payload)
    latest_speaking_data = output.json()
    
    for i, d in enumerate(latest_speaking_data):
        attendee_name = d["attendee_name"]
        
        # update data for jellyfish
#        animation_path_level = int(d["animation_path_level"]) + i+1
        animation_path_level = i+4
        jellyfish_tentacles_num = animation_path_level * 5
        jellyfish_tentacles_length = animation_path_level * 1
        # update data for particle plate
        bubbles_count = int(d["bubbles_count"])  
        bubbles_instance = d["bubbles_instance"]
        corals_count = i*20
        # update data bottom material
        material_stage_level = i+2
        
        
        # update jellyfish
        update_jellyfish_animation_path(attendee_name, animation_path_level)
        update_jellyfish_particle(attendee_name, jellyfish_tentacles_num, jellyfish_tentacles_length)
        update_jellyfish_body_size(attendee_name, animation_path_level)
        
        # update particle palte
        update_particle_plate(attendee_name, bubbles_count, bubbles_instance, corals_count)
        # update bottom material
        update_bottom_material(attendee_name, material_stage_level)
        
        # delete keyframes
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.context.scene.objects["Jellyfish_{}".format(attendee_name)]
        bpy.context.active_object.animation_data_clear()
        
    bpy.ops.screen.animation_play()
else:
    setup_environment()
    bpy.ops.screen.animation_play()
    