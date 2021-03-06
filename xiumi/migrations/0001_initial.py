# Generated by Django 2.1.5 on 2020-01-14 15:19

from django.db import migrations, models
import django.db.models.deletion
import xiumi.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(blank=True, max_length=50, null=True)),
                ('expires_in', models.IntegerField(blank=True, help_text='access_token有效的时间，单位是秒', null=True)),
                ('code', models.IntegerField(default=0, help_text='为一个非0的整数值，表示发生了错误，具体值的含义没有约定。')),
                ('msg', models.TextField(blank=True, help_text='用来说明错误原因，可能在页面上显示给用户', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PartnerUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(help_text='正整数，小于2的32次方。用户在合作方应用的唯一标识。 由合作方应用提供，秀米将使用其作为用户在秀米的身份标识。')),
                ('route_type', models.CharField(default='article', help_text='登录后使用的功能，当前固定为article，表示“图文编辑器”', max_length=10)),
                ('timestamp', models.IntegerField(help_text='当前UNIX时间戳，单位：秒。')),
                ('appid', models.CharField(help_text='合作方应用在秀米平台的唯一标识，由秀米提前颁发，形式为一个32个字符的字符串。', max_length=50)),
                ('nonce', models.CharField(help_text='随机字符串，由合作方应用在每一次签名时生成，使用于签名算法内。', max_length=10)),
                ('signature', models.CharField(help_text='每次登录时根据各项参数计算得出的签名字符串。算法见下面的说明.', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SomeArticles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_id', models.IntegerField(blank=True, help_text='是该图文在秀米的唯一编号', null=True)),
                ('author', models.CharField(blank=True, max_length=200, null=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, help_text='是一个HTML格式的字符串，包含图文内容。', null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=xiumi.models.SomeArticles.get_upload_to)),
                ('picurl', models.URLField(blank=True, null=True)),
                ('showCover', models.IntegerField(blank=True, null=True)),
                ('summary', models.CharField(blank=True, max_length=200, null=True)),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SomePathForArticles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(default=0, help_text='code指示图文是否被正常接收，0表示正常，其他值为异常。')),
                ('msg', models.TextField(blank=True, help_text='msg是说明文本，提供相关的说明', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SomePathForImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(default=0, help_text='为一个非0的整数值，表示发生了错误，具体值的含义没有约定。')),
                ('msg', models.TextField(blank=True, help_text='用来说明错误原因，可能在页面上显示给用户', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SomePathForImageData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='图片在合作方的URL')),
                ('name', models.TextField(blank=True, help_text='图片的名称，在html中可能作为alt显示', null=True)),
                ('some_path_for_image_key', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data', to='xiumi.SomePathForImage')),
            ],
        ),
        migrations.AddField(
            model_name='somearticles',
            name='articles_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='xiumi.SomePathForArticles'),
        ),
    ]
