from django.http import QueryDict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import Vessel
from .serializers import VesselsSerializer


@api_view(['GET'])
@permission_classes((AllowAny,))
def getRoutes():
    routes = [
        'GET /api',
        'GET /api/token',
        'POST /api/token/refresh',
        'GET /api/vessels',
        'GET /api/vessels/all',
        'POST /api/vessels/add',
        'PUT /api/vessels/update',
        'DELETE /api/vessels/remove',

    ]
    return Response(routes)


@api_view(['GET'])
@permission_classes((AllowAny,))
def retrieveVessels(request):
    # Reterive all vessels
    try:
        vessels = Vessel.objects.all()
        response = paginateQueryResponse(vessels, VesselsSerializer, request)
        return response
    except Exception as e:
        message = formatResponse(
            message=str(e), status=status.HTTP_404_NOT_FOUND)
        return Response(message, status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def retrieveUserVessels(request):
    # Django rest framework provides exception handling via views which a better way to handle
    # exceptions. for this assignment it should do for now
    try:
        owner = request.user.id
        vessels = Vessel.objects.filter(owner=owner)
        response = paginateQueryResponse(vessels, VesselsSerializer, request)

        return response
    except Exception as e:
        message = formatResponse(
            message=str(e), status=status.HTTP_404_NOT_FOUND)
        return Response(message, status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def retrieveUserVessel(request, id):
    # Django rest framework provides exception handling via views which a better way to handle
    # exceptions. for this assignment it should do for now
    try:
        owner = request.user.id
        vessel = Vessel.objects.get(id=id, owner=owner)
        serializer = VesselsSerializer(vessel)

        message = formatResponse(data=serializer.data,
                                 status=status.HTTP_200_OK)
        return Response(message, status.HTTP_200_OK)
    except Exception as e:
        message = formatResponse(
            message=str(e), status=status.HTTP_404_NOT_FOUND)
        return Response(message, status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def addVessel(request):
    try:
        data = QueryDict.fromkeys(
            ['owner'], value=request.user.id, mutable=True)
        data.update(request.data)
        serializer = VesselsSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        message = formatResponse(data=serializer.data,
                                 status=status.HTTP_201_CREATED)
        return Response(message, status=status.HTTP_201_CREATED)
    except Exception as e:
        message = formatResponse(message="Vessel with this NACCS code already exists",
                                 status=status.HTTP_409_CONFLICT)
        return Response(message, status=status.HTTP_409_CONFLICT)


@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def updateVessel(request, id):
    try:
        vessel = Vessel.objects.get(id=id)

        if vessel.owner.id != request.user.id:
            message = formatResponse(
                message="You don't have permission to access this resource",
                status=status.HTTP_403_FORBIDDEN
            )
            return Response(message, status=status.HTTP_403_FORBIDDEN)

        serializer = VesselsSerializer(vessel, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        message = formatResponse(data=serializer.data,
                                 status=status.HTTP_200_OK)
        return Response(message)
    except Exception:
        message = formatResponse(
            message="Resource not found",
            status=status.HTTP_404_NOT_FOUND
        )
        return Response(message, status.HTTP_404_NOT_FOUND)


@ api_view(['DELETE'])
@ permission_classes((IsAuthenticated,))
def deleteVessel(request, id):
    message = formatResponse(status.HTTP_202_ACCEPTED)
    try:
        vessel = Vessel.objects.get(id=id)
        if vessel.owner.id != request.user.id:
            message = formatResponse(
                message="You don't have permission to access this resource",
                status=status.HTTP_403_FORBIDDEN
            )
            return Response(message, status=status.HTTP_403_FORBIDDEN)

        vessel.delete()
        return Response(message, status=status.HTTP_202_ACCEPTED)
    except:
        return Response(message, status=status.HTTP_202_ACCEPTED)

# This the wrong way to go about this but for this assignment it should suffice


def formatResponse(status, data=None, message=None):
    response = {}

    response['status'] = status
    if message != None:
        response['message'] = message
    elif data != None:
        response['data'] = data

    return response

# I dont know te right way to do paigination using a function base pattren - for it, it should suffice


def paginateQueryResponse(modelQuery, modelSerializer, request, message=None, status=status.HTTP_200_OK, pageSize=None):
    paginator = PageNumberPagination()
    paginator.page_size = pageSize if pageSize != None else paginator.page_size
    result_page = paginator.paginate_queryset(modelQuery, request)
    serializer = modelSerializer(result_page, many=True)
    message = formatResponse(status, data=serializer.data, message=message)
    return paginator.get_paginated_response(message)
