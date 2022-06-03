from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from api.models import BakeryItems, Ingredients, Inventory, MyUser
from .serializers import IngredientSerializer, InventorySerializer, UserCreateSerializer, UserLoginSerializer,ItemsSerializer
from .renderer import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegister(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'msg': 'Registion success', 'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class UserLogin(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg': 'Login Success', 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_fields_error': ['Email or password is not valid']}})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddIngredients(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    def post(self, request, format=None):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            Ingredient = serializer.save()
            return Response({"success": "True"})
        return Response(serializer.errors)




#Retreving and creating Bakery items , overridding create method for manytomany object serailzation 
class BakeryItemView(ModelViewSet):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ItemsSerializer
    
    def get_queryset(self):
        bakery_items = BakeryItems.objects.all()
        return bakery_items
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        new_bakery_item = BakeryItems.objects.create(item_name=data["item_name"],item_description=data["item_description"])
        new_bakery_item.save()
        
        for ingredients in data["item_ingredients"]:
            ingredient_obj = Ingredients.objects.get(item_name=ingredients["item_name"])
            new_bakery_item.item_ingredients.add(ingredient_obj)
        
        serializer = ItemsSerializer(new_bakery_item)
        
        return Response(serializer.data)

#for creating and viewing the inventories 
class InventoryView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        inventories = Inventory.objects.all()
        return inventories
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        user_obj = MyUser.objects.get(email=data["email"])
        print(user_obj)
        new_inventory = Inventory.objects.create(user=user_obj)
        new_inventory.save()
        
        serializer = InventorySerializer(new_inventory)
        return Response(serializer.data)




        
    
    
    
    