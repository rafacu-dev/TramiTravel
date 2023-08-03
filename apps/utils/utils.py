
from django.shortcuts import redirect
from django.contrib.auth import logout

def toMoney(val) -> str:
    l = str(val).split(".")
    start = l[0]
    if len(l) == 1: return [start,"00"]
    end =  l[1]
    if len(end) == 1: end += "0"
    return f"{start}.{end}"


def permission_checked(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin_agency and request.user.agency and not request.user.agency.name and "/info-agency/" not in request.path:
            return redirect('ChangeInfoAgency')
        
        if (not request.user.is_authenticated  or not request.user.is_admin_agency) and "/info-agency/" in request.path:
            return redirect('index')

        return view_func(request, *args, **kwargs)
    return wrapper