from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from app.helpers.paginationHelper import paginationResponse
from app.helpers.sortHelper import sortHelper
from rest_framework.decorators import api_view 
from app.models import Projects
from app.serializer.projectSerializer import ProjectsSerializer,getProjectsSerializer
from app.constants.messageConstants import *
from rest_framework.exceptions import NotFound 
class ProjectView(viewsets.ViewSet):
    @api_view(['POST'])
    def create_project(request):
        try:
            serializer = ProjectsSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': CREATE_PROJECT_SUCCESSFULLY, 'data': serializer.data}, status=201)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
    
    @api_view(['GET']) 
    def retrieve_all_projects(request):
        try:  
            paginator = PageNumberPagination()
            limit = int(request.query_params.get('limit', 10))
            page = int(request.query_params.get('page', 1))

            paginator.page_size = limit

            sortBy = request.query_params.get('sort_by', 'id')
            sortType = request.query_params.get('sort_type', 'desc') 

            projects = Projects.objects.all() 
            
            projects = sortHelper(sortBy, sortType, projects) 

            page_result = paginator.paginate_queryset(projects, request)

            serializer = ProjectsSerializer(page_result, many=True)

            response_data = paginationResponse(ALL_PROJECTS_RETRIEVED_SUCCESSFULLY, paginator.page.paginator.count, limit, page, serializer.data)
            
            return Response(response_data, status=200) 
        
        except NotFound as e:  # Handle the InvalidPage exception
            return Response({"success": False, "errors": str(e)}, status=400) 
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
    
    @api_view(['GET'])  
    def retrieve_single_project(request, id):
        try:              
            project = Projects.objects.get(id=id)
            serializer = getProjectsSerializer(project)
            return Response({'success': True, 'message': SINGLE_PROJECT_RETRIEVED_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except Projects.DoesNotExist:
            return Response({'success': False, 'message': PROJECT_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
    
    @api_view(['PUT'])
    def update_project(request, id):
        try:
            project = Projects.objects.get(id=id)
            serializer = ProjectsSerializer(project, data=request.data)  
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': UPDATE_PROJECT_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Projects.DoesNotExist:
            return Response({'success': False, 'message': PROJECT_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
      
    @api_view(['DELETE'])     
    def delete_project(request, id):
        try:
            project = Projects.objects.get(id=id)
            project.delete() 
            return Response({'success': True, 'message': DELETE_PROJECT_SUCCESSFULLY}, status=204)
        except Projects.DoesNotExist:
            return Response({'success': False, 'message': PROJECT_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
