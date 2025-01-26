from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from mysite.models import IndividualItems, ItemType, ShoppingList, AmountType

@api_view(['PUT'])
def add_item(request):
    try:
        data = request.data
        item_type = ItemType.objects.get(id=data['itemType'])
        IndividualItems.objects.create(
            type=item_type,
            expirationDate=data['expirationDate'],
            amount=data['amount']
        )
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def remove_item(request):
    try:
        item_id = request.data['ID']
        item = IndividualItems.objects.get(id=item_id)
        item.delete()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def remove_items(request):
    try:
        ids = [item['ID'] for item in request.data]
        IndividualItems.objects.filter(id__in=ids).delete()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def new_type(request):
    try:
        data = request.data
        amount_type = AmountType.objects.get(id=data['amountType'])
        ItemType.objects.create(
            uniqueBarcode=data['uniqueBarcode'],
            name=data['name'],
            amountType=amount_type
        )
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def remove_type(request):
    try:
        unique_barcode = request.data['uniqueBarcode']
        item_type = ItemType.objects.get(uniqueBarcode=unique_barcode)
        if IndividualItems.objects.filter(type=item_type).exists():
            return Response("Cannot delete type, items exist", status=status.HTTP_400_BAD_REQUEST)
        item_type.delete()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def add_to_shopping_list(request):
    try:
        data = request.data
        item_type = ItemType.objects.get(id=data['itemType'])
        item, created = ShoppingList.objects.get_or_create(itemType=item_type)
        if not created:
            item.amount += data['amount']
            item.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def remove_from_shopping_list(request):
    try:
        data = request.data
        item_type = ItemType.objects.get(id=data['itemType'])
        item = ShoppingList.objects.get(itemType=item_type)
        item.amount -= data['amount']
        if item.amount <= 0:
            item.delete()
        else:
            item.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def purchase_item(request):
    try:
        data = request.data
        item_type = ItemType.objects.get(id=data['itemType'])
        shopping_item = ShoppingList.objects.get(itemType=item_type)
        if shopping_item.amount < data['amount']:
            return Response("Not enough items in shopping list", status=status.HTTP_400_BAD_REQUEST)
        shopping_item.amount -= data['amount']
        if shopping_item.amount <= 0:
            shopping_item.delete()
        else:
            shopping_item.save()
        IndividualItems.objects.create(
            type=item_type,
            expirationDate=data['expirationDate'],
            amount=data['amount']
        )
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
