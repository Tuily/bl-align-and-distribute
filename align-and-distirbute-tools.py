import bpy

from bpy.props import (FloatProperty)
from bpy.types import (
    Operator,
    Panel,
)


PROPS = [
    ('gap', FloatProperty(name='Gap', default=1)),
]


bl_info = {
    "name": "Align and Distribute Tools",
    "author": "tuily",
    "version": (0, 3, 4),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Item Tab",
    "description": "Align and Distribute Tools",
    "warning": "",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/object/align_tools.html",
    "category": "Object",
}


# Align Location Operator


class OBJECT_OP_AlignLocationOperator(Operator):
    bl_idname = "object.align_location"
    bl_label = "Align selected objects axis to active object axis"
    bl_description = "Align selected objects axis to active object axis"

    axis: bpy.props.StringProperty(name='axis')

    @ classmethod
    def poll(cls, context):
        validNumberOfObjects = len(bpy.context.selected_objects) > 1
        return context.active_object is not None and validNumberOfObjects

    def execute(self, context):
        axis = {'x': 0, 'y': 1, 'z': 2}[self.axis]

        activeObject = bpy.context.active_object
        activeObjectAxisValue = activeObject.matrix_world.translation[axis]

        for o in bpy.context.selected_objects:
            o.matrix_world.translation[axis] = activeObjectAxisValue

        return {'FINISHED'}

# Distribute Evenly Operator


class OBJECT_OP_DistributeEvenlyOperator(Operator):
    bl_idname = "object.distribute_evenly"
    bl_label = "Distribute selected objects evenly"
    bl_description = "Distribute selected objects evenly"

    axis: bpy.props.StringProperty(name='axis')

    @ classmethod
    def poll(cls, context):
        validNumberOfObjects = len(bpy.context.selected_objects) > 2
        return context.active_object is not None and validNumberOfObjects

    def execute(self, context):

        axis = {'x': 0, 'y': 1, 'z': 2}[self.axis]

        selectedObjects = bpy.context.selected_objects

        selectedObjects.sort(key=lambda o: o.location[axis])

        firstObjAxisValue = selectedObjects[0].matrix_world.translation[axis]

        def minMaxLambda(o): return o.location[axis]

        maxValue = max(selectedObjects, key=minMaxLambda).location[axis]
        minValue = min(selectedObjects, key=minMaxLambda).location[axis]

        length = maxValue - minValue
        spaceBetween = length / (len(selectedObjects) - 1)

        for i, o in enumerate(selectedObjects):
            o.location[axis] = firstObjAxisValue + (i * spaceBetween)

        return {'FINISHED'}

# Distribute With Gap Operator


class OBJECT_OP_DistributeWithGapOperator(Operator):
    bl_idname = "object.distribute_with_gap"
    bl_label = "Distribute selected objects with gap"
    bl_description = "Distribute selected objects with gap"

    axis: bpy.props.StringProperty(name='axis')

    @ classmethod
    def poll(cls, context):
        validNumberOfObjects = len(bpy.context.selected_objects) > 1
        return context.active_object is not None and validNumberOfObjects

    def execute(self, context):

        axis = {'x': 0, 'y': 1, 'z': 2}[self.axis]
        gap = context.scene.gap
        activeObject = bpy.context.active_object

        selectedObjects = bpy.context.selected_objects
        selectedObjects.remove(activeObject)

        if self.axis == 'x':
            selectedObjects.sort(key=lambda o: o.location.y)
            selectedObjects.sort(key=lambda o: o.location.z)
        elif self.axis == 'y':
            selectedObjects.sort(key=lambda o: o.location.x)
            selectedObjects.sort(key=lambda o: o.location.z)
        elif self.axis == 'z':
            selectedObjects.sort(key=lambda o: o.location.y)
            selectedObjects.sort(key=lambda o: o.location.x)

        for i, o in enumerate(selectedObjects):
            o.location[axis] = activeObject.location[axis] + ((i+1) * gap)

        return {'FINISHED'}


# Interface Panel

class VIEW3D_PT_AlignAndDistributePanel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Align and Distribute Tools"
    bl_context = "objectmode"
    bl_category = 'Item'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout

        # align operators
        col = layout.column()
        col.label(text="Align to active object")
        col = layout.column_flow(columns=3, align=True)

        alignX = col.operator("object.align_location", text="X")
        alignX.axis = 'x'

        alignY = col.operator("object.align_location", text="Y")
        alignY.axis = 'y'

        alignZ = col.operator("object.align_location", text="Z")
        alignZ.axis = 'z'

        # distribute evenly operators
        col = layout.column()
        col.label(text="Evenly distribute")
        col = layout.column_flow(columns=3, align=True)

        distributeX = col.operator("object.distribute_evenly", text="X")
        distributeX.axis = 'x'

        distributeY = col.operator("object.distribute_evenly", text="Y")
        distributeY.axis = 'y'

        distributeZ = col.operator("object.distribute_evenly", text="Z")
        distributeZ.axis = 'z'

        # distribute with gap operators
        col = layout.column()
        col.label(text="Distribute with gap")

        for (prop_name, _) in PROPS:
            col.prop(context.scene, prop_name)

        col = layout.column_flow(columns=3, align=True)

        distributeGapX = col.operator("object.distribute_with_gap", text="X")
        distributeGapX.axis = 'x'

        distributeGapY = col.operator("object.distribute_with_gap", text="Y")
        distributeGapY.axis = 'y'

        distributeGapZ = col.operator("object.distribute_with_gap", text="Z")
        distributeGapZ.axis = 'z'


# Class List
classes = [
    VIEW3D_PT_AlignAndDistributePanel,
    OBJECT_OP_AlignLocationOperator,
    OBJECT_OP_DistributeWithGapOperator,
    OBJECT_OP_DistributeEvenlyOperator
]

# Register all operators and panels


def register():

    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
