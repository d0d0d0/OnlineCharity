from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import authenticate,login,logout
from json import dumps
from django.http import HttpResponse
from API.serializers import Serializer, CharitySerializer
from models import *
import time


def session_process(request, is_logout=False):
    """
    Session expiricy in 5 minutes
    """
    try:
        last_activity = request.session['last_activity']
        now = time.time()
        if (now - last_activity) > 300.0 or is_logout:
            del request.session['last_activity']
            del request.session['charity']
            logout(request)
            return True
        request.session['last_activity'] = now
        return False
    except:
        return True


@api_view(['GET', 'POST', ])
def login_view(request):
    """
    Show login form
    """
    try:
        context = {'message': 'Redirected.'}
        return redirect('/index', context)
    except Exception as e:
        context = {'message': e}
        return redirect('/index', context)


@api_view(['GET','POST', ])
@renderer_classes((TemplateHTMLRenderer,))
def login_user(request):
    """
    Login to system
    """
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['last_activity'] = time.time()
                try:
                    request.session['charity'] = CharitySerializer().serialize(obj=Charity.objects.get(username=username))
                    return Response({'message':' Successfully logged in.',
                                    'data': {'name': request.session['charity']['name'],
                                    'address': request.session['charity']['address'],
                                    'description': request.session['charity']['description']}},
                                    template_name='index.html')
                except Exception as e:
                    print e
                    return Response({'message': e}, template_name='login.html')
            else:
                return Response({'message': 'Account is disabled.'}, template_name='login.html')
        else:
            return Response({'message': 'Invalid username or password.'}, template_name='login.html')
    except Exception as e:
        return Response({'message': e}, template_name='login.html')


@api_view(['GET','POST', ])
@renderer_classes((TemplateHTMLRenderer,))
def logout_view(request):
    try:
        session_process(request, is_logout=True)
        return Response({'message': 'Successfully logged out.'}, template_name='login.html')
    except Exception as e:
        return Response({'message': e}, template_name='login.html')


@api_view(['GET', 'POST'])
@renderer_classes((TemplateHTMLRenderer,))
def repr_list(request, typ):
    """
    List all items, or create a new item of given type.
    """
    try:
        if session_process(request):
            return Response({'message': 'Redirected'}, template_name='login.html',
                            status=status.HTTP_301_MOVED_PERMANENTLY)
        convert = Serializer(typ).serializer
        if request.method == 'GET':
            serialized = convert().get_all(charity=request.session['charity'])
            return HttpResponse(dumps(serialized), content_type="application/json")
        elif request.method == 'POST':
            print request.data
            response = convert().deserialize(request.data, request.session['charity']['username'])
            if response['availability']:
                return HttpResponse(dumps(response), content_type="application/json")
            else:
                return HttpResponse(dumps(response), content_type="application/json")
    except KeyError:
        return Response({'message': 'No such item.'}, status=status.HTTP_302_FOUND)
    except Exception as e:
        return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@renderer_classes((TemplateHTMLRenderer,))
def repr_indv(request, typ, tc_no=None, name=None):
    """
    Get, update or delete an.
    """
    try:
        if session_process(request):
            return Response({'message': 'Redirected'}, template_name='login.html',
                            status=status.HTTP_301_MOVED_PERMANENTLY)
        convert = Serializer(typ).serializer
        if typ == 'Person' and tc_no:
            item = convert.Meta.model.objects.get(tc_no=tc_no)
            if item.charity.name != request.session['charity']['name']:
                return Response({'message': 'Does not authorize to charity.'}, status=status.HTTP_400_BAD_REQUEST)
        elif typ == 'Charity' and name:
            item = convert.Meta.model.objects.get(name=name)
        if item:
            if request.method == 'GET':
                return Response(dumps(convert().serialize(item)), status=status.HTTP_200_OK)
            elif request.method == 'PUT':
                print request.data
                response = convert().check(request.data)
                if response['availability']:
                    item.delete()
                    convert().deserialize(request.data, request.session['charity']['username'])
                return HttpResponse(dumps(response), content_type="application/json")
            elif request.method == 'DELETE':
                response = item.delete()
                if response:
                    return HttpResponse(dumps({'availability': True}), content_type="application/json")
        else:
            return Response({'message': 'Error occurred.'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'message': 'No such item.'}, status.HTTP_302_FOUND)
    except Exception as e:
        return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)