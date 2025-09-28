import importlib
import unreal

def ask_and_toast(q: str):
    try:
        import dw_dev
        importlib.reload(dw_dev)
    except Exception as e:
        unreal.log_error(f"Daywalker: dw_dev not available: {e}")
        unreal.EditorDialog.show_message("Daywalker", "dw_dev not available. Is the proxy running on 8092?", unreal.AppMsgType.OK)
        return

    q = (q or "").strip()
    if not q:
        unreal.EditorDialog.show_message("Daywalker", "Question is empty.", unreal.AppMsgType.OK)
        return

    try:
        ans = dw_dev.ask(q)
    except Exception as e:
        unreal.log_error(f"Daywalker error: {e}")
        unreal.EditorDialog.show_message("Daywalker", f"Error: {e}", unreal.AppMsgType.OK)
        return

    unreal.log(f"You: {q}")
    unreal.log(f"Daywalker: {ans}")
    # Keep dialog short; full text is in Output Log
    preview = ans if len(ans) < 280 else (ans[:277] + "...")
    unreal.EditorDialog.show_message("Daywalker", preview, unreal.AppMsgType.OK)
