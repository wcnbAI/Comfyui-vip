import json
import re
import io
import base64
import traceback
import random
import torch
import requests
from urllib.parse import urlparse
from server import PromptServer
from .shaobkj_shared import (
    get_config_value,
    post_json_with_retry,
    create_requests_session,
    disable_insecure_request_warnings,
    build_submit_timeout,
    resize_and_encode_image,
    resize_pil_long_side,
    tensor_to_pil
)

class Shaobkj_VIP_LLM_App:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        api_key_default = get_config_value("API_KEY", "SHAOBKJ_API_KEY", "")
        return {
            "required": {
                "API密钥": ("STRING", {"default": api_key_default, "multiline": False, "tooltip": "服务端 API Key；推荐：填写有效 Key"}),
                "API地址": ("STRING", {"default": "https://yhmx.work", "multiline": False, "tooltip": "API 基础地址；推荐：https://yhmx.work"}),
                "模型选择": (["gemini-2.5-flash", "gemini-3.1-pro-preview", "gemini-3-flash-preview"], {"default": "gemini-2.5-flash", "tooltip": "模型选择；推荐：gemini-2.5-flash"}),
                "使用系统代理": ("BOOLEAN", {"default": True, "tooltip": "是否使用系统代理；推荐：开启"}),
                "系统指令": ("STRING", {"default": "你是高效的AI提示词生成大师。请根据用户输入生成可直接执行的方案或内容，结构清晰，直接输出提示词，不要有任何废话。", "multiline": True, "tooltip": "系统级指令；推荐：默认内容"}),
                "用户输入": ("STRING", {"default": "", "multiline": True, "tooltip": "用户输入内容；推荐：清晰具体"}),
                "思考模式": ("BOOLEAN", {"default": False, "label_on": "开启", "label_off": "关闭", "tooltip": "是否启用思考模式；推荐：关闭"}),
                "思考预算": ("INT", {"default": 10240, "min": 1024, "max": 65536, "step": 1024, "tooltip": "思考预算上限；推荐：10240"}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1, "tooltip": "采样温度；推荐：0.7"}),
                "topP": ("FLOAT", {"default": 0.95, "min": 0.0, "max": 1.0, "step": 0.01, "tooltip": "核采样概率；推荐：0.95"}),
                "输入图像-长边设置": (["1024", "1280", "1536"], {"default": "1280", "tooltip": "输入图像长边缩放；推荐：1280"}),
                "等待时间": ("INT", {"default": 180, "min": 0, "max": 1000000, "tooltip": "请求超时时间(秒)；推荐：180"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2147483647, "tooltip": "随机种子；推荐：0"}),
                "API申请地址": ("STRING", {"default": "https://yhmx.work/login?expired=true", "multiline": False, "tooltip": "API 申请入口；推荐：默认地址"}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("文本内容", "API响应")
    FUNCTION = "run_llm"
    CATEGORY = "🤖Shaobkj-vip"

    def run_llm(self, API密钥, API地址, 模型选择, 使用系统代理, 系统指令, 用户输入, 思考模式, 思考预算, temperature, topP, 输入图像_长边设置=1280, 等待时间=180, seed=0, **kwargs):
        # Implementation of LLM Logic
        return self._execute_llm(API密钥, API地址, 模型选择, 使用系统代理, 系统指令, 用户输入, 思考模式, 思考预算, temperature, topP, 输入图像_长边设置, 等待时间, seed, **kwargs)

    def _execute_llm(self, API密钥, API地址, 模型选择, 使用系统代理, 系统指令, 用户输入, 思考模式, 思考预算, temperature, topP, 输入图像_长边设置, 等待时间, seed, **kwargs):
        api_key = API密钥
        if not api_key:
            raise ValueError("API Key is required.")

        base_origin = str(API地址).rstrip("/")
        if base_origin.endswith("/v1"):
            base_origin = base_origin[:-3]
            
        model = 模型选择
        long_side_val = int(kwargs.get("输入图像-长边设置", 输入图像_长边设置))
        image_inputs = []
        for k, v in kwargs.items():
            if k.startswith("image_") and v is not None:
                image_inputs.append((k, v))
        image_inputs.sort(key=lambda x: int(x[0].split("_")[1]))

        def append_images(parts):
            for _, tensor in image_inputs:
                try:
                    if isinstance(tensor, torch.Tensor) and tensor.dim() == 4:
                        for i in range(tensor.shape[0]):
                            pil_img = tensor_to_pil(tensor[i])
                            b64_str, _ = resize_and_encode_image(pil_img, long_side_val)
                            if b64_str:
                                parts.append({"inline_data": {"mime_type": "image/jpeg", "data": b64_str}})
                    else:
                        pil_img = tensor_to_pil(tensor)
                        b64_str, _ = resize_and_encode_image(pil_img, long_side_val)
                        if b64_str:
                            parts.append({"inline_data": {"mime_type": "image/jpeg", "data": b64_str}})
                except Exception:
                    pass

        # ... (Rest of the LLM logic is reused, we can extract this common logic if needed, but for now I will duplicate the core request logic to support both nodes) ...
        # For brevity and safety, I will keep the original implementation here and just call it.
        # However, since I cannot easily call the method from another class without inheritance or a helper, 
        # I will refactor the core request logic into a standalone function or keep it inside.
        
        # To avoid massive code duplication, let's just use the logic I read previously.
        # Since I'm rewriting the file, I'll include the full logic.
        
        url = f"{base_origin}/v1beta/models/{model}:generateContent"
        # ... (Logic for Gemini 2.5 Flash and others) ...
        
        # Actually, let's implement the full logic cleanly.
        
        disable_insecure_request_warnings()
        session, proxies = create_requests_session(bool(使用系统代理))
        submit_timeout = build_submit_timeout(int(等待时间))

        # Construct Prompt
        system_prompt = 系统指令.strip() if isinstance(系统指令, str) else ""
        user_prompt = 用户输入.strip()
        
        # Special handling for Gemini 2.5 Flash (often doesn't support systemInstruction field well in some proxy/versions, so prepending is safer)
        # But for 3-pro-preview, systemInstruction is supported.
        # Let's use the standard payload structure.
        
        parts = [{"text": user_prompt}]
        append_images(parts)
        
        payload = {
            "contents": [{"role": "user", "parts": parts}],
            "generationConfig": {
                "temperature": temperature,
                "topP": topP,
                "seed": int(seed) if int(seed) >= 0 else 0
            }
        }
        
        if system_prompt:
             payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

        if 思考模式:
             payload["generationConfig"]["thinkingConfig"] = {
                "includeThoughts": True,
                "thinkingBudget": 思考预算
            }

        headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
        
        try:
            response = post_json_with_retry(
                session,
                url,
                headers=headers,
                payload=payload,
                timeout=submit_timeout,
                proxies=proxies,
                verify=False,
            )
            
            if response.status_code != 200:
                return (f"API Error {response.status_code}: {response.text}", str(response.text))

            res_json = response.json()
            
            generated_text = ""
            if "candidates" in res_json and len(res_json["candidates"]) > 0:
                candidate = res_json["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "text" in part:
                            generated_text += part["text"]
            
            if not generated_text:
                generated_text = "No text response generated."
                
            return (generated_text, json.dumps(res_json, ensure_ascii=False))

        except Exception as e:
            return (f"Error: {str(e)}", str(traceback.format_exc()))


NODE_CLASS_MAPPINGS = {
    "Shaobkj_VIP_LLM_App": Shaobkj_VIP_LLM_App,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Shaobkj_VIP_LLM_App": "🤖LLM应用",
}
