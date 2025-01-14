# Generated by Django 2.2.5 on 2020-01-10 07:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dockerapi', '0017_auto_20191220_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysLog',
            fields=[
                ('log_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='使用用户ID')),
                ('operation_type', models.CharField(max_length=255, verbose_name='操作类型')),
                ('operation_name', models.CharField(max_length=255, verbose_name='操作名称')),
                ('operation_value', models.CharField(max_length=255, verbose_name='操作内容')),
                ('operation_args', models.TextField(default='', null=True, verbose_name='参数')),
                ('ip', models.CharField(max_length=255, verbose_name='IP地址')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'sys_log',
            },
        ),
        migrations.AlterField(
            model_name='timemoudel',
            name='time_id',
            field=models.CharField(default='eb0fa616-f5f6-4f6d-8864-1fd37d126ec6', max_length=255, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
