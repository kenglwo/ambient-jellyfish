import bpy
import time
import threading
import requests

# ==================================== requests

#res = requests.get("http://localhost:3000/api/test")
#data = res.json()["length"]
#data = data / 3
#bpy.context.scene.objects["C"].select_set(True)

#bpy.ops.transform.resize(value=(data, data, data), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

#bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

# ====================================

#for i in range(0, 100, 1):
#    time.sleep(6)
#    print(i, "seconds")
res = requests.get("http://localhost:3000/api/test")
data = res.json()["length"]
data = data / 3
print(data)

bpy.context.scene.objects["C"].select_set(True)
bpy.ops.transform.resize(value=(data, data, data), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

bpy.ops.screen.animation_play() 

#bpy.ops.screen.animation_cancel()    


## Duplicate a new body with particle system
#bpy.context.scene.objects["Jellyfish"].select_set(True)
#bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1.1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
#jellyfish_new = bpy.context.selected_objects[0]
#name = "Jellyfish_Kento"  
#jellyfish_new.name = name

## Add an animation path
#jellyfish_new.constraints["Follow Path"].target = bpy.data.objects["Animation_Path.002"]
##bpy.context.scene.objects[name].select_set(True)
#bpy.context.view_layer.objects.active = jellyfish_new
#bpy.ops.constraint.followpath_path_animate(constraint="Follow Path", owner='OBJECT', frame_start=1, length=600)
#bpy.context.object.constraints["Follow Path"].use_curve_follow = True
