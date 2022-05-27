# import re
# from django.http import JsonResponse
# from .models import Drink
# from .serializers import DrinkSerializer
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# @api_view(['GET', 'POST'])
# def drink_list(request, format=None):
#     if request.method == 'GET':
#         # get all drinks
#         drinks = Drink.objects.all()
#         # serialize them
#         serializer = DrinkSerializer(drinks, many=True)
#         # return json
#         return Response(serializer.data)

#     if request.method == 'POST':
#         # serialize them
#         serializer = DrinkSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # return json
#             return Response(serializer.data, status=status.HTTP_201_created)

# @api_view(['GET', 'PUT', 'DELETE'])
# def drink_detail(request,id,format=None):
    
#     try:
#         drink=Drink.objects.get(pk=id)
#     except Drink.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     # View Read
#     if request.method == 'GET':
#        serializer = DrinkSerializer(drink)
#        return Response(serializer.data)

#     # View Update
#     elif request.method == 'PUT':
#         # serialize them
#         serializer = DrinkSerializer(drink, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # return json
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # View Delete
#     elif request.method == 'DELETE':
#         # serialize them
#         drink.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)