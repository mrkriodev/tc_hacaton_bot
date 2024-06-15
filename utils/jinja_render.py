import aiofiles
from jinja2 import Template


async def render_sc_base_info_data(data: dict):
    async with aiofiles.open("sc_base_info_template.html", 'r') as file:
        sc_base_info_template_content = await file.read()
    sc_base_info_renderer = Template(sc_base_info_template_content)
    return sc_base_info_renderer.render(data)
