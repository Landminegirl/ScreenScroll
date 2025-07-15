bl_info = {
    "name": "SreenScroll",
    "author": "LandmineGirl",
    "version": (4, 4),
    "blender": (3, 0, 0),
    "location": "Object Data Properties > ScreenScroll",
    "description": "Advanced text animation with loop, delete, reverse, random speed, and sentence cycling.",
    "category": "Animation",
}

import bpy
import random
import time

_cursor_presets = {
    "BAR": "|",
    "BLOCK": "█",
    "UNDERSCORE": "_",
    "PIPE_LEFT": "▌",
    "ANGLE": ">",
    "ANGLER": "<",
    "NONE": "",
}

_typewriter_cache = {}

def get_cursor(props):
    if props.cursor_style == "CUSTOM":
        return props.custom_cursor
    return _cursor_presets.get(props.cursor_style, "")

def update_typewriter(scene):
    frame = scene.frame_current
    fps = scene.render.fps

    for obj in scene.objects:
        if obj.type != 'FONT' or not hasattr(obj, 'typewriter_props'):
            continue

        props = obj.typewriter_props
        if not props.enabled or not props.text_source:
            continue

        full_text = props.text_source.as_string()
        obj_id = obj.name
        start_frame = props.start_frame
        speed = max(1, props.letters_per_second)
        reverse = props.reverse_mode
        delete_mode = props.delete_mode
        loop_mode = props.loop_mode
        sentence_mode = props.sentence_cycle
        delay_between = props.loop_delay
        randomize = props.random_delay
        randomness = props.random_delay_factor
        max_lines = props.max_lines if props.scroll_mode else 0
        cursor = get_cursor(props)
        blink = props.blinking_cursor and (time.time() % (props.cursor_blink_speed * 2)) < props.cursor_blink_speed

        elapsed_time = (frame - start_frame) / fps

        if loop_mode:
            if obj_id not in _typewriter_cache or frame == start_frame:
                _typewriter_cache[obj_id] = {
                    "sentences": [s.strip() for s in full_text.split(",")] if sentence_mode else [full_text],
                }

            sentence_list = _typewriter_cache[obj_id]["sentences"]
            total_chars = sum(len(s) * 2 for s in sentence_list) + delay_between * fps * 2 * len(sentence_list)
            loop_frame = int((frame - start_frame) % total_chars)
            total_elapsed = 0

            for sentence in sentence_list:
                write_len = len(sentence)
                write_time = write_len / speed
                pause_time = delay_between
                delete_time = write_len / speed
                cycle_time = write_time + pause_time + delete_time + pause_time

                if loop_frame < total_elapsed + cycle_time:
                    local_time = loop_frame - total_elapsed
                    if local_time < write_time:
                        char_index = int(local_time * speed)
                        visible = sentence[:char_index]
                    elif local_time < write_time + pause_time:
                        visible = sentence
                    elif local_time < write_time + pause_time + delete_time:
                        del_index = int((local_time - write_time - pause_time) * speed)
                        visible = sentence[:max(0, len(sentence) - del_index)]
                    else:
                        visible = ""
                    break
                total_elapsed += cycle_time
            else:
                visible = sentence_list[-1]
        else:
            if obj_id not in _typewriter_cache or frame == start_frame:
                _typewriter_cache[obj_id] = {"full": full_text}

            if randomize:
                key = (obj_id, full_text, speed, randomness)
                if "_random_delays" not in _typewriter_cache[obj_id]:
                    rng = random.Random(obj_id + full_text)
                    base_time = 1.0 / speed
                    delays = [
                        base_time + rng.uniform(-base_time, base_time) * randomness
                        for _ in full_text
                    ]
                    cumulative = []
                    total = 0.0
                    for d in delays:
                        total += max(0.01, d)
                        cumulative.append(total)
                    _typewriter_cache[obj_id]["_random_delays"] = cumulative

                cumulative = _typewriter_cache[obj_id]["_random_delays"]
                char_index = sum(1 for t in cumulative if t <= elapsed_time)
            else:
                char_index = int(elapsed_time * speed)

            if delete_mode:
                visible = full_text[:max(0, len(full_text) - char_index)]
            elif reverse:
                visible = full_text[max(0, len(full_text) - char_index):]
            else:
                visible = full_text[:char_index]

        if max_lines > 0:
            lines = visible.splitlines()
            visible = "\n".join(lines[-max_lines:])

        obj.data.body = visible
        if blink and cursor:
            obj.data.body += cursor

# === UI ===
class TYPEWRITER_PT_panel(bpy.types.Panel):
    bl_label = "ScreenScroll Effect"
    bl_idname = "OBJECT_PT_screenscroll_effect"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'FONT'

    def draw(self, context):
        props = context.object.typewriter_props
        layout = self.layout

        layout.prop(props, "enabled")
        layout.prop(props, "text_source")
        layout.prop(props, "start_frame")
        layout.prop(props, "letters_per_second")

        layout.prop(props, "delete_mode")
        layout.prop(props, "reverse_mode")

        layout.prop(props, "loop_mode")
        if props.loop_mode:
            layout.prop(props, "loop_delay")
        layout.prop(props, "sentence_cycle")

        layout.prop(props, "scroll_mode")
        if props.scroll_mode:
            layout.prop(props, "max_lines")

        layout.prop(props, "blinking_cursor")
        if props.blinking_cursor:
            layout.prop(props, "cursor_style")
            if props.cursor_style == "CUSTOM":
                layout.prop(props, "custom_cursor")
            layout.prop(props, "cursor_blink_speed")

        layout.prop(props, "random_delay")
        if props.random_delay:
            layout.prop(props, "random_delay_factor")

# === Properties ===
class TYPEWRITER_Props(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(default=False)
    text_source: bpy.props.PointerProperty(type=bpy.types.Text)
    start_frame: bpy.props.IntProperty(default=1, min=0)
    letters_per_second: bpy.props.IntProperty(default=15, min=1)

    delete_mode: bpy.props.BoolProperty(default=False)
    reverse_mode: bpy.props.BoolProperty(default=False)

    loop_mode: bpy.props.BoolProperty(default=False)
    loop_delay: bpy.props.FloatProperty(default=0.5, min=0.0)
    sentence_cycle: bpy.props.BoolProperty(default=False)

    scroll_mode: bpy.props.BoolProperty(default=False)
    max_lines: bpy.props.IntProperty(default=5, min=1)

    blinking_cursor: bpy.props.BoolProperty(default=True)
    cursor_style: bpy.props.EnumProperty(
        name="Cursor Style",
        items=[
            ("BAR", "Bar |", ""),
            ("BLOCK", "Block █", ""),
            ("UNDERSCORE", "Underscore _", ""),
            ("PIPE_LEFT", "Left ▌", ""),
            ("ANGLE", "Angle >", ""),
            ("ANGLER", "Angle <", ""),
            ("NONE", "None", ""),
            ("CUSTOM", "Custom", ""),
        ],
        default="BAR",
    )
    custom_cursor: bpy.props.StringProperty(default="|")
    cursor_blink_speed: bpy.props.FloatProperty(default=0.5, min=0.05)

    random_delay: bpy.props.BoolProperty(default=False)
    random_delay_factor: bpy.props.FloatProperty(
        name="Random Delay Amount",
        description="Controls how much character delay varies randomly",
        default=0.3, min=0.0, max=2.0,
    )

# === Registration ===
classes = (
    TYPEWRITER_PT_panel,
    TYPEWRITER_Props,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.typewriter_props = bpy.props.PointerProperty(type=TYPEWRITER_Props)

    if update_typewriter not in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.append(update_typewriter)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    if update_typewriter in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(update_typewriter)
    del bpy.types.Object.typewriter_props

if __name__ == "__main__":
    register()
