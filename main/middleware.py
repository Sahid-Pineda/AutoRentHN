from django.shortcuts import redirect

class RolMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.restricciones = {
            '/admin/': [1],
            '/cliente/': [2],
            '/empleado/': [3],
        }

    def __call__(self, request):
        path = request.path

        # Deja ver URL super user
        #if path.startswith('/admin/'):
        #    return self.get_response(request)
        
        rol_id = request.session.get('rol_id')

        for ruta, roles_permitidos in self.restricciones.items():
            if path.startswith(ruta):
                if rol_id not in roles_permitidos:
                    return redirect('home')
                
        return self.get_response(request)