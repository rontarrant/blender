
# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	  See the
# GNU General Public License for more details.
#
# If you have Internet access, you can find the license text at
# http://www.gnu.org/licenses/gpl.txt,
# if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------

__bpydoc__ = """\
CreaPrim does what it says. I takes the active object and turns it into an Add Mesh addon.	  When you
enable this, your custom object will be added to the Add->Mesh menu.


Documentation

Go to User Preferences->Addons and enable the CreaPrim addon in the Object section.
First select your object or objects.  The addon will show up in the 3dview properties panel.	
The name (in panel) will be set to the active object name.	  Select "Apply transform" if you
want transforms to be applied to the selected objects.	  Modifiers will taken into account.
You can always change this. Just hit the button and the selected
objects will be saved in your addons folder as an Add Mesh addon with the name 
"add_mesh_XXXX.py" with XXXX being your object name.  The addon will show up in User
Preferences->Addons in the Add Mesh section.  
Enable this addon et voila, your new custom primitive will now show up in the Add Mesh menu.

REMARK - dont need to be admin anymore - saves to user scripts dir
			
ALSO - dont forget to Apply rotation and scale to have your object show up correctly
"""

bl_info = {
	"name": "CreaPrim",
	"author": "Gert De Roost",
	"version": (0, 8, 0),
	"blender": (2, 80, 0),
	"location": "View3D > Object Tools",
	"description": "Create primitive addon",
	"warning": "",
	"wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"\
		"Scripts",
	"tracker_url": "https://projects.blender.org/tracker/index.php?"\
		"func=detail&aid=32801",
	"category": "Object"}

if "bpy" in locals():
	import imp


import bpy
import bmesh
import os


started = 0
oldname = ""
single = True


class MyProps(bpy.types.PropertyGroup):
	icons = ["NONE", "QUESTION", "ERROR", "CANCEL", "TRIA_RIGHT", "TRIA_DOWN", "TRIA_LEFT", "TRIA_UP", "ARROW_LEFTRIGHT", "PLUS", "DISCLOSURE_TRI_RIGHT", "DISCLOSURE_TRI_DOWN", "RADIOBUT_OFF", "RADIOBUT_ON", "MENU_PANEL", "BLENDER", "GRIP", "DOT", "COLLAPSEMENU", "X", "DUPLICATE", "TRASH", "COLLECTION_NEW", "NODE", "NODE_SEL", "WINDOW", "WORKSPACE", "RIGHTARROW_THIN", "BORDERMOVE", "VIEWZOOM", "ADD", "REMOVE", "PANEL_CLOSE", "COPY_ID", "EYEDROPPER", "CHECKMARK", "AUTO", "CHECKBOX_DEHLT", "CHECKBOX_HLT", "UNLOCKED", "LOCKED", "UNPINNED", "PINNED", "SCREEN_BACK", "RIGHTARROW", "DOWNARROW_HLT", "FCURVE_SNAPSHOT", "OBJECT_HIDDEN", "PLUGIN", "HELP", "GHOST_ENABLED", "COLOR", "UNLINKED", "LINKED", "HAND", "ZOOM_ALL", "ZOOM_SELECTED", "ZOOM_PREVIOUS", "ZOOM_IN", "ZOOM_OUT", "DRIVER_DISTANCE", "DRIVER_ROTATIONAL_DIFFERENCE", "DRIVER_TRANSFORM", "FREEZE", "STYLUS_PRESSURE", "GHOST_DISABLED", "FILE_NEW", "FILE_TICK", "QUIT", "URL", "RECOVER_LAST", "THREE_DOTS", "FULLSCREEN_ENTER", "FULLSCREEN_EXIT", "LIGHT", "MATERIAL", "TEXTURE", "ANIM", "WORLD", "SCENE", "OUTPUT", "SCRIPT", "PARTICLES", "PHYSICS", "SPEAKER", "TOOL_SETTINGS", "SHADERFX", "MODIFIER", "BLANK1", "FAKE_USER_OFF", "FAKE_USER_ON", "VIEW3D", "GRAPH", "OUTLINER", "PROPERTIES", "FILEBROWSER", "IMAGE", "INFO", "SEQUENCE", "TEXT", "SOUND", "ACTION", "NLA", "PREFERENCES", "TIME", "NODETREE", "CONSOLE", "TRACKER", "ASSET_MANAGER", "NODE_COMPOSITING", "NODE_TEXTURE", "NODE_MATERIAL", "UV", "OBJECT_DATAMODE", "EDITMODE_HLT", "UV_DATA", "VPAINT_HLT", "TPAINT_HLT", "WPAINT_HLT", "SCULPTMODE_HLT", "POSE_HLT", "PARTICLEMODE", "TRACKING", "TRACKING_BACKWARDS", "TRACKING_FORWARDS", "TRACKING_BACKWARDS_SINGLE", "TRACKING_FORWARDS_SINGLE", "TRACKING_CLEAR_BACKWARDS", "TRACKING_CLEAR_FORWARDS", "TRACKING_REFINE_BACKWARDS", "TRACKING_REFINE_FORWARDS", "SCENE_DATA", "RENDERLAYERS", "WORLD_DATA", "OBJECT_DATA", "MESH_DATA", "CURVE_DATA", "META_DATA", "LATTICE_DATA", "LIGHT_DATA", "MATERIAL_DATA", "TEXTURE_DATA", "ANIM_DATA", "CAMERA_DATA", "PARTICLE_DATA", "LIBRARY_DATA_DIRECT", "GROUP", "ARMATURE_DATA", "COMMUNITY", "BONE_DATA", "CONSTRAINT", "SHAPEKEY_DATA", "CONSTRAINT_BONE", "CAMERA_STEREO", "PACKAGE", "UGLYPACKAGE", "EXPERIMENTAL", "BRUSH_DATA", "IMAGE_DATA", "FILE", "FCURVE", "FONT_DATA", "RENDER_RESULT", "SURFACE_DATA", "EMPTY_DATA", "PRESET", "RENDER_ANIMATION", "RENDER_STILL", "LIBRARY_DATA_BROKEN", "BOIDS", "STRANDS", "LIBRARY_DATA_INDIRECT", "GREASEPENCIL", "LINE_DATA", "LIBRARY_DATA_OVERRIDE", "GROUP_BONE", "GROUP_VERTEX", "GROUP_VCOL", "GROUP_UVS", "FACE_MAPS", "RNA", "RNA_ADD", "MOUSE_LMB", "MOUSE_MMB", "MOUSE_RMB", "MOUSE_MOVE", "MOUSE_LMB_DRAG", "MOUSE_MMB_DRAG", "MOUSE_RMB_DRAG", "PRESET_NEW", "DECORATE", "DECORATE_KEYFRAME", "DECORATE_ANIMATE", "DECORATE_DRIVER", "DECORATE_LINKED", "DECORATE_LIBRARY_OVERRIDE", "DECORATE_UNLOCKED", "DECORATE_LOCKED", "DECORATE_OVERRIDE", "FUND", "TRACKER_DATA", "HEART", "ORPHAN_DATA", "USER", "SYSTEM", "SETTINGS", "OUTLINER_OB_EMPTY", "OUTLINER_OB_MESH", "OUTLINER_OB_CURVE", "OUTLINER_OB_LATTICE", "OUTLINER_OB_META", "OUTLINER_OB_LIGHT", "OUTLINER_OB_CAMERA", "OUTLINER_OB_ARMATURE", "OUTLINER_OB_FONT", "OUTLINER_OB_SURFACE", "OUTLINER_OB_SPEAKER", "OUTLINER_OB_FORCE_FIELD", "OUTLINER_OB_GROUP_INSTANCE", "OUTLINER_OB_GREASEPENCIL", "OUTLINER_OB_LIGHTPROBE", "OUTLINER_OB_IMAGE", "RESTRICT_COLOR_OFF", "RESTRICT_COLOR_ON", "HIDE_ON", "HIDE_OFF", "RESTRICT_SELECT_ON", "RESTRICT_SELECT_OFF", "RESTRICT_RENDER_ON", "RESTRICT_RENDER_OFF", "RESTRICT_INSTANCED_OFF", "OUTLINER_DATA_EMPTY", "OUTLINER_DATA_MESH", "OUTLINER_DATA_CURVE", "OUTLINER_DATA_LATTICE", "OUTLINER_DATA_META", "OUTLINER_DATA_LIGHT", "OUTLINER_DATA_CAMERA", "OUTLINER_DATA_ARMATURE", "OUTLINER_DATA_FONT", "OUTLINER_DATA_SURFACE", "OUTLINER_DATA_SPEAKER", "OUTLINER_DATA_LIGHTPROBE", "OUTLINER_DATA_GP_LAYER", "OUTLINER_DATA_GREASEPENCIL", "GP_SELECT_POINTS", "GP_SELECT_STROKES", "GP_MULTIFRAME_EDITING", "GP_ONLY_SELECTED", "GP_SELECT_BETWEEN_STROKES", "MODIFIER_OFF", "MODIFIER_ON", "ONIONSKIN_OFF", "ONIONSKIN_ON", "RESTRICT_VIEW_ON", "RESTRICT_VIEW_OFF", "RESTRICT_INSTANCED_ON", "MESH_PLANE", "MESH_CUBE", "MESH_CIRCLE", "MESH_UVSPHERE", "MESH_ICOSPHERE", "MESH_GRID", "MESH_MONKEY", "MESH_CYLINDER", "MESH_TORUS", "MESH_CONE", "MESH_CAPSULE", "EMPTY_SINGLE_ARROW", "LIGHT_POINT", "LIGHT_SUN", "LIGHT_SPOT", "LIGHT_HEMI", "LIGHT_AREA", "CUBE", "SPHERE", "CONE", "META_PLANE", "META_CUBE", "META_BALL", "META_ELLIPSOID", "META_CAPSULE", "SURFACE_NCURVE", "SURFACE_NCIRCLE", "SURFACE_NSURFACE", "SURFACE_NCYLINDER", "SURFACE_NSPHERE", "SURFACE_NTORUS", "EMPTY_AXIS", "STROKE", "EMPTY_ARROWS", "CURVE_BEZCURVE", "CURVE_BEZCIRCLE", "CURVE_NCURVE", "CURVE_NCIRCLE", "CURVE_PATH", "LIGHTPROBE_CUBEMAP", "LIGHTPROBE_PLANAR", "LIGHTPROBE_GRID", "COLOR_RED", "COLOR_GREEN", "COLOR_BLUE", "TRIA_RIGHT_BAR", "TRIA_DOWN_BAR", "TRIA_LEFT_BAR", "TRIA_UP_BAR", "FORCE_FORCE", "FORCE_WIND", "FORCE_VORTEX", "FORCE_MAGNETIC", "FORCE_HARMONIC", "FORCE_CHARGE", "FORCE_LENNARDJONES", "FORCE_TEXTURE", "FORCE_CURVE", "FORCE_BOID", "FORCE_TURBULENCE", "FORCE_DRAG", "FORCE_SMOKEFLOW", "RIGID_BODY", "RIGID_BODY_CONSTRAINT", "IMAGE_PLANE", "IMAGE_BACKGROUND", "IMAGE_REFERENCE", "NODE_INSERT_ON", "NODE_INSERT_OFF", "NODE_TOP", "NODE_SIDE", "NODE_CORNER", "SELECT_SET", "SELECT_EXTEND", "SELECT_SUBTRACT", "SELECT_INTERSECT", "SELECT_DIFFERENCE", "ALIGN_LEFT", "ALIGN_CENTER", "ALIGN_RIGHT", "ALIGN_JUSTIFY", "ALIGN_FLUSH", "ALIGN_TOP", "ALIGN_MIDDLE", "ALIGN_BOTTOM", "BOLD", "ITALIC", "UNDERLINE", "SMALL_CAPS", "CON_ACTION", "HOLDOUT_OFF", "HOLDOUT_ON", "INDIRECT_ONLY_OFF", "INDIRECT_ONLY_ON", "CON_CAMERASOLVER", "CON_FOLLOWTRACK", "CON_OBJECTSOLVER", "CON_LOCLIKE", "CON_ROTLIKE", "CON_SIZELIKE", "CON_TRANSLIKE", "CON_DISTLIMIT", "CON_LOCLIMIT", "CON_ROTLIMIT", "CON_SIZELIMIT", "CON_SAMEVOL", "CON_TRANSFORM", "CON_TRANSFORM_CACHE", "CON_CLAMPTO", "CON_KINEMATIC", "CON_LOCKTRACK", "CON_SPLINEIK", "CON_STRETCHTO", "CON_TRACKTO", "CON_ARMATURE", "CON_CHILDOF", "CON_FLOOR", "CON_FOLLOWPATH", "CON_PIVOT", "CON_SHRINKWRAP", "MODIFIER_DATA", "MOD_WAVE", "MOD_BUILD", "MOD_DECIM", "MOD_MIRROR", "MOD_SOFT", "MOD_SUBSURF", "HOOK", "MOD_PHYSICS", "MOD_PARTICLES", "MOD_BOOLEAN", "MOD_EDGESPLIT", "MOD_ARRAY", "MOD_UVPROJECT", "MOD_DISPLACE", "MOD_CURVE", "MOD_LATTICE", "MOD_TINT", "MOD_ARMATURE", "MOD_SHRINKWRAP", "MOD_CAST", "MOD_MESHDEFORM", "MOD_BEVEL", "MOD_SMOOTH", "MOD_SIMPLEDEFORM", "MOD_MASK", "MOD_CLOTH", "MOD_EXPLODE", "MOD_FLUIDSIM", "MOD_MULTIRES", "MOD_SMOKE", "MOD_SOLIDIFY", "MOD_SCREW", "MOD_VERTEX_WEIGHT", "MOD_DYNAMICPAINT", "MOD_REMESH", "MOD_OCEAN", "MOD_WARP", "MOD_SKIN", "MOD_TRIANGULATE", "MOD_WIREFRAME", "MOD_DATA_TRANSFER", "MOD_NORMALEDIT", "MOD_PARTICLE_INSTANCE", "MOD_HUE_SATURATION", "MOD_NOISE", "MOD_OFFSET", "MOD_SIMPLIFY", "MOD_THICKNESS", "MOD_INSTANCE", "MOD_TIME", "MOD_OPACITY", "REC", "PLAY", "FF", "REW", "PAUSE", "PREV_KEYFRAME", "NEXT_KEYFRAME", "PLAY_SOUND", "PLAY_REVERSE", "PREVIEW_RANGE", "ACTION_TWEAK", "PMARKER_ACT", "PMARKER_SEL", "PMARKER", "MARKER_HLT", "MARKER", "KEYFRAME_HLT", "KEYFRAME", "KEYINGSET", "KEY_DEHLT", "KEY_HLT", "MUTE_IPO_OFF", "MUTE_IPO_ON", "DRIVER", "SOLO_OFF", "SOLO_ON", "FRAME_PREV", "FRAME_NEXT", "NLA_PUSHDOWN", "IPO_CONSTANT", "IPO_LINEAR", "IPO_BEZIER", "IPO_SINE", "IPO_QUAD", "IPO_CUBIC", "IPO_QUART", "IPO_QUINT", "IPO_EXPO", "IPO_CIRC", "IPO_BOUNCE", "IPO_ELASTIC", "IPO_BACK", "IPO_EASE_IN", "IPO_EASE_OUT", "IPO_EASE_IN_OUT", "NORMALIZE_FCURVES", "VERTEXSEL", "EDGESEL", "FACESEL", "CURSOR", "PIVOT_BOUNDBOX", "PIVOT_CURSOR", "PIVOT_INDIVIDUAL", "PIVOT_MEDIAN", "PIVOT_ACTIVE", "CENTER_ONLY", "ROOTCURVE", "SMOOTHCURVE", "SPHERECURVE", "INVERSESQUARECURVE", "SHARPCURVE", "LINCURVE", "NOCURVE", "RNDCURVE", "PROP_OFF", "PROP_ON", "PROP_CON", "PROP_PROJECTED", "PARTICLE_POINT", "PARTICLE_TIP", "PARTICLE_PATH", "SNAP_FACE_CENTER", "SNAP_PERPENDICULAR", "SNAP_MIDPOINT", "SNAP_OFF", "SNAP_ON", "SNAP_NORMAL", "SNAP_GRID", "SNAP_VERTEX", "SNAP_EDGE", "SNAP_FACE", "SNAP_VOLUME", "SNAP_INCREMENT", "STICKY_UVS_LOC", "STICKY_UVS_DISABLE", "STICKY_UVS_VERT", "CLIPUV_DEHLT", "CLIPUV_HLT", "SNAP_PEEL_OBJECT", "GRID", "OBJECT_ORIGIN", "ORIENTATION_GLOBAL", "ORIENTATION_GIMBAL", "ORIENTATION_LOCAL", "ORIENTATION_NORMAL", "ORIENTATION_VIEW", "COPYDOWN", "PASTEDOWN", "PASTEFLIPUP", "PASTEFLIPDOWN", "VIS_SEL_11", "VIS_SEL_10", "VIS_SEL_01", "VIS_SEL_00", "AUTOMERGE_OFF", "AUTOMERGE_ON", "UV_VERTEXSEL", "UV_EDGESEL", "UV_FACESEL", "UV_ISLANDSEL", "UV_SYNC_SELECT", "TRANSFORM_ORIGINS", "GIZMO", "ORIENTATION_CURSOR", "NORMALS_VERTEX", "NORMALS_FACE", "NORMALS_VERTEX_FACE", "SHADING_BBOX", "SHADING_WIRE", "SHADING_SOLID", "SHADING_RENDERED", "SHADING_TEXTURE", "OVERLAY", "XRAY", "LOCKVIEW_OFF", "LOCKVIEW_ON", "AXIS_SIDE", "AXIS_FRONT", "AXIS_TOP", "NDOF_DOM", "NDOF_TURN", "NDOF_FLY", "NDOF_TRANS", "LAYER_USED", "LAYER_ACTIVE", "SORTALPHA", "SORTBYEXT", "SORTTIME", "SORTSIZE", "SHORTDISPLAY", "LONGDISPLAY", "IMGDISPLAY", "BOOKMARKS", "FONTPREVIEW", "FILTER", "NEWFOLDER", "FILE_PARENT", "FILE_REFRESH", "FILE_FOLDER", "FILE_BLANK", "FILE_BLEND", "FILE_IMAGE", "FILE_MOVIE", "FILE_SCRIPT", "FILE_SOUND", "FILE_FONT", "FILE_TEXT", "SORT_DESC", "SORT_ASC", "LINK_BLEND", "APPEND_BLEND", "IMPORT", "EXPORT", "LOOP_BACK", "LOOP_FORWARDS", "BACK", "FORWARD", "FILE_ARCHIVE", "FILE_CACHE", "FILE_VOLUME", "FILE_3D", "FILE_HIDDEN", "FILE_BACKUP", "DISK_DRIVE", "MATPLANE", "MATSPHERE", "MATCUBE", "MONKEY", "HAIR", "ALIASED", "ANTIALIASED", "MAT_SPHERE_SKY", "MATSHADERBALL", "MATCLOTH", "MATFLUID", "WORDWRAP_OFF", "WORDWRAP_ON", "SYNTAX_OFF", "SYNTAX_ON", "LINENUMBERS_OFF", "LINENUMBERS_ON", "SCRIPTPLUGINS", "DESKTOP", "EXTERNAL_DRIVE", "NETWORK_DRIVE", "SEQ_SEQUENCER", "SEQ_PREVIEW", "SEQ_LUMA_WAVEFORM", "SEQ_CHROMA_SCOPE", "SEQ_HISTOGRAM", "SEQ_SPLITVIEW", "SEQ_STRIP_META", "SEQ_STRIP_DUPLICATE", "IMAGE_RGB", "IMAGE_RGB_ALPHA", "IMAGE_ALPHA", "IMAGE_ZDEPTH", "VIEW_PERSPECTIVE", "VIEW_ORTHO", "VIEW_CAMERA", "VIEW_PAN", "VIEW_ZOOM", "BRUSH_BLOB", "BRUSH_BLUR", "BRUSH_CLAY", "BRUSH_CLAY_STRIPS", "BRUSH_CLONE", "BRUSH_CREASE", "BRUSH_FILL", "BRUSH_FLATTEN", "BRUSH_GRAB", "BRUSH_INFLATE", "BRUSH_LAYER", "BRUSH_MASK", "BRUSH_MIX", "BRUSH_NUDGE", "BRUSH_PINCH", "BRUSH_SCRAPE", "BRUSH_SCULPT_DRAW", "BRUSH_SMEAR", "BRUSH_SMOOTH", "BRUSH_SNAKE_HOOK", "BRUSH_SOFTEN", "BRUSH_TEXDRAW", "BRUSH_TEXFILL", "BRUSH_TEXMASK", "BRUSH_THUMB", "BRUSH_ROTATE", "GPBRUSH_SMOOTH", "GPBRUSH_THICKNESS", "GPBRUSH_STRENGTH", "GPBRUSH_GRAB", "GPBRUSH_PUSH", "GPBRUSH_TWIST", "GPBRUSH_PINCH", "GPBRUSH_RANDOMIZE", "GPBRUSH_CLONE", "GPBRUSH_WEIGHT", "GPBRUSH_PENCIL", "GPBRUSH_PEN", "GPBRUSH_INK", "GPBRUSH_INKNOISE", "GPBRUSH_BLOCK", "GPBRUSH_MARKER", "GPBRUSH_FILL", "GPBRUSH_AIRBRUSH", "GPBRUSH_CHISEL", "GPBRUSH_ERASE_SOFT", "GPBRUSH_ERASE_HARD", "GPBRUSH_ERASE_STROKE", "SMALL_TRI_RIGHT_VEC", "KEYTYPE_KEYFRAME_VEC", "KEYTYPE_BREAKDOWN_VEC", "KEYTYPE_EXTREME_VEC", "KEYTYPE_JITTER_VEC", "KEYTYPE_MOVING_HOLD_VEC", "HANDLETYPE_FREE_VEC", "HANDLETYPE_ALIGNED_VEC", "HANDLETYPE_VECTOR_VEC", "HANDLETYPE_AUTO_VEC", "HANDLETYPE_AUTO_CLAMP_VEC", "COLORSET_01_VEC", "COLORSET_02_VEC", "COLORSET_03_VEC", "COLORSET_04_VEC", "COLORSET_05_VEC", "COLORSET_06_VEC", "COLORSET_07_VEC", "COLORSET_08_VEC", "COLORSET_09_VEC", "COLORSET_10_VEC", "COLORSET_11_VEC", "COLORSET_12_VEC", "COLORSET_13_VEC", "COLORSET_14_VEC", "COLORSET_15_VEC", "COLORSET_16_VEC", "COLORSET_17_VEC", "COLORSET_18_VEC", "COLORSET_19_VEC", "COLORSET_20_VEC", "EVENT_A", "EVENT_B", "EVENT_C", "EVENT_D", "EVENT_E", "EVENT_F", "EVENT_G", "EVENT_H", "EVENT_I", "EVENT_J", "EVENT_K", "EVENT_L", "EVENT_M", "EVENT_N", "EVENT_O", "EVENT_P", "EVENT_Q", "EVENT_R", "EVENT_S", "EVENT_T", "EVENT_U", "EVENT_V", "EVENT_W", "EVENT_X", "EVENT_Y", "EVENT_Z", "EVENT_SHIFT", "EVENT_CTRL", "EVENT_ALT", "EVENT_OS", "EVENT_F1", "EVENT_F2", "EVENT_F3", "EVENT_F4", "EVENT_F5", "EVENT_F6", "EVENT_F7", "EVENT_F8", "EVENT_F9", "EVENT_F10", "EVENT_F11", "EVENT_F12", "EVENT_ESC", "EVENT_TAB", "EVENT_PAGEUP", "EVENT_PAGEDOWN", "EVENT_RETURN", "EVENT_SPACEKEY"]
	
	# items = [];
	items = []
	
	for i, icon in enumerate(icons):
		items.append((icon, "", icon, icon, i + 1))

	#Icon = bpy.props.EnumProperty(
	Icon:bpy.props.EnumProperty(

				items = items,
				name="Icon",
				description="icon for primitive")
	
	#Name = bpy.props.StringProperty(
	Name:bpy.props.StringProperty(
				name="Name",
				description="name for primitive",
				maxlen= 1024)
	
	#Apply = bpy.props.BoolProperty(
	Apply:bpy.props.BoolProperty(
			name = "Apply transform", 
			description = "apply transform to selected objects",
			default = False)


def message_draw(self, context):
	
	global groupname
	
	layout = self.layout
	row = layout.row()
	row.label(text = message)
		
		
class PANEL_PT_CreaPrimPanel(bpy.types.Panel):
	bl_label = "CreaPrim"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = 'CreaPrim'

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return (obj and obj.type == 'MESH' and context.mode == 'OBJECT')

	def draw(self, context):
   
		scn = context.scene
		   
		self.layout.operator("object.creaprim", text="Create primitive", icon = 'PLUGIN')
		self.layout.prop(scn.my_props, "Name")
		self.layout.prop(scn.my_props, "Icon")
		self.layout.prop(scn.my_props, "Apply")


class OBJECT_OT_CreaPrim(bpy.types.Operator):
	bl_idname = "object.creaprim"
	bl_label = "CreaPrim"
	bl_description = "Create primitive addon"
	bl_options = {"REGISTER"}
	
	
	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return (obj and obj.type == 'MESH' and context.mode == 'OBJECT')

	def invoke(self, context, event):

		global oldname, groupname, message, single
		
		scn = context.scene
				
		objlist = []

		for coll in scn.collection.children:
			for selobj in coll.objects:
				if selobj.select_get() and selobj.type == 'MESH':
					objlist.append(selobj)
		direc = bpy.utils.script_path_user()
		if direc == None:
			direc = bpy.utils.script_paths()[1]
		groupname = scn.my_props.Name

		if groupname == "":
			message = "You must enter a valid Name."
			bpy.ops.creaprim.message('INVOKE_DEFAULT')
			return {"CANCELLED"}
		if len(objlist) == 0:
			return {"CANCELLED"}
		if len(objlist) > 1:
			groupname = groupname.replace(".", "")
			addondir = direc + os.sep + "addons" + os.sep + "add_mesh_" + groupname + os.sep
			if not os.path.exists(addondir):
				os.makedirs(addondir)
		else:
			print (bpy.utils.script_paths())
			addondir = direc + os.sep + "addons" + os.sep
			print (addondir)
			if not os.path.exists(addondir):
				os.makedirs(addondir)
		actobj = bpy.context.active_object
		txtlist = []
		namelist = []
		for selobj in objlist:
			if len(objlist) == 1:
				single = True
				objname = scn.my_props.Name
				objname = objname.replace(" ", "_")
			else:
				single = False
				objname = selobj.name
				objname = objname.replace(".", "")
				objname = objname.replace(" ", "_")
				namelist.append(objname)
			mesh = selobj.to_mesh()
			oldname = selobj.name

			context.view_layer.objects.active = selobj
			if scn.my_props.Apply:
				bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
			txt = do_creaprim(self, mesh, objname, addondir)
			if txt == 0:
				return {'CANCELLED'}
			txtlist.append(txt)
		oldname = actobj.name
		context.view_layer.objects.active = actobj
		
		bpy.ops.preferences.addon_refresh()
		if len(txtlist) > 1:
			makeinit(txtlist, namelist, groupname, addondir)
			bpy.ops.preferences.addon_enable(module="add_mesh_" + groupname)
		else:
			bpy.ops.preferences.addon_enable(module="add_mesh_" + str.lower(objname))
		bpy.ops.wm.save_userpref()
			
		message = "Add Mesh addon " + groupname + " saved.  It can be found (for removal) in the Preferences->Addons->Add Mesh category."
		bpy.context.window_manager.popup_menu(message_draw, title="Confirmation", icon='INFO')
		
		
		context.window_manager.modal_handler_add(self)

		wm = context.window_manager
		self._timer = wm.event_timer_add(time_step=0.1, window=context.window)
		
		return {'FINISHED'}


	def modal(self, context, event):
	
		if event.type == 'TIMER':
			setname(1)
			
		return {'PASS_THROUGH'}
		
		

		
def setname(dummy):
	
	global oldname
	
	scn = bpy.context.scene
	
	if bpy.context.active_object != None and bpy.context.active_object.name != oldname:
		scn.my_props.Name = bpy.context.active_object.name
		oldname = scn.my_props.Name
	

classes = (
	MyProps,
	OBJECT_OT_CreaPrim,
	PANEL_PT_CreaPrimPanel,
)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
	bpy.types.Scene.my_props = bpy.props.PointerProperty(type=MyProps)
	
def unregister():
	from bpy.utils import unregister_class
	for cls in classes:
		unregister_class(cls)

if __name__ == "__main__":
	register()




def do_creaprim(self, mesh, objname, addondir):
	
	global message
	
	scn = bpy.context.scene
	objname = objname.replace(".", "")
	objname = objname.replace(" ", "_")
	bm = bmesh.new()
	bm.from_mesh(mesh)	  
	
	
	try:
		txt = bpy.data.texts[str.lower("add_mesh_" + objname) + ".py"]
		txt.clear()
	except:
		txt = bpy.data.texts.new("add_mesh_" + str.lower(objname) + ".py")
	
	strlist = []
	strlist.append("bl_info = {\n")
	strlist.append("\"name\": \"" + objname + "\", \n")
	strlist.append("\"author\": \"Gert De Roost\",\n")
	strlist.append("\"version\": (1, 0, 0),\n")
	strlist.append("\"blender\": (2, 80, 0),\n")
	strlist.append("\"location\": \"Add > Mesh\",\n")
	strlist.append("\"description\": \"Create " + objname + " primitive.\",\n")
	strlist.append("\"warning\": \"\",\n")
	strlist.append("\"wiki_url\": \"\",\n")
	strlist.append("\"tracker_url\": \"\",\n")
	strlist.append("\"category\": \"Add Mesh\"}\n")
	strlist.append("\n")
	strlist.append("\n") 
	strlist.append("if \"bpy\" in locals():\n")
	strlist.append("	   import importlib\n")
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("import bpy\n")
	strlist.append("import bmesh\n")
	strlist.append("import math\n")
	strlist.append("from mathutils import *\n")
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("class MESH_OT_" + objname + "(bpy.types.Operator):\n")
	strlist.append("	bl_idname = \"mesh." + str.lower(objname) + "\"\n")
	strlist.append("	bl_label = \"" + objname + "\"\n")
	strlist.append("	bl_options = {\'REGISTER\', \'UNDO\'}\n")
	strlist.append("	bl_description = \"add " + objname + " primitive\"\n")
	strlist.append("\n")
	strlist.append("	def invoke(self, context, event):\n")
	strlist.append("\n")
	strlist.append("		mesh = bpy.data.meshes.new(name=\"" + objname + "\")\n")
	strlist.append("		obj = bpy.data.objects.new(name=\"" + objname + "\", object_data=mesh)\n")
	strlist.append("		scene = bpy.context.scene\n")
	strlist.append("		bpy.context.collection.objects.link(obj)\n")
	strlist.append("		obj.location = scene.cursor.location\n")
	strlist.append("		bm = bmesh.new()\n")
	strlist.append("		bm.from_mesh(mesh)\n")
	strlist.append("\n")
	strlist.append("		idxlist = []\n")
	posn = 0
	strlist.append("		vertlist = [")
	for v in bm.verts:
		if posn > 0:
			strlist.append(", ")
		posn += 1
		strlist.append(str(v.co[:]))
	strlist.append("]\n")	 
	strlist.append("		for co in vertlist:\n")
	strlist.append("			v = bm.verts.new(co)\n")
	strlist.append("			bm.verts.index_update()\n")
	strlist.append("			idxlist.append(v.index)\n")
	posn = 0
	strlist.append("		edgelist = [")
	for e in bm.edges:
		if posn > 0:
			strlist.append(", ")
		posn += 1
		strlist.append("[" + str(e.verts[0].index) + ", " + str(e.verts[1].index) + "]")
	strlist.append("]\n")	 
	strlist.append("		for verts in edgelist:\n")
	strlist.append("			try:\n")
	strlist.append("				bm.edges.new((bm.verts[verts[0]], bm.verts[verts[1]]))\n")
	strlist.append("			except:\n")
	strlist.append("				pass\n")
	posn1 = 0
	strlist.append("		facelist = [(")
	for f in bm.faces:
		if posn1 > 0:
			strlist.append(", (")
		posn1 += 1
		posn2 = 0
		for v in f.verts:
			if posn2 > 0:
				strlist.append(", ")
			strlist.append(str(v.index))
			posn2 += 1
		strlist.append(")")
	strlist.append("]\n")	 
	strlist.append("		bm.verts.ensure_lookup_table()\n")
	strlist.append("		for verts in facelist:\n")
	strlist.append("			vlist = []\n")	  
	strlist.append("			for idx in verts:\n")	 
	strlist.append("				vlist.append(bm.verts[idxlist[idx]])\n")	
	strlist.append("			try:\n")
	strlist.append("				bm.faces.new(vlist)\n")
	strlist.append("			except:\n")
	strlist.append("				pass\n")
	strlist.append("\n")
	strlist.append("		bm.to_mesh(mesh)\n")
	strlist.append("		mesh.update()\n")
	strlist.append("		bm.free()\n")	 
	strlist.append("		obj.rotation_quaternion = (Matrix.Rotation(math.radians(90), 3, \'X\').to_quaternion())\n")
	strlist.append("\n")
#	strlist.append("		from bpy_extras import object_utils\n")
#	strlist.append("		object_utils.object_data_add(context, mesh, operator=self)\n")
	strlist.append("		return {\'FINISHED\'}\n")
		
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("def menu_item(self, context):\n")	 
	strlist.append("   self.layout.operator(MESH_OT_" + objname + ".bl_idname, text=\"" + objname + "\", icon=\"" + scn.my_props.Icon + "\")\n")
	strlist.append("\n") 
	strlist.append("def register():\n")
	strlist.append("	from bpy.utils import register_class\n")
	strlist.append("	register_class(MESH_OT_" + objname + ")\n")
	strlist.append("	bpy.types.VIEW3D_MT_mesh_add.append(menu_item)\n")
	strlist.append("\n") 
	strlist.append("def unregister():\n")
	strlist.append("	bpy.types.VIEW3D_MT_mesh_add.remove(menu_item)\n")
#	strlist.append("	from bpy.utils import unregister_class\n")
#	strlist.append("	unregister_class(MESH_OT_" + objname + ")\n")
	strlist.append("\n") 
	strlist.append("if __name__ == \"__main__\":\n") 
	strlist.append("	   register()\n")	 
	endstring = ''.join(strlist)
	txt.write(endstring)
	
	try:
		fileobj = open(addondir + "add_mesh_" + str.lower(objname) + ".py", "w")
	except:
		message = "Permission problem - cant write file to folder" + addondir + "- you could run Blender as Administrator!"
		bpy.context.window_manager.popup_menu(message_draw, title="Problem", icon='INFO')
		return 0

	fileobj.write(endstring)
	fileobj.close()
	
	bm.free()
	
	return txt
	
	
def makeinit(txtlist, namelist, groupname, addondir):
	
	global message
	
	scn = bpy.context.scene

	try:
		txt = bpy.data.texts["__init__.py"]
		txt.clear()
	except:
		txt = bpy.data.texts.new("__init__.py")
	
	strlist = []
	strlist.append("bl_info = {\n")
	strlist.append("\"name\": \"" + groupname + "\", \n")
	strlist.append("\"author\": \"Gert De Roost\",\n")
	strlist.append("\"version\": (1, 0, 0),\n")
	strlist.append("\"blender\": (2, 80, 0),\n")
	strlist.append("\"location\": \"Add > Mesh\",\n")
	strlist.append("\"description\": \"Create " + groupname + " primitive group.\",\n")
	strlist.append("\"warning\": \"\",\n")
	strlist.append("\"wiki_url\": \"\",\n")
	strlist.append("\"tracker_url\": \"\",\n")
	strlist.append("\"category\": \"Add Mesh\"}\n")
	strlist.append("\n")
	strlist.append("\n") 
	strlist.append("if \"bpy\" in locals():\n")
	strlist.append("	import importlib\n")
	addonlist = []
	for txt in txtlist:
		name = txt.name.replace(".py", "")
		addonlist.append(name)
	for name in addonlist:
		strlist.append("	importlib.reload(" + name + ")\n")	
	strlist.append("else:\n")
	for name in addonlist:
		strlist.append("	from . import " + name + "\n")	  
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("import bpy\n")
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("class INFO_MT_mesh_" + str.lower(groupname) + "_add(bpy.types.Menu):\n")
	strlist.append("	bl_idname = \"INFO_MT_mesh_" + str.lower(groupname) + "_add\"\n")
	strlist.append("	bl_label = \"" + groupname + "\"\n")
	strlist.append("\n")
	strlist.append("	def draw(self, context):\n")
	strlist.append("		layout = self.layout\n")
#		  layout.operator_context = 'INVOKE_REGION_WIN'
	for name in namelist:
		strlist.append("		layout.operator(\"mesh." + str.lower(name) + "\", text=\"" + name + "\")\n")
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("\n")
	strlist.append("\n") 
	strlist.append("def menu_item(self, context):\n")	 
	strlist.append("	   self.layout.menu(\"INFO_MT_mesh_" + str.lower(groupname) + "_add\", icon=\"" + scn.my_props.Icon + "\")\n")
	strlist.append("def register():\n")
	strlist.append("	   from bpy.utils import register_class\n")
	strlist.append("	   register_class(INFO_MT_mesh_" + str.lower(groupname) + "_add)\n")
	for name in addonlist:
		strlist.append("	   " + name + ".register()\n")	  
	strlist.append("	   bpy.types.VIEW3D_MT_mesh_add.append(menu_item)\n")
	strlist.append("\n") 
	strlist.append("def unregister():\n")
	strlist.append("	   bpy.types.VIEW3D_MT_mesh_add.remove(menu_item)\n")
	for name in addonlist:
		strlist.append("	   " + name + ".unregister()\n")	  
# 	strlist.append("	   from bpy.utils import unregister_class\n")
#	strlist.append("	   unregister_class(INFO_MT_mesh_" + str.lower(groupname) + "_add)\n")
	strlist.append("\n") 
	strlist.append("if __name__ == \"__main__\":\n") 
	strlist.append("	   register()\n")	 
	endstring = ''.join(strlist)
	txt.write(endstring)
	
	try:
		fileobj = open(addondir + "__init__.py", "w")
	except:
		message = "Permission problem - cant write file to folder" + addondir + "- you could run Blender as Administrator!"
		bpy.context.window_manager.popup_menu(message_draw, title="Problem", icon='INFO')
		return 0
	fileobj.write(endstring)
	fileobj.close()




	
	

