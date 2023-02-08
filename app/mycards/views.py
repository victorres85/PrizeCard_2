"""Views for the mycards APIs."""

from rest_framework import status
from rest_framework.response import Response
import re
import pytesseract

from datetime import datetime
from rest_framework.decorators import action
from PIL import Image

import random

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import MyCards, Shopper, MyCardsHistory, Receipt
from mycards import serializers


def CodeGenerator():
    nums = [random.randrange(1, 9) for _ in range(6)]
    code = ''.join(str(num) for num in nums)
    return code


class MycardsViewSet(viewsets.ModelViewSet):
    """View for manage card APIs."""

    serializer_class = serializers.MycardsDetailSerializer
    queryset = MyCards.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve Myards for authenticated user."""
        shoppers = list(Shopper.objects.all().filter(
            user=self.request.user).values_list('id'))

        return self.queryset.filter(shopper=shoppers[0]).order_by('-id')

    def get_serializer_class(self):
        """Get serializer depending on the action"""
        if self.request.GET.get('code') is not None:
            return serializers.RewardSerializer
        elif self.action == 'list':
            return serializers.MycardsSerializer
        else:
            return serializers.MycardsDetailSerializer

    def update(self, request, pk=None, *args, **kwargs):
        '''
        update the image, check if image contains the
        name of the business if so, increase the points by 1
        '''
        myCards_obj = MyCards.objects.get(id=pk)
        data = request.data
        myCards_obj.image = data["image"]
        myCards_obj.save()
        image = myCards_obj.image
        result = pytesseract.image_to_string(Image.open(image))
        company = myCards_obj.card.company.company_name
        total_points = myCards_obj.card.points_needed
        date_pattern = r"\d{2}[/-]\d{2}[/-]\d{4}"
        hour_pattern = r"\d{2}[:]\d{2}[:]\d{2}"
        date = re.findall(date_pattern, result)
        hour = re.findall(hour_pattern, result)
        # validade image and add a point if everything is ok
        key = company + str(date) + str(hour)

        if company in result:
            if not Receipt.objects.filter(receipt_key=key).exists:
                raise 'Receipt already in use'
            else:
                Receipt.objects.create(
                    receipt_key=key,
                )
                myCards_obj.points += 1
                # check if all the points have been acumulated,
                # send an email with a congrats message and generates a
                # code to be used by the custumer
                if myCards_obj.points == total_points:
                    myCards_obj.points = 0
                    # card_completed.delay(myCards_obj.profile.user.pk)
                    MyCardsHistory.objects.create(
                        company=myCards_obj.card.company,
                        shopper=myCards_obj.shopper,
                        card=myCards_obj.card,
                        finalized=datetime.now(),
                        code=CodeGenerator(),
                        )

        else:
            return Response("Please take a new picture")

        myCards_obj.save()
        serializer = serializers.MycardsSerializer(myCards_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def cardslist(self, request, pk=None):
        user_id = request.user
        cards = MyCards.objects.get(user=user_id)
        serializer = serializers.MycardsSerializer(cards)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save()
