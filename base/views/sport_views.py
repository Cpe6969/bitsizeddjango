from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from base.models import Sport, Review, User
from base.serializers import SportSerializer, ReviewSerializer

import mimetypes
import os

@api_view(['GET'])
def get_sport(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
        
    sports = Sport.objects.filter(
        headline__icontains=query).order_by('-createdAt')
    
    page = request.query_params.get('page')
    paginator = Paginator(sports, 5)

    try:
        sports = paginator.page(page)
    except PageNotAnInteger:
        sports = paginator.page(1)
    except EmptyPage:
        sports = paginator.page(paginator.num_pages)

    if page == None:
        page = 1
        
    page = int(page)
    print('Page:', page)
    serializer = SportSerializer(sports, many=True)
    return Response({'sports': serializer.data, 'page': page, 'pages': paginator.num_pages})

@api_view(['GET'])
def get_top_sport(request):
    sport = Sport.objects.filter(rating__gte=4).order_by('-rating')[:5]
    serializer = SportSerializer(sport, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_sport_details(request, pk):
    sport = get_object_or_404(Sport, _id=pk)
    serializer = SportSerializer(sport)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_sport(request):
    user = request.user
    sport = Sport.objects.create(user=user, headline='Sample headline')
    serializer = SportSerializer(sport)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_sport(request, pk):
    sport = get_object_or_404(Sport, id=pk)
    serializer = SportSerializer(instance=sport, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_sport(request, pk):
    sport = get_object_or_404(Sport, id=pk)
    sport.delete()
    return Response('Sport news deleted')


@api_view(['POST'])
def upload_image(request):
    data = request.data
    sport_id = data.get('sport_id')
    sport = get_object_or_404(Sport, id=sport_id)

    sport.image = request.FILES.get('image')
    sport.save()

    return Response('Image uploaded')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_sport_review(request, pk):
    user = request.user
    sport = get_object_or_404(Sport, _id=pk)
    data = request.data

    review = Review.objects.create(
        user=user,
        name=user,
        sport=sport,
        rating=data['rating'],
        comment=data['comment'],
    )

    reviews = sport.review_set.all()
    sport.num_reviews = len(reviews)
    sport.save()

    return Response('Review added')


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_sport_review(request, pk):
    user = request.user
    review = get_object_or_404(Review, _id=pk, user=user)
    data = request.data
    review.rating = data['rating']
    review.comment = data['comment']
    review.save()

    sport = review.sport
    reviews = sport.review_set.all()
    sport.num_reviews = len(reviews)
    sport.save()

    return Response('Review updated')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_sport_review(request, pk):
    user = request.user
    review = get_object_or_404(Review, _id=pk, user=user)
    sport = review.sport
    review.delete()

    reviews = sport.review_set.all()
    sport.num_reviews = len(reviews)
    sport.save()

    return Response('Review deleted')


@api_view(['GET'])
def get_user_reviews(request):
    user = request.user
    reviews = user.review_set.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

