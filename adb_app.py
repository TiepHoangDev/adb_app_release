import json
import re
import subprocess


class AdbApp:
    @staticmethod
    def set_fake_gps(device_id: str, latitude: float, longitude: float) -> str:
        """Set fake GPS location"""
        cmd = f'adb -s {device_id} shell content call --uri content://com.example.adb_app.provider --method fake_gps --arg "{latitude},{longitude}"'
        return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

    @staticmethod
    def get_gps(device_id: str) -> str:
        """Get current GPS location"""
        cmd = f"adb -s {device_id} shell content call --uri content://com.example.adb_app.provider --method get_location"
        return (
            subprocess.check_output(cmd, shell=True, timeout=5).decode("utf-8").strip()
        )

    @staticmethod
    def stop_fake_gps(device_id: str) -> str:
        """Stop fake GPS"""
        cmd = f"adb -s {device_id} shell content call --uri content://com.example.adb_app.provider --method fake_gps --arg 'stop'"
        return (
            subprocess.check_output(cmd, shell=True, timeout=5).decode("utf-8").strip()
        )

    @staticmethod
    def get_public_ip(device_id: str) -> str:
        """
        Lấy địa chỉ IP public
        """
        # adb shell content call --uri content://com.example.adb_app.provider --method get --arg "https://myip.devappnow.com/api/ip"
        # https://myip.devappnow.com/api/ip -> {"ip":"222.252.107.64"}
        cmd = f'adb -s {device_id} shell content call --uri content://com.example.adb_app.provider --method get --arg "https://myip.devappnow.com/api/ip"'
        result = (
            subprocess.check_output(cmd, shell=True, timeout=5).decode("utf-8").strip()
        )
        match = re.search(r"result=({.*?})", result)
        if match:
            json_str = match.group(1)
            data = json.loads(json_str)
            ip = data.get("ip")
            if ip:
                return ip
        raise Exception(f"Cannot get public ip: {result}")

    @staticmethod
    def try_get_public_ip(device_id: str) -> str | None:
        try:
            return AdbApp.get_public_ip(device_id)
        except Exception:
            return None
