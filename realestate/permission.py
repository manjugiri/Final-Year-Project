# def is_agent(function):
#     def wrapper(request, *args, **kwargs):
#         user = request.user
#         if user.agent.is_approved:
#         	return True
#         return False
#     return wrapper
from django.shortcuts import render,redirect


def is_agent(view_func):
    def _wrapped_view_func(request, *args, **kwargs): 
    	user = request.user
    	try:
    		if user.agent.is_approved:
    			return redirect('addproperty')
    		else:
    			return redirect('applyagent')
    	except:
    		return redirect('applyagent')
    return _wrapped_view_func