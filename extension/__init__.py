import bpy
from bpy.props import FloatProperty, BoolProperty
from bpy.types import (
    Operator,
    Panel,
)


PROPS = [
    ("gap", FloatProperty(name="Gap", default=1)),
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

    axis: bpy.props.StringProperty(name="axis")

    @classmethod
    def poll(cls, context):
        validNumberOfObjects = len(bpy.context.selected_objects) > 1
        return context.active_object is not None and validNumberOfObjects

    def execute(self, context):
        axis = {"x": 0, "y": 1, "z": 2}[self.axis]

        activeObject = bpy.context.active_object
        activeObjectAxisValue = activeObject.matrix_world.translation[axis]

        for o in bpy.context.selected_objects:
            o.matrix_world.translation[axis] = activeObjectAxisValue

        return {"FINISHED"}


# Distribute Evenly Operator


class OBJECT_OP_DistributeEvenlyOperator(Operator):
    bl_idname = "object.distribute_evenly"
    bl_label = "Distribute selected objects evenly"
    bl_description = "Distribute selected objects evenly"

    axis: bpy.props.StringProperty(name="axis")

    @classmethod
    def poll(cls, context):
        validNumberOfObjects = len(bpy.context.selected_objects) > 2
        return context.active_object is not None and validNumberOfObjects

    def execute(self, context):

        axis = {"x": 0, "y": 1, "z": 2}[self.axis]

        selectedObjects = bpy.context.selected_objects

        selectedObjects.sort(key=lambda o: o.location[axis])

        firstObjAxisValue = selectedObjects[0].matrix_world.translation[axis]

        def minMaxLambda(o):
            return o.location[axis]

        maxValue = max(selectedObjects, key=minMaxLambda).location[axis]
        minValue = min(selectedObjects, key=minMaxLambda).location[axis]

        length = maxValue - minValue
        spaceBetween = length / (len(selectedObjects) - 1)

        for i, o in enumerate(selectedObjects):
            o.location[axis] = firstObjAxisValue + (i * spaceBetween)

        return {"FINISHED"}


# Distribute With Gap Operator


class OBJECT_OP_DistributeWithGapOperator(Operator):
    bl_idname = "object.distribute_with_gap"
    bl_label = "Distribute selected objects with gap"
    bl_description = "Distribute selected objects with gap"

    axis: bpy.props.StringProperty(name="axis")

    @classmethod
    def poll(cls, context):
        """
        Ensure the operator is only available when there are more than one selected object
        and an active object is present.
        """
        validNumberOfObjects = len(bpy.context.selected_objects) > 1
        return context.active_object is not None and validNumberOfObjects

    def execute(self, context):
        """
        Distribute selected objects along the specified axis with a gap.
        The active object remains in place, and the gap can be inverted on subsequent clicks.
        """
        print("Distributing with gap")

        # Axis mapping for Blender's coordinate system
        X, Y, Z = 0, 1, 2
        axis = {"x": X, "y": Y, "z": Z}[self.axis]
        reference_axis = {"x": Y, "y": X, "z": X}[self.axis]

        # Reset invert_gap if the axis changes
        if context.scene.last_used_axis != self.axis:
            context.scene.invert_gap = False  # Reset invert_gap to default
            context.scene.last_used_axis = self.axis  # Update the last used axis

        # Get the active object and selected objects
        active_object = bpy.context.active_object
        selected_objects = bpy.context.selected_objects
        active_object_index = selected_objects.index(active_object)

        # Toggle invert_gap for alternating gap directions
        context.scene.invert_gap = not context.scene.invert_gap
        invert_gap = context.scene.invert_gap
        gap_sign = -1 if invert_gap else 1
        gap = context.scene.gap * gap_sign

        # Sort objects by their position along the reference axis
        selected_objects.sort(key=lambda o: o.location[reference_axis])

        # Debugging: Print active object details
        print(
            f"Active object: {active_object.name} - Axis Value: {active_object.location[axis]}"
        )

        # Distribute objects with the specified gap
        index = 0
        for obj in selected_objects:
            # Skip the active object
            if obj == active_object:
                index += 1
                continue

            # Calculate the distance from the active object
            distance_between_active_index = index - active_object_index

            # Debugging: Print object distribution details
            print(
                f"Object: {obj.name} | Index: {index} | Distance: {distance_between_active_index}"
            )

            # Update the object's position along the specified axis
            obj.location[axis] = (
                active_object.location[axis] - distance_between_active_index * gap
            )
            index += 1

        return {"FINISHED"}


# Interface Panel


class VIEW3D_PT_AlignAndDistributePanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Align and Distribute Tools"
    bl_context = "objectmode"
    bl_category = "Item"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):

        layout = self.layout

        # align operators
        col = layout.column()
        col.label(text="Align to active object")
        col = layout.column_flow(columns=3, align=True)

        alignX = col.operator("object.align_location", text="X")
        alignX.axis = "x"

        alignY = col.operator("object.align_location", text="Y")
        alignY.axis = "y"

        alignZ = col.operator("object.align_location", text="Z")
        alignZ.axis = "z"

        # distribute evenly operators
        col = layout.column()
        col.label(text="Evenly distribute")
        col = layout.column_flow(columns=3, align=True)

        distributeX = col.operator("object.distribute_evenly", text="X")
        distributeX.axis = "x"

        distributeY = col.operator("object.distribute_evenly", text="Y")
        distributeY.axis = "y"

        distributeZ = col.operator("object.distribute_evenly", text="Z")
        distributeZ.axis = "z"

        # distribute with gap operators
        col = layout.column()
        col.label(text="Distribute with gap (experimental)")

        for prop_name, _ in PROPS:
            col.prop(context.scene, prop_name)

        col = layout.column_flow(columns=3, align=True)

        distributeGapX = col.operator("object.distribute_with_gap", text="X")
        distributeGapX.axis = "x"

        distributeGapY = col.operator("object.distribute_with_gap", text="Y")
        distributeGapY.axis = "y"

        distributeGapZ = col.operator("object.distribute_with_gap", text="Z")
        distributeGapZ.axis = "z"


# Class List
classes = [
    VIEW3D_PT_AlignAndDistributePanel,
    OBJECT_OP_AlignLocationOperator,
    OBJECT_OP_DistributeWithGapOperator,
    OBJECT_OP_DistributeEvenlyOperator,
]

# Register all operators and panels


def update_ui(self, context):
    for area in context.screen.areas:
        if area.type == "VIEW_3D":  # Ensure we only update the 3D View UI
            area.tag_redraw()


def register():

    bpy.types.Scene.invert_gap = BoolProperty(
        name="Invert Gap",
        default=False,
        description="Invert the gap distribution on second click",
        update=update_ui,
    )

    bpy.types.Scene.last_used_axis = bpy.props.StringProperty(
        name="Last Used Axis",
        default="",
        description="Tracks the last axis used for distributing with gap",
    )

    for prop_name, prop_value in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    del bpy.types.Scene.invert_gap
    for prop_name, _ in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
