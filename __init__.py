from .node_api_generator import NODE_CLASS_MAPPINGS as api_class_mappings, NODE_DISPLAY_NAME_MAPPINGS as api_display_name_mappings
from .node_llm_app import NODE_CLASS_MAPPINGS as llm_class_mappings, NODE_DISPLAY_NAME_MAPPINGS as llm_display_name_mappings

NODE_CLASS_MAPPINGS = {**api_class_mappings, **llm_class_mappings}
NODE_DISPLAY_NAME_MAPPINGS = {**api_display_name_mappings, **llm_display_name_mappings}

WEB_DIRECTORY = "js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

print("[Comfyui-Shaobkj-vip] 🤖图像生成 & 🤖LLM应用 nodes loaded.")
