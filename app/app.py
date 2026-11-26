from nicegui import ui
from frontend import MainProject

@ui.page('/')
async def run_app():
    Page=MainProject()
    await Page.async_init()

if __name__ in {"__main__","__mp_main__"}:
    ui.run(
        title="Engine Monitoring",
        native=False,
        reload=True,
        port=8080,
        show=False,
        dark=True
    )