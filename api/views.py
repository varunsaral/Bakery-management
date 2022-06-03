from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from api.models import BakeryItems, Cart, CartOrders, Ingredients, Inventory, InventoryItems, MyUser
from .serializers import CartItemSerializer, IngredientSerializer, InventoryItemSerializer, InventorySerializer, UserCreateSerializer, UserLoginSerializer,ItemsSerializer,CartSerializer
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
    permission_classes = [IsAuthenticated,IsAdminUser]
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
    serializer_class = InventorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    
    def get_queryset(self):
        inventories = Inventory.objects.all()
        return inventories
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        user_obj = MyUser.objects.get(email=data["email"])
        new_inventory = Inventory.objects.create(user=user_obj)
        new_inventory.save()
        
        serializer = InventorySerializer(new_inventory)
        return Response(serializer.data)

class InventoryItemsView(ModelViewSet):
    serializer_class = InventoryItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    def get_queryset(self):
        inventories_item = InventoryItems.objects.all()
        return inventories_item    

    def create(self,request,*args, **kwargs):
        data = request.data
        
        inventory_obj = Inventory.objects.get(user__email=data["email"])
        new_inventory_item = InventoryItems.objects.create(inventory=inventory_obj)
        new_inventory_item.save()
        
        for ingredients in data["Ingredients"]:
            ingredient_obj = Ingredients.objects.get(item_name=ingredients["item_name"])
            new_inventory_item.Ingredients.add(ingredient_obj)
        
        serializer = InventoryItemSerializer(new_inventory_item)
        return Response(serializer.data)
        
        
class CartView(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        carts = Cart.objects.all()
        return carts
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        user_obj = MyUser.objects.get(email=data["email"])
        new_cart = Cart.objects.create(user=user_obj)
        new_cart.save()
        
        serializer = CartSerializer(new_cart)
        return Response(serializer.data)
    
class CartItemView(ModelViewSet):
    serializer_class = CartItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        cart_order = CartOrders.objects.all()
        return cart_order
    
    def create(self,request,*args, **kwargs):
        data = request.data
        
        cart_obj = Cart.objects.get(user__email=data["email"])
        new_cart_order = CartOrders(cart=cart_obj,order_total=data["order_total"])
        new_cart_order.save()
        
        for item in data["items"]:
            item_obj = BakeryItems.objects.get(item_name=item["item_name"])
            new_cart_order.items.add(item_obj)
            
        serialzer = CartItemSerializer(new_cart_order)
        return Response(serialzer.data)
              
