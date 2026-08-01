from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(
    directory="app/templates"
)


# Disable Jinja template cache
templates.env.cache = {}