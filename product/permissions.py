from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers
from app_userseller.models import SellerProfile
from app_user.models import User

class IsAnonymoused(BasePermission):
    """
        Allows access only to not authenticated users.
    """

    message = 'permission denied, at first you must logout'

    def has_permission(self, request, view):
        return bool(request.user.is_anonymous)


class IsSellerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        print(request.user)
        if request.user.is_authenticated:
            try:
                seller_profile = SellerProfile.objects.get(
                    email_or_phone=request.user)
                user = User.objects.get(email_or_phone=request.user)
                if seller_profile.is_seller:
                    return True
                try:
                    if user.is_seller:
                        raise PermissionDenied("No permission")
                except User.DoesNotExist:
                    raise serializers.ValidationError("permission error")

                
            except SellerProfile.DoesNotExist:
                raise PermissionDenied(f"Seller account does not exist for account:{str(request.user)}")
            except User.DoesNotExist:
                raise PermissionDenied({"permissions":"no permission"})
            raise PermissionDenied({"permissions":"Permission denied for user."})
        raise PermissionDenied({"permissions":"Only admin or seller users can create product."})

    def has_object_permission(self, request, view, obj):
        return (obj.user.is_seller)


    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user
    # def has_object_permission(self, request, view, obj):
    #     return (obj.user.is_seller)
    
class IsSellerAndHasStore(BasePermission):
    """
        Allow access only user that is seller and have store
    """

    message = "permission denied, you are not seller user or don't have store"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        has_store = True
        try:
            obj.store
        except:
            has_store = False
        return bool(obj.is_seller and has_store)


class IsSellerOfProduct(BasePermission):
    """
        Allow access only user that seller of product
    """

    message = 'permission denied, you are not seller of this product'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        return bool(obj.seller.founder == request.user and request.user.is_seller)