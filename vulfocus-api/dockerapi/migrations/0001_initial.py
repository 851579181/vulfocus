# Generated by Django 2.2.5 on 2019-10-29 04:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageInfo',
            fields=[
                ('image_id', models.UUIDField(default='66b8a169-eb66-45e5-adc2-a50dc2d3b33a', primary_key=True, serialize=False)),
                ('image_name', models.CharField(max_length=256, unique=True, verbose_name='Docker镜像名称')),
                ('image_vul_name', models.CharField(max_length=256, verbose_name='漏洞名称')),
                ('image_port', models.CharField(max_length=256, verbose_name='暴露端口')),
                ('image_desc', models.TextField(null=True, verbose_name='镜像描述')),
                ('rank', models.FloatField(verbose_name='Rank')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Docker创建时间，默认为当前时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Docker更新时间，默认为当前时间')),
            ],
            options={
                'db_table': 'image_info',
            },
        ),
        migrations.CreateModel(
            name='TimeMoudel',
            fields=[
                ('time_id', models.CharField(default='ac7258ed-b864-4349-b875-9619069c1b00', max_length=255, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='用户ID')),
                ('start_time', models.FloatField(verbose_name='开始时间戳')),
                ('end_time', models.FloatField(verbose_name='结束时间')),
            ],
            options={
                'db_table': 'time_moudel',
            },
        ),
        migrations.CreateModel(
            name='ContainerVul',
            fields=[
                ('container_id', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False, verbose_name='漏洞容器创建ID')),
                ('docker_container_id', models.CharField(max_length=255, verbose_name='Docker容器运行进ID')),
                ('user_id', models.IntegerField(verbose_name='用户ID')),
                ('vul_host', models.CharField(max_length=255, verbose_name='容器漏洞URL')),
                ('container_status', models.CharField(max_length=255, verbose_name='容器当前状态')),
                ('container_port', models.CharField(max_length=255, verbose_name='容器端口')),
                ('container_flag', models.CharField(max_length=255, verbose_name='flag')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='容器创建时间，默认为当前时间')),
                ('is_check', models.BooleanField(default=False, verbose_name='Flag是否通过')),
                ('is_check_date', models.DateTimeField(null=True, verbose_name='Flag提交时间')),
                ('time_model_id', models.CharField(default='', max_length=255, verbose_name='时间模式 ID')),
                ('image_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dockerapi.ImageInfo', verbose_name='Docker ID')),
            ],
            options={
                'db_table': 'container_vul',
            },
        ),
    ]
