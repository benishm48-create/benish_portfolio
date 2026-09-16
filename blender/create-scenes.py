"""Run: blender --background --python blender/create-scenes.py
Creates original editable Blender scenes, optimized GLB files and fallback renders.
Coordinates use Blender Z-up; the GLB exporter converts to Three.js Y-up.
"""
import bpy, math, os
from mathutils import Matrix
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODELS=ROOT/'public'/'models';MODELS.mkdir(exist_ok=True,parents=True)
TEXTURES=ROOT/'public'/'textures'

def mat(name,color,metal=0,rough=.5,emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
 if emission:bs.inputs['Emission Color'].default_value=(*color,1);bs.inputs['Emission Strength'].default_value=emission
 return m

def finish(obj,name,material):
 obj.name=name
 if material:obj.data.materials.append(material)
 return obj

def box(name,loc,scale,material,bevel=.04):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Soft manufactured edges','BEVEL');mod.width=bevel;mod.segments=3
  bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
  mod=o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');bpy.ops.object.modifier_apply(modifier=mod.name)
 return finish(o,name,material)

def sphere(name,loc,scale,material,segments=24):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=12,location=loc);o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for p in o.data.polygons:p.use_smooth=True
 return finish(o,name,material)

def cylinder(name,a,b,r,material,r2=None):
 v=Vector(b)-Vector(a);mid=(Vector(a)+Vector(b))/2
 bpy.ops.mesh.primitive_cone_add(vertices=24,radius1=r,radius2=r if r2 is None else r2,depth=v.length,location=mid);o=bpy.context.object;o.rotation_euler=v.to_track_quat('Z','Y').to_euler()
 for p in o.data.polygons:p.use_smooth=True
 mod=o.modifiers.new('Edge softness','BEVEL');mod.width=.012;mod.segments=2;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 return finish(o,name,material)

def text(name,body,loc,size,material,rot=(math.pi/2,0,0)):
 bpy.ops.object.text_add(location=loc);o=bpy.context.object;o.name=name;o.data.body=body;o.data.size=size;o.data.align_x='CENTER';o.data.extrude=.0007;o.rotation_euler=rot;o.data.materials.append(material);bpy.ops.object.convert(target='MESH');return bpy.context.object

def screen_material(file):
 m=mat('Display: '+file,(1,1,1),rough=.9);bs=m.node_tree.nodes.get('Principled BSDF');im=bpy.data.images.load(str(TEXTURES/file));im.pack();node=m.node_tree.nodes.new('ShaderNodeTexImage');node.image=im;m.node_tree.links.new(node.outputs['Color'],bs.inputs['Base Color']);m.node_tree.links.new(node.outputs['Color'],bs.inputs['Emission Color']);bs.inputs['Emission Strength'].default_value=.65;return m


def curve(name, points, radius, material):
 data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.bevel_depth=radius;data.bevel_resolution=3
 sp=data.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for pt,co in zip(sp.bezier_points,points):pt.co=co;pt.handle_left_type='AUTO';pt.handle_right_type='AUTO'
 ob=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(ob);ob.data.materials.append(material)
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH');return bpy.context.object

def texture_surface(material, scale, strength, distance, stretch=(1,1,1)):
 nt=material.node_tree;n=nt.nodes;bs=n.get('Principled BSDF')
 coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=stretch;nt.links.new(coord.outputs['Generated'],mapping.inputs[0])
 noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;noise.inputs['Detail'].default_value=3;nt.links.new(mapping.outputs[0],noise.inputs['Vector'])
 bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=strength;bump.inputs['Distance'].default_value=distance;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs['Normal'],bs.inputs['Normal'])

def scene(kind):
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 graphite=mat('Graphite powder coat',(.055,.068,.09),.45,.35)
 edge=mat('Brushed alloy',(.22,.27,.34),.7,.3)
 dark=mat('Soft charcoal',(.025,.032,.046),.05,.8)
 desk=mat('Smoked walnut',(.21,.155,.115),0,.48)
 pad=mat('Slate desk mat',(.075,.095,.13),0,.85)
 blue=mat('Cool blue accent',(.25,.42,.7),.2,.35)
 light=mat('Warm light',(.98,.78,.5),0,.4,2)
 white=mat('Lettering',(.66,.73,.85),.1,.5)
 green=mat('Sage leaves',(.14,.27,.2),0,.65)
 skin=mat('Warm skin',(.47,.26,.16),0,.7)
 hair=mat('Dark hair',(.023,.018,.018),0,.8)
 shirt=mat('Midnight knit',(.09,.16,.28),0,.95)
 jeans=mat('Charcoal trousers',(.045,.058,.081),0,.95)
 shoe=mat('Off-white sneakers',(.62,.64,.61),0,.8)
 texture_surface(desk,7,.22,.025,(1,32,6))
 texture_surface(shirt,110,.2,.012)
 texture_surface(pad,95,.2,.009)
 # A small architectural platform, framing the workspace.
 box('Floating studio platform',(0,-.2,.025),(5.8,4.6,.15),graphite,.23)
 box('Walnut desktop',(0,.2,2.05),(4.65,1.9,.15),desk,.08)
 box('Desk front edge',(0,-.743,2.015),(4.49,.025,.07),edge,.01)
 for x in [-1.96,1.96]:
  for y in [-.48,.87]:cylinder('Desk leg',(x,y,.18),(x,y,2),.045,graphite)
  cylinder('Desk foot rail',(x,-.66,.17),(x,1.06,.17),.045,graphite)
 box('Desk mat',(.15,.07,2.134),(2.25,1.16,.018),pad,.08)
 # Victus-style laptop with separate lid, keys, trackpad and wordmark.
 box('HP Victus chassis',(.2,.06,2.18),(1.48,.88,.075),edge,.04)
 box('Keyboard deck',(.2,.045,2.222),(1.41,.82,.013),graphite,.025)
 for row in range(5):
  for col in range(14):box('Keyboard key',(-.406+col*.093,.333-row*.085,2.235),(.069,.054,.012),dark,.006)
 box('Space bar',(.15,-.06,2.236),(.43,.045,.012),dark,.006)
 box('Touchpad',(.19,-.239,2.235),(.46,.21,.008),edge,.015)
 # Lid is vertical, so the screen remains readable from the presentation camera.
 box('Victus display lid',(.2,.464,2.69),(1.49,.075,.94),graphite,.045)
 box('Display bezel',(.2,.420,2.697),(1.41,.018,.843),dark,.009)
 bpy.ops.mesh.primitive_plane_add(size=2,location=(.2,.407,2.711),rotation=(math.pi/2,0,0));o=bpy.context.object;o.scale=(.674,.39,1);finish(o,'Laptop screen',screen_material('code-screen.png' if kind=='hero' else 'music-screen.png'))
 text('VICTUS wordmark','V I C T U S',(.2,.399,2.265),.029,white)
 sphere('Webcam',(.2,.407,3.133),(.013,.006,.013),edge)
 # Back logo remains visible when rotating.
 text('Victus V logo','V',(.2,.508,2.74),.22,white,(-math.pi/2,0,math.pi))
 # Tilt the entire screen assembly around the real hinge, not its center.
 hinge=Vector((.2,.46,2.23));rot=Matrix.Rotation(math.radians(-13),4,'X')
 for obj in list(bpy.context.scene.objects):
  if obj.name in ['Victus display lid','Display bezel','Laptop screen','VICTUS wordmark','Webcam','Victus V logo']:
   obj.matrix_world=Matrix.Translation(hinge)@rot@Matrix.Translation(-hinge)@obj.matrix_world
 for x in [-.36,.76]:cylinder('Display hinge',(x-.09,.45,2.235),(x+.09,.45,2.235),.032,edge)
 for x in [-.548,.948]:
  for y in [-.12,.07,.2]:box('Recessed USB port',(x,y,2.18),(.008,.075,.024),dark,.004)
 for i in range(21):box('Rear cooling vent',(-.42+i*.06,.497,2.179),(.033,.009,.032),dark,.003)
 for side in [-1,1]:
  for i in range(16):box('Speaker grille',(.2+side*.662,-.16+i*.032,2.234),(.011,.013,.003),edge,.002)
 for row in range(4):
  for col in range(12):text('Key legend','1234567890QWERTYUIOPASDFGHJKLZXCVBNM'[(row*12+col)%36],(-.4+col*.093,.32-row*.085,2.243),.019,white,(0,0,0))
 # Mouse and pen notebook.
 sphere('Wireless mouse',(1.2,-.24,2.19),(.135,.205,.055),graphite)
 box('Mouse wheel',(1.2,-.17,2.244),(.015,.052,.012),white,.003)
 book=box('Notebook',(-1.22,-.14,2.17),(.54,.72,.045),blue,.025);book.rotation_euler.z=.12
 cylinder('Pen',(-1.32,-.42,2.2),(-1.16,.12,2.2),.015,edge)
 # Warm task lamp.
 cylinder('Lamp base',(-1.83,.74,2.13),(-1.83,.74,2.19),.22,graphite)
 cylinder('Lamp lower arm',(-1.83,.74,2.2),(-1.83,.74,3.18),.025,edge)
 cylinder('Lamp upper arm',(-1.83,.74,3.18),(-1.34,.54,3.53),.025,edge)
 cylinder('Lamp shade',(-1.34,.54,3.48),(-1.34,.54,3.67),.22,graphite,.105)
 cylinder('Lamp diffuser',(-1.34,.54,3.464),(-1.34,.54,3.48),.196,light)
 # Ceramic pot and individually modeled leaves.
 potmat=mat('Stone ceramic',(.44,.43,.4),0,.85)
 cylinder('Plant pot',(1.87,.68,2.14),(1.87,.68,2.47),.14,potmat,.19)
 cylinder('Pot soil',(1.87,.68,2.462),(1.87,.68,2.47),.17,dark)
 for i in range(9):
  a=i*2.399;z=2.65+(i%3)*.1;end=(1.87+math.cos(a)*.21,.68+math.sin(a)*.21,z)
  cylinder('Plant stem',(1.87,.68,2.45),end,.009,green)
  leaf=sphere('Plant leaf',end,(.085,.035,.21),green,16);leaf.rotation_euler=(math.sin(a)*.7,math.cos(a)*.7,a)
 # Bring the desk to a comfortable seated working height.
 for obj in list(bpy.context.scene.objects):
  if obj.name.startswith('Floating studio platform') or obj.name.startswith('Desk foot rail'):
   continue
  if obj.name.startswith('Desk leg'):
   obj.scale.z *= (1.6-.18)/(2-.18)
   obj.location.z -= .2
  else:
   obj.location.z -= .4
 furniture_start=set(bpy.context.scene.objects)
 # Ergonomic chair, facing the desk.
 cx=-.35 if kind=='about' else -.35;cy=-1.24
 cylinder('Chair gas lift',(cx,cy,.25),(cx,cy,.97),.06,edge)
 for i in range(5):
  a=i*math.tau/5;ex=cx+math.cos(a)*.57;ey=cy+math.sin(a)*.57
  cylinder('Chair base spoke',(cx,cy,.29),(ex,ey,.21),.035,graphite)
  sphere('Chair caster',(ex,ey,.16),(.087,.087,.074),dark,16)
 box('Chair seat',(cx,cy,1.01),(.88,.83,.17),dark,.11)
 box('Chair back support',(cx,cy-.43,1.54),(.77,.14,.95),graphite,.11)
 box('Chair back cushion',(cx,cy-.34,1.59),(.67,.08,.75),pad,.04)
 box('Chair headrest',(cx,cy-.45,2.17),(.52,.16,.26),dark,.09)
 for x in [cx-.5,cx+.5]:
  cylinder('Armrest support',(x,cy,1.01),(x,cy,1.39),.035,edge)
  box('Padded armrest',(x,cy+.025,1.4),(.14,.51,.07),dark,.035)
 # Upholstery piping, shaped lumbar pad and a stitched headrest.
 for side in [-1,1]:
  curve('Backrest seam',[(cx+side*.29,cy-.285,1.24),(cx+side*.32,cy-.28,1.59),(cx+side*.25,cy-.285,1.92)],.006,edge)
  sphere('Backrest side bolster',(cx+side*.34,cy-.31,1.58),(.075,.10,.38),dark)
 sphere('Lumbar cushion',(cx,cy-.25,1.32),(.30,.095,.13),pad)
 curve('Seat piping',[(cx-.37,cy+.30,1.08),(cx,cy+.37,1.08),(cx+.37,cy+.30,1.08)],.007,edge)
 for i in range(9):box('Headrest stitch',(cx-.2+i*.05,cy-.358,2.17),(.018,.003,.003),edge,.001)
 if kind=='about':
  # Anatomical landmarks are defined in the final seated pose, so shoulders,
  # elbows and wrists cannot separate when the torso reclines.
  def sculpt(name, objects, material, voxel=.018):
   bpy.ops.object.select_all(action='DESELECT')
   for o in objects:o.select_set(True)
   bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();o=bpy.context.object;o.name=name
   rem=o.modifiers.new('Continuous sculpted surface','REMESH');rem.mode='VOXEL';rem.voxel_size=voxel;rem.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=rem.name)
   sm=o.modifiers.new('Relax sculpt','SMOOTH');sm.factor=.8;sm.iterations=5;bpy.ops.object.modifier_apply(modifier=sm.name)
   for poly in o.data.polygons:poly.use_smooth=True
   return o
  parts=[]
  parts.append(sphere('Body waist',(cx,cy+.035,1.28),(.285,.215,.22),shirt))
  parts.append(sphere('Body chest',(cx,cy-.06,1.59),(.315,.21,.37),shirt))
  parts.append(sphere('Body shoulders',(cx,cy-.11,1.83),(.33,.185,.17),shirt))
  # Slightly sloping shoulders connect into sleeves, with bent elbows resting on arms.
  for side in [-1,1]:
   shoulder=(cx+side*.275,cy-.09,1.80);elbow=(cx+side*.405,cy+.015,1.43);wrist=(cx+side*.43,cy+.34,1.40)
   parts.append(sphere('Shoulder blend',shoulder,(.125,.135,.145),shirt))
   parts.append(cylinder('Upper sleeve',shoulder,elbow,.113,shirt,.10))
   parts.append(sphere('Elbow blend',elbow,(.106,.108,.105),shirt))
   parts.append(cylinder('Lower sleeve',elbow,wrist,.10,shirt,.074))
   cylinder('Ribbed cuff',(wrist[0],wrist[1]-.03,wrist[2]),(wrist[0],wrist[1]+.035,wrist[2]),.077,pad)
   handparts=[sphere('Palm',(wrist[0],wrist[1]+.09,wrist[2]-.009),(.066,.09,.037),skin)]
   for finger in range(4):
    x=wrist[0]-.046+finger*.030
    handparts.append(curve('Finger',[(x,wrist[1]+.11,wrist[2]),(x,wrist[1]+.19,wrist[2]-.025),(x,wrist[1]+.18,wrist[2]-.06)],.014,skin))
   handparts.append(curve('Thumb',[(wrist[0]-side*.053,wrist[1]+.07,wrist[2]),(wrist[0]-side*.085,wrist[1]+.12,wrist[2]-.022)],.021,skin))
   sculpt('Sculpted hand',handparts,skin,.009)
  sculpt('Continuous sweatshirt',parts,shirt)
  # Collar, exposed neck, and head pivot have an overlapping attachment.
  sphere('Sweater collar',(cx,cy-.12,1.92),(.135,.12,.065),pad)
  cylinder('Neck',(cx,cy-.12,1.91),(cx,cy-.12,2.08),.092,skin)
  bpy.ops.object.empty_add(location=(cx,cy-.12,2.035));pivot=bpy.context.object;pivot.name='Quiet breathing head'
  bpy.context.view_layer.update()
  def headpart(o):
   bpy.context.view_layer.update();world=o.matrix_world.copy();o.parent=pivot;o.matrix_world=world;return o
  hy=cy-.105
  headparts=[sphere('Cranium',(cx,hy,2.235),(.177,.163,.221),skin,32),sphere('Jaw',(cx,hy+.034,2.13),(.143,.139,.122),skin,32),sphere('Chin',(cx,hy+.09,2.087),(.084,.087,.049),skin,24),sphere('Nose bridge',(cx,hy+.155,2.216),(.025,.033,.060),skin,24),sphere('Nose tip',(cx,hy+.181,2.187),(.036,.039,.030),skin,24)]
  headpart(sculpt('Sculpted face and jaw',headparts,skin,.009))
  headpart(sphere('Swept hair',(cx,hy-.018,2.385),(.184,.165,.104),hair,32))
  for i in range(11):
   x=cx-.145+i*.028
   headpart(curve('Hair strand',[(x,hy+.102,2.415),(x+.023,hy+.01,2.475),(x+.012,hy-.098,2.409)],.009,hair))
  for side in [-1,1]:
   x=cx+side*.065
   headpart(curve('Lowered eyelid',[(x-.021,hy+.174,2.238),(x,hy+.181,2.229),(x+.021,hy+.174,2.238)],.004,hair))
   headpart(curve('Worried brow',[(x-side*.026,hy+.172,2.274),(x,hy+.177,2.265),(x+side*.026,hy+.168,2.255)],.006,hair))
   headpart(sphere('Ear',(cx+side*.169,hy,2.221),(.027,.042,.060),skin))
   headpart(sphere('Headphone pad',(cx+side*.199,hy-.007,2.24),(.040,.085,.10),dark))
   headpart(sphere('Headphone shell',(cx+side*.222,hy-.007,2.24),(.029,.077,.091),edge))
  headpart(curve('Downturned lips',[(cx-.035,hy+.179,2.130),(cx,hy+.186,2.139),(cx+.035,hy+.179,2.130)],.0035,hair))
  headpart(curve('Continuous headphone band',[(cx-.221,hy-.007,2.26),(cx-.185,hy-.007,2.435),(cx,hy-.007,2.496),(cx+.185,hy-.007,2.435),(cx+.221,hy-.007,2.26)],.018,graphite))
  legparts=[sphere('Pelvis',(cx,cy+.07,1.15),(.29,.25,.19),jeans)]
  for side in [-1,1]:
   hip=(cx+side*.16,cy+.10,1.15);knee=(cx+side*.20,cy+.65,1.06);ankle=(cx+side*.23,cy+.82,.31)
   legparts.extend([cylinder('Thigh',hip,knee,.136,jeans,.111),sphere('Knee',knee,(.113,.12,.112),jeans),cylinder('Shin',knee,ankle,.107,jeans,.073)])
   box('Sneaker',(cx+side*.23,cy+.92,.248),(.205,.38,.15),shoe,.065)
   box('Shoe sole',(cx+side*.23,cy+.92,.18),(.213,.39,.035),white,.015)
   for i in range(4):curve('Shoelace',[(cx+side*.23-.058,cy+.87+i*.032,.324),(cx+side*.23+.058,cy+.885+i*.032,.324)],.006,white)
  sculpt('Continuous trousers',legparts,jeans)
  # All upper-body points already incorporate the recline. Animate only a
  # small chin-down movement, relative to the neck, with no post-keyframe transforms.
  for frame,angle in [(1,.28),(55,.30),(110,.28),(160,.28)]:
   pivot.rotation_euler=(angle,0,-.055);pivot.keyframe_insert(data_path='rotation_euler',frame=frame)
  bpy.context.scene.frame_start=1;bpy.context.scene.frame_end=160;bpy.context.scene.frame_set(1)
 else:
  for x in [cx-.21,cx+.21]:sphere('Desk headphones',(x,cy+.04,1.16),(.065,.115,.08),edge)
  curve('Resting headphone band',[(cx-.21,cy+.04,1.16),(cx,cy+.28,1.16),(cx+.21,cy+.04,1.16)],.022,graphite)
 # Studio lighting and camera for the editable source and fallback image.
 world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.13,.17,.24,1);world.node_tree.nodes['Background'].inputs[1].default_value=.45
 def area(name,loc,power,color,size):
  bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.color=color;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1.4))-o.location).to_track_quat('-Z','Y').to_euler()
 area('Large softbox',(1,-4,7),850,(.8,.88,1),5)
 area('Blue rim',(2,4,5),1100,(.42,.61,1),4)
 area('Warm fill',(-4,-1,4),650,(1,.79,.55),4)
 bpy.ops.object.camera_add(location=(6.5,-8.5,6.5));cam=bpy.context.object;cam.name='Presentation camera';cam.rotation_euler=(Vector((0,-.2,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=7.4;bpy.context.scene.camera=cam
 sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=40;sc.cycles.use_denoising=True;sc.render.resolution_x=1000;sc.render.resolution_y=900;sc.render.resolution_percentage=100;sc.render.film_transparent=True;sc.view_settings.view_transform='AgX'
 bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender'/f'{kind}-workspace.blend'))
 # Batch static objects by material for fewer web draw calls.
 # Editable .blend above preserves each original named object.
 batches={}
 for obj in list(bpy.context.scene.objects):
  if obj.type=='MESH' and obj.parent is None and len(obj.data.materials)==1:
   batches.setdefault(obj.data.materials[0].name,[]).append(obj)
 for name,objects in batches.items():
  if len(objects)<2:continue
  bpy.ops.object.select_all(action='DESELECT')
  for obj in objects:obj.select_set(True)
  bpy.context.view_layer.objects.active=objects[0]
  bpy.ops.object.join();bpy.context.object.name='Web batch - '+name
 bpy.ops.export_scene.gltf(filepath=str(MODELS/f'{kind}-workspace.glb'),export_format='GLB',export_cameras=False,export_lights=False,export_animations=kind=='about',export_image_format='AUTO',export_yup=True)
 sc.render.filepath=str(MODELS/f'{kind}-preview.png');bpy.ops.render.render(write_still=True)

if __name__=='__main__':
 scene('hero');scene('about')
