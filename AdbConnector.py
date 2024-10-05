import subprocess

# Must call refresh_adb_device_list to update the dictionary before using
serial_and_model_dict: dict[str, str] = {}


def refresh_adb_device_list():
    serial_and_model_dict.clear()
    adb_command = "./platform-tools/adb devices -l"
    adb_device_result_list = subprocess.run(adb_command, capture_output=True, text=True).stdout.splitlines()
    adb_device_result_list.pop(0)
    adb_device_result_list.pop()
    for adb_device_info in adb_device_result_list:
        lst = adb_device_info.split(" ")
        model_name = next((ele for ele in lst if "model:" in ele), None)
        serial_and_model_dict[model_name] = lst[0]
