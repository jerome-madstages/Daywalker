import unreal

DEVCHAT_URL = "http://127.0.0.1:8092/devchat"

def add_daywalker_menu_entry():
    menus = unreal.ToolMenus.get()
    main  = menus.find_menu("LevelEditor.MainMenu")
    if not main:
        unreal.log_warning("Main menu not found.")
        return False

    # Entry 1: open Dev Chat in the default browser (reliable in-Editor call)
    open_entry = unreal.ToolMenuEntry(
        name="Daywalker.OpenDevChatBrowser",
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.FIRST),
    )
    open_entry.set_label("Daywalker: Open Dev Chat (browser)")
    open_entry.set_tool_tip("Open the local Dev Chat page")
    open_entry.set_string_command(
        unreal.ToolMenuStringCommandType.PYTHON,
        "",
        "import unreal; unreal.SystemLibrary.launch_url('{}')".format(DEVCHAT_URL),
    )

    # Entry 2: ask Daywalker using clipboard text, print reply to Output Log
    ask_entry = unreal.ToolMenuEntry(
        name="Daywalker.AskFromClipboard",
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.FIRST),
    )
    ask_entry.set_label("Daywalker: Ask (from clipboard)")
    ask_entry.set_tool_tip("Send clipboard text to Dev Chat and print the reply")
    ask_entry.set_string_command(
        unreal.ToolMenuStringCommandType.PYTHON,
        "",
        "import unreal, importlib, dw_dev; importlib.reload(dw_dev); "
        "q = unreal.SystemLibrary.get_clipboard_text(); "
        "ans = dw_dev.ask(q) if q else '(clipboard empty)'; "
        "unreal.log('You: ' + (q or '(empty)')); unreal.log('Daywalker: ' + ans)"
    )

    # Install under common sections to be engine-version agnostic
    added_any = False
    for section in ("Window", "Help", "File", "Default"):
        try:
            main.add_menu_entry(section, open_entry)
            main.add_menu_entry(section, ask_entry)
            added_any = True
            break
        except Exception:
            pass

    if not added_any:
        unreal.log_warning("Failed to add Daywalker menu entries.")
        return False

    menus.refresh_all_widgets()
    unreal.log("Added: Daywalker menu entries (Open Dev Chat, Ask from clipboard)")
    return True
