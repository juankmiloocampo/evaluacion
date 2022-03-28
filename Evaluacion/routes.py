from controllers import *

routes = {
"register": "/jumi/register", "register_controllers": RegisterControllers.as_view("register_api"),
"login": "/jumi/login", "login_controllers": LoginControllers.as_view("login_api"),
"crearProductos": "/jumi/crear", "crear_controllers": CrearControllers.as_view("crear_api"),
"productos": "/jumi/productos", "productos_controllers": ProductosControllers.as_view("productos_api")
}
