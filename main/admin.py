from django.contrib import admin

from main.models import Product, ProductImage, Plan, PlanItem, Subscription

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Plan)
admin.site.register(PlanItem)
admin.site.register(Subscription)
