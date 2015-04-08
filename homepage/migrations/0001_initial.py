# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='username', unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(verbose_name='first name', blank=True, max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='email address', blank=True, max_length=75)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('phone', models.TextField(null=True, blank=True, max_length=40)),
                ('security_question', models.TextField(null=True, blank=True, max_length=200)),
                ('security_answer', models.TextField(null=True, blank=True, max_length=200)),
                ('requires_reset', models.BooleanField(default=False)),
                ('organization_name', models.TextField(null=True, blank=True, max_length=200)),
                ('organization_type', models.TextField(null=True, blank=True, max_length=40)),
                ('date_appointed_agent', models.DateField(null=True, blank=True)),
                ('relationship', models.TextField(null=True, blank=True, max_length=200)),
                ('emergency_contact', models.TextField(null=True, blank=True, max_length=200)),
                ('emergency_phone', models.TextField(null=True, blank=True, max_length=200)),
                ('emergency_relationship', models.TextField(null=True, blank=True, max_length=200)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('street1', models.TextField(max_length=200)),
                ('street2', models.TextField(null=True, blank=True, max_length=200)),
                ('city', models.TextField(max_length=100)),
                ('state', models.TextField(max_length=20)),
                ('zip_code', models.TextField(max_length=20)),
                ('country', models.TextField(max_length=100)),
            ],
            options={
                'ordering': ['state', 'city', 'zip_code', 'street1', 'street2'],
                'verbose_name_plural': 'addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200)),
                ('description', models.TextField(max_length=1000)),
                ('place_number', models.PositiveIntegerField()),
                ('coordinator', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='coordinates')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CartLineItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConfigurationParameters',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('sales_tax_rate', models.DecimalField(max_digits=5, decimal_places=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DamageFee',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('waived', models.BooleanField(default=False)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200)),
                ('description', models.TextField(max_length=1000)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('map_file_name', models.TextField(max_length=200)),
                ('venue_name', models.TextField(null=True, max_length=200)),
                ('address', models.ForeignKey(to='homepage.Address', null=True, related_name='+')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LateFee',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('waived', models.BooleanField(default=False)),
                ('days_late', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField()),
                ('phone', models.TextField()),
                ('date_packed', models.DateTimeField()),
                ('date_paid', models.DateTimeField(null=True)),
                ('date_shipped', models.DateTimeField(null=True)),
                ('tracking_number', models.TextField(null=True, max_length=50)),
                ('customer', models.ForeignKey(related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('handled_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='handledby_set')),
                ('packed_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='packedby_set')),
                ('payment_processed_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='paymentprocessedby_set')),
                ('shipped_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='shippedby_set')),
                ('ships_to', models.ForeignKey(related_name='+', to='homepage.Address')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipantRole',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200)),
                ('type', models.TextField(max_length=40)),
                ('area', models.ForeignKey(to='homepage.Area')),
                ('participant', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photograph',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('date_taken', models.DateTimeField()),
                ('place_taken', models.TextField(null=True, blank=True, max_length=200)),
                ('description', models.TextField(null=True, blank=True, max_length=1000)),
                ('image', models.TextField(null=True, blank=True, max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('description', models.TextField()),
                ('manufacturer', models.TextField(max_length=80)),
                ('average_cost', models.DecimalField(max_digits=10, decimal_places=2)),
                ('sku', models.TextField(max_length=20)),
                ('order_form_name', models.TextField(null=True, max_length=200)),
                ('production_time', models.TextField(null=True, max_length=200)),
                ('category', models.ForeignKey(related_name='+', to='homepage.Category')),
                ('photo', models.OneToOneField(to='homepage.Photograph', null=True)),
                ('vendor', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RentalItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('date_out', models.DateTimeField(auto_now_add=True)),
                ('date_in', models.DateTimeField(null=True)),
                ('date_due', models.DateTimeField()),
                ('discount_percent', models.DecimalField(max_digits=3, decimal_places=2)),
                ('order', models.ForeignKey(to='homepage.Order')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(to='homepage.Order')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StockedProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('quantity_on_hand', models.IntegerField()),
                ('shelf_location', models.TextField(max_length=40)),
                ('order_file', models.TextField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SerializedProduct',
            fields=[
                ('stockedproduct_ptr', models.OneToOneField(primary_key=True, auto_created=True, to='homepage.StockedProduct', serialize=False, parent_link=True)),
                ('serial_number', models.TextField(null=True, unique=True, max_length=100)),
                ('type', models.TextField(max_length=100)),
                ('date_acquired', models.DateField(auto_now_add=True)),
                ('cost', models.DecimalField(max_digits=10, decimal_places=2)),
                ('for_sale', models.BooleanField(default=True)),
                ('condition_new', models.BooleanField(default=True)),
                ('notes', models.TextField()),
                ('size', models.TextField(null=True, max_length=40)),
                ('size_modifier', models.TextField(null=True, max_length=40)),
                ('gender', models.TextField(null=True, max_length=40)),
                ('color', models.TextField(null=True, max_length=40)),
                ('pattern', models.TextField(null=True, max_length=40)),
                ('start_year', models.PositiveIntegerField(null=True)),
                ('end_year', models.PositiveIntegerField(null=True)),
                ('note', models.TextField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('homepage.stockedproduct',),
        ),
        migrations.CreateModel(
            name='RentalProduct',
            fields=[
                ('serializedproduct_ptr', models.OneToOneField(primary_key=True, auto_created=True, to='homepage.SerializedProduct', serialize=False, parent_link=True)),
                ('times_rented', models.IntegerField()),
                ('price_per_day', models.DecimalField(max_digits=10, decimal_places=2)),
                ('replacement_price', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
            options={
                'abstract': False,
            },
            bases=('homepage.serializedproduct',),
        ),
        migrations.AddField(
            model_name='stockedproduct',
            name='photo',
            field=models.ForeignKey(null=True, to='homepage.Photograph'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stockedproduct',
            name='polymorphic_ctype',
            field=models.ForeignKey(to='contenttypes.ContentType', related_name='polymorphic_homepage.stockedproduct_set', null=True, editable=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stockedproduct',
            name='product_specification',
            field=models.ForeignKey(related_name='+', to='homepage.ProductSpecification'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='serializedproduct',
            name='owner',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='saleitem',
            name='product',
            field=models.ForeignKey(related_name='+', to='homepage.StockedProduct'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rentalitem',
            name='rental_product',
            field=models.ForeignKey(related_name='+', to='homepage.RentalProduct'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='latefee',
            name='order',
            field=models.ForeignKey(to='homepage.Order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='latefee',
            name='rental_item',
            field=models.ForeignKey(related_name='+', to='homepage.RentalItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='damagefee',
            name='order',
            field=models.ForeignKey(to='homepage.Order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='damagefee',
            name='rental_item',
            field=models.ForeignKey(related_name='+', to='homepage.RentalItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cartlineitem',
            name='stocked_product',
            field=models.ForeignKey(to='homepage.StockedProduct'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cartlineitem',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='event',
            field=models.ForeignKey(to='homepage.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='participants',
            field=models.ManyToManyField(null=True, through='homepage.ParticipantRole', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='photo',
            field=models.ForeignKey(null=True, to='homepage.Photograph'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='area',
            name='supervisor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='supervises'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.ForeignKey(blank=True, to='homepage.Address', null=True, related_name='+'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(verbose_name='groups', blank=True, related_query_name='user', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ForeignKey(blank=True, to='homepage.Photograph', null=True, related_name='+'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(verbose_name='user permissions', blank=True, related_query_name='user', to='auth.Permission', help_text='Specific permissions for this user.', related_name='user_set'),
            preserve_default=True,
        ),
    ]
