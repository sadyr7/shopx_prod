from django.urls import path
from .views import (
    SellerSendCodeView,
    CodeCheckingView,
    # UserResetPasswordView,
    SellerRegisterView,
    SellerLoginView,
    SellerVerifyRegisterCode,
    BecomeSellerView,
    SellerDetailApiview,
    SellerListApiview,
    SellerUpdateProfileShopApi,
    LogoutView,
    ChangePasswordAPIVIew
)
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
urlpatterns = [


#     path('refresh-token/', TokenRefreshView.as_view()),
    path('send-code-to-email/', SellerSendCodeView.as_view(), name='seller-send_password_reset_code'), # отправить code в почту

    path('forget-password/reset/',SellerSendCodeView.as_view(), name='seller-reset_password'), # забыл пароль при входе
    path('code/checking/', CodeCheckingView.as_view(), name='seller-reset_password'), # менять пароль в профиле

    # path('    path('send-code-to-email/', SellerSendCodeView.as_view(), name='send_password_reset_code'), # отправить code в почту

    path('code/checking/',CodeCheckingView.as_view(), name='reset_password'), # забыл пароль при входеreset-password-profile/', UserResetPasswordView.as_view(), name='reset_password'), # менять пароль в профиле


#     path('profiles/', ListProfileApi.as_view(), name=''),
#     path('profile/<int:id>/', DetailUserProfileApi.as_view(), name=''),
#     path('profile/update/<int:id>/', UpdateUserProfileApi.as_view(), name=''),


    path('register/',SellerRegisterView.as_view(), name='seller-register'),
    path('login/', SellerLoginView.as_view(), name='seller-login'), # логин
    path('verify-register-code/', SellerVerifyRegisterCode.as_view(), name='seller-verify_register_code'), # подтвердить почту

    path('become/seller/', BecomeSellerView.as_view(), name='seller-become_seller'),
    path('seller/profiles/detail/<int:pk>/',SellerDetailApiview.as_view(),name='seller-profile-detail'),
    path('seller-profiles/',SellerListApiview.as_view()),
#     path('seller-profile/<int:id>/', DetailUserProfileApi.as_view(), name=''),
    path('seller/profile/update/<int:pk>/', SellerUpdateProfileShopApi.as_view(), name='seller-profile-update'),

    path('logout/seller/', LogoutView.as_view(), name='seller-logout'),

    path('change/password/seller/', ChangePasswordAPIVIew.as_view(),name='seller-change-password'),

#     path('market/', MarketListAPIView.as_view(), name=''),
#     path('logout/', LogoutView.as_view(), name='logout'),
    
]