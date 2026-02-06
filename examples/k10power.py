#!/usr/bin/env python3
# Power consumption monitor for ksystemstats
# Sensors: amd_gpu (PPT), rapl_package_0 (CPU Package), rapl_core (CPU Cores)

import subprocess
import time

# RAPL state for power calculation
rapl_state = {
    "package": {"last_energy": 0, "last_time": 0},
    "core": {"last_energy": 0, "last_time": 0},
}

def read_amd_gpu_power() -> str:
    """Read AMD GPU power from sensors command (PPT in mW -> W)"""
    try:
        result = subprocess.run(["sensors"], capture_output=True, text=True, timeout=2)
        for line in result.stdout.splitlines():
            if "PPT:" in line:
                # Parse "PPT:           7.00 mW" -> convert to W
                parts = line.split()
                if len(parts) >= 2:
                    power_mw = float(parts[1])
                    return str(round(power_mw / 1000, 3))
    except Exception:
        pass
    return "0"

def read_rapl_power(domain: str) -> str:
    """Read RAPL power (calculated from energy delta)"""
    paths = {
        "package": "/sys/class/powercap/intel-rapl:0/energy_uj",
        "core": "/sys/class/powercap/intel-rapl:0:0/energy_uj",
    }
    
    try:
        with open(paths[domain]) as f:
            current_energy = int(f.read().strip())
        current_time = time.time()
        
        state = rapl_state[domain]
        last_energy = state["last_energy"]
        last_time = state["last_time"]
        
        state["last_energy"] = current_energy
        state["last_time"] = current_time
        
        if last_time == 0:
            return "0"
        
        time_delta = current_time - last_time
        if time_delta <= 0:
            return "0"
        
        energy_delta = current_energy - last_energy
        if energy_delta < 0:  # Counter overflow
            energy_delta = 0
        
        # microjoules / seconds = microwatts -> watts
        power_w = (energy_delta / time_delta) / 1_000_000
        return str(round(power_w, 2))
    except Exception:
        return "0"

SENSORS = {
    "amd_gpu": {
        "name": "GPU Power",
        "description": "AMD GPU PPT power consumption",
        "read": read_amd_gpu_power,
    },
    "rapl_package_0": {
        "name": "CPU Package",
        "description": "Total CPU package power",
        "read": lambda: read_rapl_power("package"),
    },
    "rapl_core": {
        "name": "CPU Cores",
        "description": "CPU cores power",
        "read": lambda: read_rapl_power("core"),
    },
}

def get_property(sensor_id: str, prop: str) -> str:
    if sensor_id not in SENSORS:
        return ""
    s = SENSORS[sensor_id]
    if prop == "name":
        return s["name"]
    elif prop == "description":
        return s["description"]
    elif prop == "unit":
        return "W"
    elif prop == "min":
        return "0"
    elif prop == "max":
        return "500"
    elif prop == "variant_type":
        return "double"
    elif prop == "initial_value":
        return "0"
    elif prop == "value":
        return s["read"]()
    return ""

def main():
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        
        if line == "?":
            print("\t".join(SENSORS.keys()), flush=True)
        elif "\t" in line:
            sensor_id, prop = line.split("\t", 1)
            print(get_property(sensor_id, prop), flush=True)
        else:
            print("", flush=True)

if __name__ == "__main__":
    main()
