import json
import os
import yaml


def _project_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _resolve(path):
    if not os.path.isabs(path):
        path = os.path.join(_project_root(), path)
    return path


def load_yaml(path):
    target = _resolve(path)
    try:
        with open(target, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件未找到: {target}")
    except yaml.YAMLError as e:
        raise ValueError(f"YAML 解析失败: {target}\n{e}")


def load_json(path, default=None):
    target = _resolve(path)
    if not os.path.exists(target):
        return default if default is not None else {}
    try:
        with open(target, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"JSON 解析失败: {target}\n{e}")


def save_json(path, data):
    target = _resolve(path)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
