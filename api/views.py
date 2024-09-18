from django.shortcuts import render, get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework import generics
from user.models import User
from rest_framework import views
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .authentication import *
from django.core.cache import cache
from rest_framework import mixins, generics
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication


# region user

class UserListApiView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializers

    def get(self, *args, **kwargs):
        users = User.objects.all()
        serializer = UserListSerializers(users, many=True)
        return Response(serializer.data)


class SendVerificationCodeApiView(views.APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=SendVerificationForEmailSerializer,
        responses={201: SendVerificationForEmailSerializer}
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        verification_code = generate_random_code()
        cache.set(f'{email}', verification_code, timeout=300)
        print(verification_code)  # چک

        return Response({'message': f'Verification code send to {email}'}, status=status.HTTP_200_OK)


class UserRegistrationWithCodeApiView(views.APIView):
    serializer_class = UserRegistrationSerializers
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegistrationSerializers,
        responses={201: UserRegistrationSerializers},
    )
    def post(self, request: Response, *args, **kwargs):
        serializer = UserRegistrationSerializers(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['verification_code']
            if not email or not code:
                raise ValueError('kkkkkkkkkk')
            verification_code = cache.get(email)
            if not verification_code:
                raise ValueError('no found!')
            if verification_code != code:
                raise ValueError('invalid verification code')
            serializer.save()
            return Response({'message': "Created account"}, status=status.HTTP_201_CREATED)


class UserDetailApiView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializers

    def get(self, request: Request, pk):
        return self.retrieve(request, pk)


class UserUpdateApiView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateUserSerializer

    def get_object(self):
        return self.request.user

    # def put(self, request, *args, **kwargs):
    #     response = super().put(request, *args, **kwargs)
    #     response.data['message'] = 'اکانت شما با موفقیت ویرایش یافت'


class UserAddAddressApiView(generics.CreateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

    def perform_save(self, serializer):
        serializer.save(user=self.request.user)



# endregion


# region blog

class BlogDetailApiView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers


class BlogListApiView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers


# endregion


# region product

class ListProductApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DetailProductApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# endregion


# region Shop

class ListShopApiView(generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class DetailShopApiView(generics.RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


# endregion


# region invoice


class InvoiceDetailApiView(generics.RetrieveAPIView):
    serializer_class = InvoiceSerializer

    def get_object(self):
        invoice, created = Invoice.objects.get_or_create(user=self.request.user)
        return invoice


class AddToInvoiceApiView(generics.CreateAPIView):
    serializer_class = InvoiceItemSerializer

    def create(self, request, *args, **kwargs):
        stock_data = request.data.get('stock', {})
        quantity = request.data.get('quantity')
        color = stock_data.get('color')
        product_id = stock_data.get('product')
        size = stock_data.get('size')

        if not all([quantity, color, product_id, size]):
            return Response({'error': 'all field are required!'})

        try:
            stock = Stock.objects.get(product_id=product_id, color=color, size=size)
        except Stock.DoesNotExist:
            return Response({'error': 'not found stock!'}, status=status.HTTP_404_NOT_FOUND)

        if stock.product.quantity < int(quantity):
            return Response({'error': 'no stock'})

        invoice, created = Invoice.objects.get_or_create(user=request.user)

        invoice_item, created = InvoiceItem.objects.get_or_create(invoice=invoice, stock=stock,
                                                                  defaults={'quantity': int(quantity)})

        if not created:
            invoice_item.quantity += int(quantity)
            invoice_item.save()

        serializer = self.get_serializer(invoice_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateInvoiceItemApiView(generics.UpdateAPIView):
    serializer_class = InvoiceItemSerializer
    queryset = InvoiceItem.objects.all()

    def get_object(self):
        invoice_item = super().get_object()
        if invoice_item.invoice.user != self.request.user:
            raise PermissionError('you do not have access!')
        return invoice_item

    def update(self, request, *args, **kwargs):
        stock_date = request.data.get('stock', {})

        quantity = request.data.get('quantity')
        color = stock_date.get('color')
        size = stock_date.get('size')
        product_id = stock_date.get('product')

        if not all([quantity, color, size, product_id]):
            return Response({'error': 'all data is required!'})

        try:
            stock = Stock.objects.get(
                product_id=product_id,
                size=size,
                color=color
            )
        except Stock.DoesNotExist:
            return Response({'error': 'not found stock!'}, status=status.HTTP_404_NOT_FOUND)

        if stock.product.quantity < int(quantity):
            return Response({'error': 'no stock'})

        invoice_item = self.get_object()
        invoice_item.stock = stock
        invoice_item.quantity = quantity
        invoice_item.save()
        serializer = self.get_serializer(invoice_item)
        return Response({'data': serializer.data, 'message': 'InvoiceItem updated!'}
                        , status=status.HTTP_200_OK)


class RemoveInvoiceItemApiView(generics.DestroyAPIView):
    queryset = InvoiceItem.objects.all()

    def delete(self, request, *args, **kwargs):
        stock_id = kwargs.get('pk')

        if not stock_id:
            return Response({'error': 'stock id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invoice_item = InvoiceItem.objects.get(stock_id=stock_id, invoice__user=request.user)
        except InvoiceItem.DoesNotExist:
            return Response({'error': 'item not found'}, status=status.HTTP_404_NOT_FOUND)

        invoice_item.delete()
        return Response({'message': 'item removed from Invoice item!'}, status=status.HTTP_200_OK)
# endregion
