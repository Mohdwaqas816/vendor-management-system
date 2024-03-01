from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.db.models import Count, Avg
from django.db.models import F
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
# function based views


# health check endpoint whether this service is running or not
@api_view(['GET'])
def health(request):
    '''
     health check endpoint whether this service is running or not
    '''
    data = {
        "status": "up",
        "service": "vendor-management-service",
        "timestamp": datetime.now()
    }
    return Response(data,status=status.HTTP_200_OK)

############ api functions for vendor ##############

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def vendor_list_create(request):
    if request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def vendor_retrieve_update_destroy(request, pk):
    vendor = get_object_or_404(Vendor, vendor_id=pk)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vendor.delete()
        return Response({"message": "Vendor deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

############ api functions for vendor ended ##############


############ api functions for Purchase order  ##############

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def purchase_order_list_create(request):
    if request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        vendor_id = request.query_params.get('vendor_id', None)
        if vendor_id:
            vendor = get_object_or_404(Vendor, vendor_id=vendor_id)
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
        else:
            purchase_orders = PurchaseOrder.objects.all()

        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def purchase_order_retrieve_update_destroy(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, po_id=pk)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        purchase_order.delete()
        return Response({"message": "Purchase Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



############ function for calculating vendor performance #############

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_performance(request, pk):
    vendor = get_object_or_404(Vendor, vendor_id=pk)
    vendor.update_performance_metrics()

    serializer = VendorSerializer(vendor)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, po_id=pk)
    print("purchase order",purchase_order)

    if request.method == 'POST':
        acknowledgment_date = datetime.now()
        print("acknowledgment date",acknowledgment_date)
        purchase_order.acknowledgment_date = acknowledgment_date
        print("purchase order",purchase_order)
        purchase_order.save()

        vendor = purchase_order.vendor
        print("vendor",vendor)
        vendor.update_performance_metrics()

        return Response({"message": "Purchase Order acknowledged successfully."}, status=status.HTTP_200_OK)