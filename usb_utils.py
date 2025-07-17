import subprocess

def run_powershell_hidden(script):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-Command", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        startupinfo=startupinfo
    )
    return result

def select_usb():
    ps_script = r"""
    Get-WmiObject Win32_LogicalDisk | Where-Object { $_.DriveType -eq 2 } | Select-Object -ExpandProperty VolumeName
    """
    result = run_powershell_hidden(ps_script)
    if result.returncode != 0:
        raise RuntimeError("Failed to retrieve USB volume names: " + result.stderr)
    volume_names = [name.strip() for name in result.stdout.strip().splitlines() if name.strip()]
    if not volume_names:
        return None
    return volume_names[0] if len(volume_names) == 1 else volume_names

def get_usb_drive_by_label(label):
    ps_script = f"""
    Get-WmiObject Win32_LogicalDisk |
        Where-Object {{ $_.DriveType -eq 2 -and $_.VolumeName -eq '{label}' }} |
        Select-Object -ExpandProperty DeviceID
    """
    result = run_powershell_hidden(ps_script)
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else None

def format_usb(label):
    usb_drive = get_usb_drive_by_label(label)
    if not usb_drive:
        raise RuntimeError(f"USB drive with label '{label}' not found.")
    ps_script = f"""
    $driveLetter = "{usb_drive.replace(':', '')}"
    # Format only the existing partition without deleting or repartitioning
    $partition = Get-Partition -DriveLetter $driveLetter
    if ($partition -eq $null) {{
        throw "Partition with drive letter $driveLetter not found."
    }}
    Format-Volume -Partition $partition -FileSystem FAT32 -NewFileSystemLabel '{label}' -Confirm:$false -Force
    """
    result = run_powershell_hidden(ps_script)
    if result.returncode != 0:
        raise RuntimeError("USB format failed: " + result.stderr)
    else:
        print(f"USB '{label}' has been formatted.")

