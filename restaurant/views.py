from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Booking, MenuItem
from .serializers import BookingSerializer, MenuSerializer


def index(request):
    """Serve the static-powered home page."""
    return render(request, "index.html", {})


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
