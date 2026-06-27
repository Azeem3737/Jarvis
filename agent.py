from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    noise_cancellation,
)
from Jarvis_prompts import behavior_prompts, Reply_prompts
from Jarvis_google_search import google_search, get_current_datetime
from jarvis_get_whether import get_weather
from Jarvis_window_CTRL import open, close, folder_file
from Jarvis_file_opner import Play_file
from keyboard_mouse_CTRL import move_cursor_tool, mouse_click_tool, scroll_cursor_tool, type_text_tool, press_key_tool, swipe_gesture_tool, press_hotkey_tool, control_volume_tool
load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=behavior_prompts,
                         tools=[
                            google_search,
                            get_current_datetime,
                            get_weather,
                            open, #ایپس کو کھولنے کے لیے ہیں۔
                            close, 
                            folder_file, #ye فولڈر کھولنے کے لئے ہے
                            Play_file,  #ye فائل کو رن کرنے کے لیے MP4، MP3، PDF، PPT، img، png وغیرہ کی طرح ہے۔
                            move_cursor_tool, #ye کرسر منتقل کرنے کے لئے ہے
                            mouse_click_tool, #ye ماؤس کلک کرنے کے لئے ہے
                            scroll_cursor_tool, #ye کرسر اسکرول کرنے کے لیے ہے۔
                            type_text_tool, #یہ text ٹائپ کرنے کے لیے ہے
                            press_key_tool, #یہ key press کرنے کے لیے ہے
                            press_hotkey_tool, #یہ hotkey press کرنے کے لیے ہے
                            control_volume_tool, #یہ volume control کرنے کے لیے ہے
                            swipe_gesture_tool #یہ gesture swipe کرنے کے لیے ہے 
                         ]
                         )


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            voice="Charon"
        )
    )
    
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
            video_enabled=True 
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions=Reply_prompts
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

