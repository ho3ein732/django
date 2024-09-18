from rest_framework import serializers
from user.models import User
from blog.models import *
from product.models import *
from slider.models import *
from shop.models import *
from invoice.models import *
from user.models import *


# region user
class UserRegistrationSerializers(serializers.ModelSerializer):
    verification_code = serializers.CharField(max_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'verification_code']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        email = validated_data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'An account with this email already exists.'})
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SendVerificationForEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth',
                  'bio']


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['province', 'city', 'plague', 'postal_code']


# endregion


# region blog

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = '__all__'


class BlogSerializers(serializers.ModelSerializer):
    gallery = GallerySerializer(read_only=True, many=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'


# endregion


# region product

class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['text', 'user', 'created']


class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['feature', 'feature_value']


class ProductTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['tag']


class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = ['image']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['color', 'size', 'product']


class ProductSerializer(serializers.ModelSerializer):
    features = ProductFeatureSerializer(many=True, read_only=True)
    comments = ProductCommentSerializer(many=True, read_only=True)
    tags = ProductTagsSerializer(many=True, read_only=True)
    images = GallerySerializer(many=True, read_only=True)
    stock = StockSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'off', 'product_stock',
                  'brands', 'category', 'shop', 'created_at', 'updated_at',
                  'features', 'comments', 'images', 'stock', 'tags']


# endregion


# region slider

class SliderImageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderImageItem
        fields = "__all__"


class SliderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderImage
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['sliders']


# endregion


# region invoice


class InvoiceItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    stock = StockSerializer()

    class Meta:
        model = InvoiceItem
        fields = ['id', 'quantity', 'total_price', 'stock']


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    total_price = serializers.ReadOnlyField()



    class Meta:
        model = Invoice
        fields = ['id', 'user', 'items', 'total_price']


# endregion


# region Shop

class ShopGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopGallery
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    images = ShopGallerySerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ['name', 'description', 'email', 'created_at', 'updated_at', 'images']

# endregion
