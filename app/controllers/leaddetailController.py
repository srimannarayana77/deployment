from rest_framework.response import Response
from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from app.helpers.paginationHelper import paginationResponse
from app.models import Lead_Details
from app.helpers.filters import lead_details_filters
from app.helpers.sortHelper import sortHelper
from app.serializer.leaddatailSerializer import LeadDetailsSerializer
from app.constants.messageConstants import *
from rest_framework.exceptions import NotFound


class LeadDetailsView(viewsets.ViewSet):
    @api_view(['POST'])
    def create_lead(request):
        try:
            serializer = LeadDetailsSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': CREATE_LEAD_SUCCESSFULLY, 'data': serializer.data}, status=201)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    def retrieve_all_leads(request):
        try:
            paginator = PageNumberPagination()
            limit = int(request.query_params.get('limit', 10))
            page = int(request.query_params.get('page', 1))

            paginator.page_size = limit
            sortBy = request.query_params.get('sort_by', 'id')
            sortType = request.query_params.get('sort_type', 'desc')
            leads = Lead_Details.objects.all()
            leads =lead_details_filters(leads, request.query_params)

            leads = sortHelper(sortBy, sortType, leads)
            
            page_result = paginator.paginate_queryset(leads, request)
            
            serializer = LeadDetailsSerializer(page_result, many=True)

            response_data = paginationResponse(ALL_LEADS_RETRIEVED_SUCCESSFULLY, paginator.page.paginator.count, limit, page, serializer.data)

            return Response(response_data, status=200)
        
        except NotFound as e:  # Handle the InvalidPage exception
            return Response({"success": False, "errors": str(e)}, status=400)
        
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['GET'])
    def retrieve_single_lead(request, id):
        try:
            lead = Lead_Details.objects.get(id=id)
            serializer = LeadDetailsSerializer(lead)
            return Response({'success': True, 'message': SINGLE_LEAD_RETRIEVED_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except Lead_Details.DoesNotExist:
            return Response({'success': False, 'message': LEAD_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)

    # @api_view(['PUT'])
    # def update_lead(request, id):
    #     try:
    #         lead = Lead_Details.objects.get(id=id)
    #         serializer = LeadDetailsSerializer(lead, data=request.data)
    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save()
    #             return Response({'success': True, 'message': UPDATE_LEAD_SUCCESSFULLY, 'data': serializer.data}, status=200)
    #     except serializers.ValidationError as e:
    #         return Response({'success': False, 'message': e.detail}, status=422)
    #     except Lead_Details.DoesNotExist:
    #         return Response({'success': False, 'message': LEAD_NOT_FOUND}, status=404)
    #     except Exception as err:
    #         error_message = str(err)
    #         return Response({'success': False, 'errors': error_message}, status=500)

    @api_view(['DELETE'])
    def delete_lead(request, id):
        try:
            lead = Lead_Details.objects.get(id=id)
            lead.delete()
            return Response({'success': True, 'message': DELETE_LEAD_SUCCESSFULLY}, status=204)
        except Lead_Details.DoesNotExist:
            return Response({'success': False, 'message': LEAD_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
