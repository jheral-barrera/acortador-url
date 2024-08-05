from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Enlace
from .serializers import EnlaceSerializer

import shortuuid

def api_documentacion(request):
    return render(request, 'documentacion.html')

@api_view(['GET', 'POST'])
def acortar_enlace(request):
    if request.method == 'GET':
        return Response({'url_original': 'Aquí debe ir el URL'}, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        URL_ORIGINAL = 'url_original'

        serializer = EnlaceSerializer(data = request.data)
        url_original = request.data['url_original']

        validar_url = Enlace.validar_url_existente(URL_ORIGINAL, url_original)

        if validar_url: # REFACTORIZAR ESTA MIERTA SI O SI            
            enlace = Enlace.objects.get(url_original=url_original)
            url_acortado = request.build_absolute_uri(f'/{enlace.url_acortado}/')
            return Response({'url_acortada': url_acortado}, status=status.HTTP_200_OK)

        if serializer.is_valid():
            url_serializado = serializer.validated_data['url_original']
            id_acortado = shortuuid.uuid()[:8]
            
            Enlace.objects.create(
                url_original=url_serializado, 
                url_acortado=id_acortado
            )

            url_acortado = request.build_absolute_uri(f'/{id_acortado}/')
            return Response({'url_acortado': url_acortado}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def personalizar_enlace(request):
    if request.method == 'GET':
        return Response({'url_original': 'Aquí debe ir el URL', 'url_personalizado': 'Aquí debe ir el texto'}, status=status.HTTP_200_OK)

    if request.method == 'POST':
        URL_PERSONALIZADO = 'url_personalizado'

        serializer = EnlaceSerializer(data = request.data)
        url_personalizado = request.data['url_personalizado']

        validar_url = Enlace.validar_url_existente(URL_PERSONALIZADO, url_personalizado)

        if validar_url:
            enlace = Enlace.objects.get(URL_PERSONALIZADO=url_personalizado)
            url_acortado = request.build_absolute_uri(f'/{enlace.url_personalizado}/')
            return Response({'url_personalizada': url_acortado}, status=status.HTTP_200_OK)
        
        if serializer.is_valid():
            url_original_serializado = serializer.validated_data['url_original']
            url_personalizado_serializado = serializer.validated_data['url_personalizado']
            id_acortado = shortuuid.uuid()[:8]

            Enlace.objects.create(
                url_original=url_original_serializado, 
                url_acortado=id_acortado, 
                url_personalizado=url_personalizado_serializado
            )

            url_acortado = request.build_absolute_uri(f'/{url_personalizado}/')
            return Response({'url_acortado': url_acortado}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def redireccionar_enlace(request, id_url_acortado):
    try:
        enlace = Enlace.objects.get(
            Q(url_acortado=id_url_acortado) |
            Q(url_personalizado=id_url_acortado)
        )
    except:
        return Response({'error': 'No fue posible redireccionar el enlace'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        enlace.registrar_clic()
        return redirect(enlace.url_original)
    
@api_view(['GET'])
def analizar_enlace(request, id_url_acortado):
    try:
        enlace = Enlace.objects.get(
            Q(url_acortado=id_url_acortado) |
            Q(url_personalizado=id_url_acortado)
        )
    except:
        return Response({'error': 'ni idea que paso'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        body = {
            'url_original': enlace.url_original,
            'fecha_creacion': enlace.fecha_creacion,
            'fecha_ultimo_acceso': enlace.fecha_ultimo_clic,
            'clics_totales': enlace.clics_totales
        }
        return Response(body, status=status.HTTP_200_OK)
    

# # NO UTILIZABLE POR EL USUARIO
# @api_view(['GET'])
# def manejo_lista(request):
#     try:
#         enlace = Enlace.objects.all()
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = EnlaceSerializer(enlace, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        
# # NO UTILIZABLE POR EL USUARIO
# @api_view(['GET', 'PUT', 'DELETE'])
# def manejo_enlaces(request, pk):
#     try:
#         enlace = Enlace.objects.get(pk=pk)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = EnlaceSerializer(enlace)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         serializer = EnlaceSerializer(enlace, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.errors, status=status.HTTP_200_OK)
    
#     if request.method == 'DELETE':
#         enlace.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)