# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Administrator(models.Model):
    auser = models.OneToOneField('Dbuser', models.DO_NOTHING, db_column='Auser_ID', primary_key=True)  # Field name made lowercase.
    admin_name = models.CharField(db_column='Admin_Name', max_length=100)  # Field name made lowercase.
    admin_email = models.CharField(db_column='Admin_Email', max_length=100)  # Field name made lowercase.
    admin_phone = models.BigIntegerField(db_column='Admin_Phone')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ADMINISTRATOR'


class Application(models.Model):
    application_id = models.IntegerField(db_column='Application_ID', primary_key=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=100)  # Field name made lowercase.
    user_number = models.IntegerField(db_column='User_Number')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'APPLICATION'


class Assigns(models.Model):
    spon = models.OneToOneField('Sponsor', models.DO_NOTHING, db_column='Spon_ID', primary_key=True)  # Field name made lowercase.
    driv = models.ForeignKey('Driver', models.DO_NOTHING, db_column='Driv_ID')  # Field name made lowercase.
    ad = models.ForeignKey(Administrator, models.DO_NOTHING, db_column='AD_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ASSIGNS'
        unique_together = (('spon', 'driv', 'ad'),)


class Awarded(models.Model):
    point_total = models.IntegerField(db_column='Point_Total')  # Field name made lowercase.
    date_added = models.CharField(db_column='Date_Added', max_length=100)  # Field name made lowercase.
    suser = models.OneToOneField('Sponsor', models.DO_NOTHING, db_column='Suser_ID', primary_key=True)  # Field name made lowercase.
    duser = models.ForeignKey('Driver', models.DO_NOTHING, db_column='id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AWARDED'
        unique_together = (('suser', 'duser'),)


class Catalog(models.Model):
    catalog_name = models.CharField(db_column='Catalog_Name', primary_key=True, max_length=100)  # Field name made lowercase.
    #spon = models.ForeignKey('Sponsor', models.DO_NOTHING, db_column='Spon_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CATALOG'


class Categories(models.Model):
    category_name = models.CharField(db_column='Category_Name', primary_key=True, max_length=100)  # Field name made lowercase.
    cat_name = models.ForeignKey(Catalog, models.DO_NOTHING, db_column='Cat_Name')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CATEGORIES'
   # class Meta: verbose_name_plural = 'Categories'


class Contains(models.Model):
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    prod = models.OneToOneField('Products', models.DO_NOTHING, db_column='Prod_ID', primary_key=True)  # Field name made lowercase.
    purchase = models.ForeignKey('Purchase', models.DO_NOTHING, db_column='Purchase_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CONTAINS'
        unique_together = (('prod', 'purchase'),)


class Creates(models.Model):
    p = models.OneToOneField('Purchase', models.DO_NOTHING, db_column='P_ID', primary_key=True)  # Field name made lowercase.
    d = models.ForeignKey('Driver', models.DO_NOTHING, db_column='D_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CREATES'
        unique_together = (('p', 'd'),)


class Dbuser(models.Model):
    dbuser_id = models.IntegerField(db_column='DBuser_ID', primary_key=True)  # Field name made lowercase.
    user_password = models.CharField(db_column='User_Password', max_length=100)  # Field name made lowercase.
    created_date = models.CharField(db_column='Created_Date', max_length=100)  # Field name made lowercase.
    updated_date = models.CharField(db_column='Updated_Date', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DBUSER'


class Driver(models.Model):
    id = models.OneToOneField(Dbuser, models.DO_NOTHING, db_column='id', primary_key=True)  # Field name made lowercase.
    driver_name = models.CharField(db_column='Driver_Name', max_length=100)  # Field name made lowercase.
    employee_number = models.IntegerField(db_column='Employee_Number')  # Field name made lowercase.
    driver_address = models.CharField(db_column='Driver_Address', max_length=100)  # Field name made lowercase.
    driver_points = models.FloatField(db_column='Driver_Points')  # Field name made lowercase.
    driver_rate = models.FloatField(db_column='Driver_Rate')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DRIVER'
    
    def __str__(self):
        return f"{self.driver_name}"


class Employs(models.Model):
    employs_id = models.AutoField(db_column='Employs_ID', primary_key=True)  # Field name made lowercase.
    sponsors = models.ForeignKey('Sponsor', models.DO_NOTHING, db_column='Sponsors_ID')  # Field name made lowercase.
    drivers = models.ForeignKey(Driver, models.DO_NOTHING, db_column='Drivers_ID')  # Field name made lowercase.
    driver_points = models.FloatField(db_column='Driver_Points') # Field name made lowercase

    class Meta:
        managed = True
        db_table = 'EMPLOYS'
#    class Meta: verbose_name_plural = 'Employs'
    def __str__(self):
        return f"{self.employs_id}, {self.sponsors}, {self.drivers}"

class Goodbehaviorapp(models.Model):
    app_name = models.CharField(db_column='App_Name', primary_key=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GOODBEHAVIORAPP'


class Oldadmin(models.Model):
    auser = models.OneToOneField(Dbuser, models.DO_NOTHING, db_column='Auser_ID', primary_key=True)  # Field name made lowercase.
    admin_name = models.CharField(db_column='Admin_Name', max_length=100)  # Field name made lowercase.
    admin_email = models.CharField(db_column='Admin_Email', max_length=100)  # Field name made lowercase.
    admin_phone = models.BigIntegerField(db_column='Admin_Phone')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OLDADMIN'


class Oldprices(models.Model):
    product_name = models.CharField(db_column='Product_Name', primary_key=True, max_length=100)  # Field name made lowercase.
    price_total = models.FloatField(db_column='Price_Total')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OLDPRICES'


class Oldstatus(models.Model):
    product_name = models.CharField(db_column='Product_Name', primary_key=True, max_length=100)  # Field name made lowercase.
    availability = models.CharField(db_column='Availability', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OLDSTATUS'


class Operation(models.Model):
    operation_id = models.CharField(db_column='Operation_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OPERATION'


class Owns(models.Model):
    prod = models.ForeignKey('Products', models.DO_NOTHING, db_column='Prod_ID')  # Field name made lowercase.
    sponsor = models.OneToOneField('Sponsor', models.DO_NOTHING, db_column='Sponsor_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OWNS'
        unique_together = (('sponsor', 'prod'),)


class Products(models.Model):
    product_name = models.CharField(db_column='Product_Name', max_length=100)  # Field name made lowercase.
    price_total = models.FloatField(db_column='Price_Total')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100)  # Field name made lowercase.
    availability = models.CharField(db_column='Availability', max_length=100)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=100)  # Field name made lowercase.
    point_value = models.IntegerField(db_column='Point_Value')  # Field name made lowercase.
    cate_name = models.ForeignKey(Categories, models.DO_NOTHING, db_column='Cate_Name')  # Field name made lowercase.
    product_id = models.IntegerField(db_column='Product_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PRODUCTS'
   # class Meta: verbose_name_plural = 'Products'


class Purchase(models.Model):
    purchase_id = models.IntegerField(db_column='Purchase_ID', primary_key=True)  # Field name made lowercase.
    purchase_total = models.FloatField(db_column='Purchase_Total')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=100)  # Field name made lowercase.
    created_date = models.CharField(db_column='Created_Date', max_length=100)  # Field name made lowercase.
    updated_date = models.CharField(db_column='Updated_Date', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PURCHASE'


class Qualifiesfor(models.Model):
    r = models.OneToOneField('Selectrules', models.DO_NOTHING, db_column='R_ID', primary_key=True)  # Field name made lowercase.
    prod = models.ForeignKey(Products, models.DO_NOTHING, db_column='Prod_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QUALIFIESFOR'
        unique_together = (('r', 'prod'),)


class Reviews(models.Model):
    s = models.OneToOneField('Sponsor', models.DO_NOTHING, db_column='S_ID', primary_key=True)  # Field name made lowercase.
    app = models.ForeignKey(Application, models.DO_NOTHING, db_column='App_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REVIEWS'
        unique_together = (('s', 'app'),)


class Securedfor(models.Model):
    users_type = models.OneToOneField('Usertype', models.DO_NOTHING, db_column='Users_Type', primary_key=True)  # Field name made lowercase.
    op = models.ForeignKey(Operation, models.DO_NOTHING, db_column='OP_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SECUREDFOR'
        unique_together = (('users_type', 'op'),)


class Selectrules(models.Model):
    rule_id = models.IntegerField(db_column='Rule_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SELECTRULES'


class Sponsor(models.Model):
    id = models.OneToOneField(Dbuser, models.DO_NOTHING, db_column='id', primary_key=True)  # Field name made lowercase.
    company_name = models.CharField(db_column='Company_Name', max_length=100)  # Field name made lowercase.
    comp_address = models.CharField(db_column='Comp_Address', max_length=100)  # Field name made lowercase.
    point_value = models.FloatField(db_column='Point_Value')  # Field name made lowercase.
    payment_method = models.CharField(db_column='Payment_Method', max_length=100)  # Field name made lowercase.
    payment_numb = models.IntegerField(db_column='Payment_Numb')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SPONSOR'

    def __str__(self):
        return f"{self.company_name}"


class Switches(models.Model):
    sponsors = models.OneToOneField(Sponsor, models.DO_NOTHING, db_column='Sponsors_ID', primary_key=True)  # Field name made lowercase.
    drivers = models.ForeignKey(Driver, models.DO_NOTHING, db_column='Drivers_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SWITCHES'
        unique_together = (('sponsors', 'drivers'),)


class Usertype(models.Model):
    users_type = models.CharField(db_column='Users_Type', primary_key=True, max_length=100)  # Field name made lowercase.
    tuser = models.ForeignKey(Dbuser, models.DO_NOTHING, db_column='Tuser_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USERTYPE'
        unique_together = (('users_type', 'tuser'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CatalogCatalog(models.Model):
    name = models.CharField(max_length=200)
    isprimary = models.IntegerField(db_column='isPrimary')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'catalog_catalog'


class CatalogCategory(models.Model):
    name = models.CharField(max_length=200)
    catalog = models.ForeignKey(CatalogCatalog, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'catalog_category'


class CatalogProduct(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=20)
    productimg = models.CharField(db_column='productImg', max_length=500)  # Field name made lowercase.
    productid = models.CharField(max_length=100)
    rating = models.CharField(max_length=50)
    link = models.CharField(max_length=500)
    category = models.ForeignKey(CatalogCategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'catalog_product'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

