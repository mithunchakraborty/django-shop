import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from .models import Order, OrderItem


def export_to_csv(modeladmin, request, queryset):
    """
    Uploading the order list as a CSV file.
    """
    opts = modeladmin.model._meta
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        f'attachment; filename={opts.verbose_name}.csv'

    writer = csv.writer(response)
    fields = [
        f for f in opts.get_fields() \
        if not f.many_to_many and not f.one_to_many
    ]

    # Write a first row with header information
    writer.writerow([
        field.verbose_name for field in fields
    ])

    # Write data rows
    for obj in queryset:
        data_row = []
        
        for field in fields:
            value = getattr(obj, field.name)

            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')

            data_row.append(value)

        writer.writerow(data_row)

    return response


export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    """

    """
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    """

    """
    list_display = [
        'id', 'first_name', 'last_name',
        'email', 'address', 'postal_code',
        'city', 'paid', 'created', 'updated'
    ]
    list_filter = [
        'paid', 'created', 'updated'
    ]
    lnlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)

