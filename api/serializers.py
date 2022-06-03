from dataclasses import field
from imp import source_from_cache
from rest_framework import serializers
from .models import BakeryItems, Cart, CartOrders, Ingredients, Inventory, InventoryItems, MyUser


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("password does not match")
        return super().validate(attrs)

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)

    class Meta:
        model = MyUser
        fields = ["email", "password"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ["id", "item_name", "item_cost_price",
                  "item_selling_price", "item_quantity"]


class ItemsSerializer(serializers.ModelSerializer):
    item_ingredients = IngredientSerializer(many=True)

    class Meta:
        model = BakeryItems
        fields = ["id", "item_name", "item_ingredients", "item_description"]
        depth = 1

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields= ["name","email"]

class InventorySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model=Inventory
        fields=["user"]


class InventoryItemSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer()
    Ingredients = IngredientSerializer(many=True)
    
    class Meta:
        model=InventoryItems
        fields = ["inventory","Ingredients"]
    

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model=Cart
        fields=["user"]

class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    items = ItemsSerializer(many=True)
    
    class Meta:
        model=CartOrders
        fields = ["cart","items","order_total"]