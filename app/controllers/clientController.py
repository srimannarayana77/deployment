from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate
from rest_framework import viewsets
from app.helpers.paginationHelper import paginationResponse
from app.helpers.filters import client_filters
from app.helpers.sortHelper import sortHelper
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from app.middlewares.decorators import require_token
from app.models import Client
from app.serializer.clientSerilaizer import ClientSerializer,getClientSerializer
from app.constants.messageConstants import *
from rest_framework.exceptions import NotFound

class ClientView(viewsets.ViewSet):
    @api_view(['POST'])
    def create_client(request):
        try:
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': CREATE_CLIENT_SUCCESSFULLY, 'data': serializer.data}, status=201)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
    
    @api_view(['GET']) 
    @require_token
    def retrieve_all_clients(request):
        try:  
            paginator = PageNumberPagination()
            limit = int(request.query_params.get('limit', 10))
            page = int(request.query_params.get('page', 1))

            paginator.page_size = limit

            sortBy = request.query_params.get('sort_by', 'id')
            sortType = request.query_params.get('sort_type', 'desc')    

            clients = Client.objects.all() 

            clients = client_filters(clients, request.query_params)

            clients = sortHelper(sortBy, sortType, clients)

            page_result = paginator.paginate_queryset(clients, request)

            serializer = ClientSerializer(page_result, many=True)
            response_data = paginationResponse(ALL_CLIENTS_RETRIEVED_SUCCESSFULLY, paginator.page.paginator.count, limit, page, serializer.data)
            return Response(response_data, status=200)
          
        except NotFound as e:  # Handle the InvalidPage exception
            return Response({"success": False, "errors": str(e)}, status=400)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
    
    @api_view(['GET'])  
    def retrieve_single_client(request, id):
        try:              
            client = Client.objects.get(id=id)
            serializer = getClientSerializer(client)
            return Response({'success': True, 'message': SINGLE_CLIENT_RETRIEVED_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except Client.DoesNotExist:
            return Response({'success': False, 'message': CLIENT_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
    
    @api_view(['PUT'])
    def update_client(request, id):
        try:
            client = Client.objects.get(id=id)
            serializer = ClientSerializer(client, data=request.data)  
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': UPDATE_CLIENT_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Client.DoesNotExist:
            return Response({'success': False, 'message': CLIENT_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
      
    @api_view(['DELETE'])     
    def delete_client(request, id):
        try:
            client = Client.objects.get(id=id)
            client.delete() 
            return Response({'success': True, 'message': DELETE_CLIENT_SUCCESSFULLY}, status=204)
        except Client.DoesNotExist:
            return Response({'success': False, 'message': CLIENT_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
          
    @api_view(['POST'])
    def client_sign_in(request):
         try:
            email_address = request.data.get('email_address')
            password = request.data.get('password')
            if not email_address:
             return Response({'success': False, 'message': CLIENT_EMAIL_REQUIRED}, status=422)

            if not password:
             return Response({'success': False, 'message': CLIENT_PASSWORD_REQUIRED}, status=422)

            user = Client.objects.get(email_address=email_address)

            user == authenticate(request, email_address=email_address, password=password)

            if user is not None and check_password(password,user.password):

                refresh = RefreshToken.for_user(user)
                
                return Response({'success': True, 'message': AUTHENTICATION_SUCCESSFULLY, 'refresh': str(refresh), 'access': str(refresh.access_token)}, status=200)
            else:
                return Response({'success': False, 'message': PASSWORD_INCORRECT}, status=401)

         except Client.DoesNotExist:
            return Response({'success': False, 'message': CLIENT_NOT_FOUND}, status=404)
         
         except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'message': error_message}, status=500)
