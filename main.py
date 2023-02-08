import jinja2
import aiohttp_jinja2
from aiohttp import web
import os
from zipfile import ZipFile
import shutil

app = web.Application()
routes = web.RouteTableDef()

aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "Templates"))
)


@routes.get('/')
async def homepage(request):
    response = aiohttp_jinja2.render_template("index.html", request, context={})

    return response


@routes.post('/a')
async def file_uploaded(request):
    data = await request.post()
    zip_file = data['zip'].file
    shutil.rmtree(os.path.join(os.getcwd(), "Files"))
    with ZipFile(zip_file) as zip:
        li = zip.namelist()
        zip.extractall(os.path.join(os.getcwd(), "Files"))

    c = {'names': li}
    response = aiohttp_jinja2.render_template("file.html", request, context=c)

    return response


app.add_routes(routes)
web.run_app(app)
