from fastapi import BackgroundTasks


class Logging:
    async def _send_log(self):
        pass

    def __init__(self, background_task: BackgroundTasks):
        background_task.add_task(self._send_log)
