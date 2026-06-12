import os


def _optional_bool(name):
    value = os.getenv(name)
    if value is None or value == "":
        return None
    lowered = value.lower()
    if lowered in {"1", "true", "yes", "on"}:
        return True
    if lowered in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be true or false, got {value!r}")


def _optional_number(name, cast):
    value = os.getenv(name)
    return None if value is None or value == "" else cast(value)


def _model_names():
    value = os.getenv("LLM_MODEL_NAMES") or os.getenv("LLM_MODEL_NAME", "")
    return [name.strip() for name in value.split(",") if name.strip()]


model_names = _model_names()
if not model_names:
    raise RuntimeError("LLM_MODEL_NAME must be set by the calling script")


def get_url(model_name):
    del model_name
    base_url = os.getenv("LLM_BASE_URL")
    api_key = os.getenv("LLM_API_KEY")
    if not base_url:
        raise RuntimeError("LLM_BASE_URL must be set by the calling script")
    if not api_key:
        raise RuntimeError("LLM_API_KEY must be set by the calling script")
    return base_url, api_key


def get_parameter(model_name):
    del model_name
    return {
        "temperature": _optional_number("LLM_TEMPERATURE", float),
        "top_p": _optional_number("LLM_TOP_P", float),
        "max_tokens": _optional_number("LLM_MAX_TOKENS", int),
        "enable_thinking": _optional_bool("LLM_ENABLE_THINKING"),
        "stream": False,
    }


def get_semaphore_num(model_name):
    del model_name
    return int(os.getenv("LLM_CONCURRENCY", "32"))
