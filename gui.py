import FreeSimpleGUI as sg
from usb_utils import *
from file_ops import *
import os

# color theme
colors = {
    "background": "#f0f0f0",      # light grey
    "text": "#000000",            # black
    "button_bg": "#0078D7",       # Windows blue
    "button_fg": "#ffffff",       # white
    "console_bg": "#1e1e1e",      # dark grey
    "console_fg": "#ffffff",      # white
    "combo_bg": "#ffffff",
    "combo_text": "#000000"
}

sg.theme("LightGrey1")

# helpers
def is_drive_connected(label):
    drive = get_usb_drive_by_label(label)
    return drive and os.path.exists(drive + "\\")

# console message formatter
def ColorMsg(window, element_name, message_type, message):
    txt = window[element_name].Widget
    color_map = {
        "info": "white",
        "success": "limegreen",
        "warning": "yellow",
        "error": "red"
    }
    txt.tag_config(message_type, font=('Consolas', 9), background="", foreground=color_map.get(message_type, "white"))
    txt.insert("end", message + "\n", message_type)
    window[element_name].Update("", append=True)

# USB error popup
def custom_error_popup(message):
    layout = [
        [sg.Text(message)],
        [sg.Button("Refresh USBs", key="REFRESH"), sg.Button("Exit")]
    ]
    window = sg.Window("", layout, modal=True)
    event, _ = window.read()
    window.close()
    return event

# main GUI launcher
def launch_gui():
    try:
        usb_volumes = select_usb()
    except EnvironmentError as e:
        sg.popup_error("Critical Error", str(e))
        return

    while not usb_volumes:
        event = custom_error_popup("No USB drives detected.")
        if event == "REFRESH":
            usb_volumes = select_usb()
        else:
            return

    if isinstance(usb_volumes, str):
        usb_volumes = [usb_volumes]

    selected_volume = usb_volumes[0]

    layout = [
        [
            sg.Text('Select USB:', font=('Comic Sans', 11, 'bold', 'italic'), text_color=colors["text"]),
            sg.Combo(
                usb_volumes, default_value=selected_volume, key="-USB-", readonly=True,
                font=('Lucida Console', 11),
                background_color=colors["combo_bg"], text_color=colors["combo_text"]
            )
        ],
        [
            sg.Button('Format', button_color=(colors["button_fg"], colors["button_bg"])),
            sg.Button('Insert blank downloadpq.mb211 file', button_color=(colors["button_fg"], colors["button_bg"]))
        ],
        [
            sg.Button('Invert Colors', button_color=(colors["button_fg"], colors["button_bg"])),
            sg.Button('Mirror Image', button_color=(colors["button_fg"], colors["button_bg"])),
            sg.Button('Save', button_color=(colors["button_fg"], colors["button_bg"]))
        ],
        [sg.Text('Console', font=('Comic Sans', 11, 'bold', 'italic'), text_color=colors["text"])],
        [
            sg.Multiline("", key="protocol", autoscroll=True, size=(200, 5),
                         background_color=colors["console_bg"], text_color=colors["console_fg"])
        ],
        [sg.Exit(button_color=(colors["button_fg"], colors["button_bg"]))]
    ]

    window = sg.Window('17MB211 Flasher', layout, size=(380, 260), resizable=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        selected_volume = values["-USB-"]
        if not selected_volume:
            ColorMsg(window, "protocol", "warning", "No USB volume selected.")
            continue

        # check if USB is still connected
        if not is_drive_connected(selected_volume):
            ColorMsg(window, "protocol", "error", f"USB '{selected_volume}' is no longer connected.")
            usb_volumes = select_usb()
            if usb_volumes:
                if isinstance(usb_volumes, str):
                    usb_volumes = [usb_volumes]
                window["-USB-"].update(values=usb_volumes, value=usb_volumes[0])
                selected_volume = usb_volumes[0]
                continue
            else:
                ColorMsg(window, "protocol", "warning", "No USBs detected after refresh.")
                continue

        selected_drive = get_usb_drive_by_label(selected_volume)
        file_path = os.path.join(selected_drive, "ptf.ptf")
        
        if event == "Format":
            try:
                format_usb(label=selected_volume)
                ColorMsg(window, "protocol", "info", f"USB '{selected_volume}' has been formatted.")
            except Exception as e:
                ColorMsg(window, "protocol", "error", str(e))

        elif event == "Insert blank downloadpq.mb211 file":
            try:
                insert_blank(label=selected_volume)
                ColorMsg(window, "protocol", "info", "Blank file created on USB.")
            except Exception as e:
                ColorMsg(window, "protocol", "error", str(e))

        elif event == "Invert Colors":
            if not os.path.exists(file_path):
                ColorMsg(window, "protocol", "error", "ptf.ptf not found on USB.")
                continue
            try:
                toggle_enLvdsFormat(file_path)
                ColorMsg(window, "protocol", "info", "Image colors have been inverted.")
            except Exception as e:
                ColorMsg(window, "protocol", "error", str(e))

        elif event == "Mirror Image":
            if not os.path.exists(file_path):
                ColorMsg(window, "protocol", "error", "ptf.ptf not found on USB.")
                continue
            try:
                toggle_b8Flip_lines(file_path)
                ColorMsg(window, "protocol", "info", "Image has been mirrored.")
            except Exception as e:
                ColorMsg(window, "protocol", "error", str(e))

        elif event == "Save":
            try:
                save_pq(label=selected_volume)
                ColorMsg(window, "protocol", "info", "USB has been saved.")
            except Exception as e:
                ColorMsg(window, "protocol", "error", str(e))

    window.close()
