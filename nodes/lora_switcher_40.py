from nodes import LoraLoader
import folder_paths

class LoRASwitcherNode40:
    TITLE = "LoRA Switcher 40"
    CATEGORY = "oshtz Nodes"
    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "apply_lora"

    @classmethod
    def INPUT_TYPES(cls):
        lora_list = ["None"] + folder_paths.get_filename_list("loras")
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": -10.0,
                    "max": 10.0,
                    "step": 0.01
                }),
                "selected": (["None"] + [f"LoRA {i}" for i in range(1, 41)],),
                **{f"lora_{i}": (lora_list,) for i in range(1, 41)}
            }
        }

    def apply_lora(self, model, clip, lora_strength, selected, **loras):
        if selected == "None" or lora_strength == 0:
            return (model, clip)

        # Determine which LoRA to use based on the selection
        lora_name = None
        for i in range(1, 41):
            if selected == f"LoRA {i}":
                lora_name = loras[f"lora_{i}"]
                break

        # Check if the selected LoRA is valid
        if lora_name == "None" or not lora_name:
            return (model, clip)

        # Apply the selected LoRA
        model, clip = LoraLoader().load_lora(
            model, clip, lora_name, lora_strength, lora_strength
        )

        return (model, clip)