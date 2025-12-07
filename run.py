# from google.adk import AgentRunner
# from pipeline.sre_pipeline import sre_pipeline

# if __name__ == "__main__":
#     runner = AgentRunner(agent=sre_pipeline)
#     runner.run()






import sys, os
import asyncio
from dotenv import load_dotenv
load_dotenv()
from pprint import pprint

import sys, os

# Force Python to load from this project folder FIRST
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)



from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import UserContent, Part
from pipeline.sre_pipeline import sre_pipeline
print("Loaded pipeline from:", sre_pipeline)


if __name__ == "__main__":
    session_service = InMemorySessionService()

    # Explicitly create the session before running (await the coroutine)
    asyncio.run(session_service.create_session(user_id="u1", session_id="sess1", app_name="agents"))

    runner = Runner(
        agent=sre_pipeline,
        app_name="agents",
        session_service=session_service
    )

    print("[DEBUG] Starting pipeline run...")
    result_gen = runner.run(
        user_id="u1",
        session_id="sess1",
        new_message=UserContent([Part(text="run")])
    )
    print("[DEBUG] Pipeline run complete. Results:")
    for result in result_gen:
        if isinstance(result, dict):
            pprint(result)
        else:
            try:
                pprint(result.__dict__)
            except Exception:
                print(str(result))

