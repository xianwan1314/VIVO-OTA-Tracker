import os
import sys
import re
import json
import base64
import shutil
import tempfile


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


def find_java():
    embedded_jre = resource_path("jre/bin/java.exe")
    if os.path.exists(embedded_jre):
        return embedded_jre
    for path in os.environ.get("PATH", "").split(os.pathsep):
        java_exe = os.path.join(path, "java.exe")
        if os.path.exists(java_exe):
            return java_exe
    return None


def build_java_command(config, work_dir):
    java_path = find_java()
    if not java_path:
        return None, None

    jar_path = resource_path("unidbg-android-0.9.10-SNAPSHOT.jar")

    device_type = 'tablet' if config.get('MODEL_SW_VER', '').startswith('DPD') else 'phone'

    cmd = [
        java_path,
        "-Djava.net.preferIPv4Stack=true",
        f"-DDEVICE_TYPE={device_type}",
        f"-DMODEL_SW_VER={config['MODEL_SW_VER']}",
        f"-DDEVICE_MODEL={config['DEVICE_MODEL']}",
        f"-DSW_VERSION={config['SW_VERSION']}",
        f"-DANDROID_VER={config['ANDROID_VER']}",
        f"-DSNP={config.get('SNP', 'A0000000000000A')}",
        f"-DIS_FULL={config.get('IS_FULL', 'true')}",
        "-Dhttps.protocols=TLSv1.2",
        "-Djava.library.path=" + work_dir,
        "-jar", jar_path,
    ]
    return cmd, device_type


def prepare_work_dir():
    work_dir = tempfile.mkdtemp(prefix="vivo_ota_")
    src_libs = resource_path("libs")
    dst_libs = os.path.join(work_dir, "libs")
    if os.path.exists(src_libs):
        shutil.copytree(src_libs, dst_libs)

    src_dll = resource_path("natives/windows_64/unicorn.dll")
    dst_dll = os.path.join(work_dir, "unicorn.dll")
    if os.path.exists(src_dll):
        shutil.copy(src_dll, dst_dll)

    return work_dir


def cleanup_work_dir(work_dir):
    if work_dir and os.path.exists(work_dir):
        try:
            shutil.rmtree(work_dir, ignore_errors=True)
        except Exception:
            pass


def _extract_json_result(raw_text):
    match = re.search(
        r'===VIVO_OTA_RESULT_START===\s*(.*?)\s*===VIVO_OTA_RESULT_END===',
        raw_text, re.DOTALL
    )
    if not match:
        return None
    try:
        return json.loads(match.group(1).strip())
    except (json.JSONDecodeError, ValueError):
        return None


def _extract_raw_update_payload(raw_text):
    match = re.search(
        r'=== Raw Update Payload Base64 ===\s*([A-Za-z0-9+/=\r\n]+?)\s*=== End Raw Update Payload Base64 ===',
        raw_text, re.DOTALL
    )
    if not match:
        return ""
    encoded = re.sub(r'\s+', '', match.group(1))
    try:
        return base64.b64decode(encoded).decode('utf-8', errors='replace')
    except Exception:
        return ""


def _parse_legacy_results(raw_text):
    result = {}

    device_match = re.search(r'Device:\s*(\w+)\s*\|\s*(\S+)\s*/\s*(\S+)', raw_text)
    if device_match:
        result['device_type'] = device_match.group(1)
        result['device_model'] = device_match.group(2)
        result['codename'] = device_match.group(3)

    base_match = re.search(r'Base Version:\s*(\S+)', raw_text)
    if base_match:
        result['base_version'] = base_match.group(1)

    ver_match = re.search(r'=== Update Information ===.*?Version:\s*(\S+)', raw_text, re.DOTALL)
    if not ver_match:
        ver_match = re.search(r'Version:\s*(\S+)', raw_text)
    if ver_match:
        result['update_version'] = ver_match.group(1)

    size_match = re.search(r'Size:\s*\d+\s*bytes\s*\(([\d.]+)\s*MB\)', raw_text)
    if size_match:
        result['file_size'] = size_match.group(1)

    url_match = re.search(r'Download URL:\s*(https?://\S+)', raw_text)
    if url_match:
        result['download_url'] = url_match.group(1).strip()

    return result


def parse_ota_result(raw_text):
    json_result = _extract_json_result(raw_text)
    if json_result:
        return json_result, json_result.get('raw_response', '')

    legacy = _parse_legacy_results(raw_text)
    payload = _extract_raw_update_payload(raw_text)
    return legacy, payload
