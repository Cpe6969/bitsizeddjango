from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from base.models import New, Review, User
from base.serializers import NewSerializer, ReviewSerializer

import mimetypes
import os

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_news(request):
    user = request.user
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    news = New.objects.filter(
        user=user,
        headline__icontains=query
    ).order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(news, 5)

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = NewSerializer(news, many=True)
    return Response({'news': serializer.data, 'page': page, 'pages': paginator.num_pages})

@api_view(['GET'])
def get_news(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    news = New.objects.filter(
        headline__icontains=query).order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(news, 5)

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = NewSerializer(news, many=True)
    return Response({'news': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def get_top_news(request):
    news = New.objects.filter(rating__gte=4).order_by('-rating')[:5]
    serializer = NewSerializer(news, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_news_details(request, pk):
    news = New.objects.get(_id=pk)
    serializer = NewSerializer(news, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_news(request):
    user = request.user

    newsitem = New.objects.create(
        user=user,
        headline='Sample Headline',
        image=None,
        description='Sample Description',
        rating=None,
        numReviews=0,
        price=None,
        createdAt='Sample Date'
    )

    serializer = NewSerializer(newsitem, many=False)
    return Response(serializer.data)

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_news(request, pk):
#     news = get_object_or_404(New, id=pk)
#     serializer = NewSerializer(instance=news, data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_news(request, pk):
    data = request.data
    news = New.objects.get(_id=pk)

    # Check if the authenticated user is the owner of the news item
    if request.user != news.user:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    news.headline = data['headline']
    news.description = data['description']
    news.category = data['category']

    news.save()

    serializer = NewSerializer(news, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_news(request, pk):
    news = get_object_or_404(New, _id=pk)

    # Check if the authenticated user is the owner of the news item
    if request.user != news.user:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    news.delete()
    return Response('News deleted')


@api_view(['POST'])
def upload_image(request):
    data = request.data

    news_id = data['news_id']
    news = New.objects.get(_id=news_id)

    news.image = request.FILES.get('image')
    news.save()

    return Response('Image was uploaded')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_news_review(request, pk):
    user = request.user
    new = get_object_or_404(New, _id=pk)
    data = request.data

    # Create the review
    review = Review.objects.create(
        user=user,
        name=user,
        new=new,
        rating=None,
        comment=data.get('comment', ''),
    )

    reviews = new.review_set.all()
    new.num_reviews = len(reviews)
    new.save()

    return Response('Review added')



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_news_review(request, pk):
    user = request.user
    review = get_object_or_404(Review, _id=pk, user=user)
    data = request.data
    review.rating = data['rating']
    review.comment = data['comment']
    review.save()

    news = review.news
    reviews = news.review_set.all()
    news.num_reviews = len(reviews)
    news.save()

    return Response('Review updated')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_news_review(request, pk):
    user = request.user
    review = get_object_or_404(Review, _id=pk, user=user)
    news = review.news
    review.delete()

    reviews = news.review_set.all()
    news.num_reviews = len(reviews)
    news.save()

    return Response('Review deleted')


@api_view(['GET'])
def get_user_reviews(request):
    user = request.user
    reviews = user.review_set.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
