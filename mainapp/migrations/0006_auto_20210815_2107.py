# Generated by Django 3.2.6 on 2021-08-15 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20210814_1646'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.CreateModel(
            name='TV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='mainapp/images', verbose_name='Изображение товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('slug', models.SlugField(unique=True)),
                ('type', models.CharField(max_length=255, verbose_name='Тип')),
                ('diagonal', models.CharField(max_length=255, verbose_name='Диагональ экрана')),
                ('resolution', models.CharField(max_length=255, verbose_name='Разрешение')),
                ('matrix_type', models.CharField(max_length=255, verbose_name='Тип матрицы')),
                ('matrix_frequency', models.CharField(max_length=255, verbose_name='Частота матрицы')),
                ('image_quality_index', models.CharField(max_length=255, verbose_name='Индекс качества изображения')),
                ('smart_tv', models.BooleanField(default=False, verbose_name='Smart TV')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Телевизор',
                'verbose_name_plural': 'Телевизоры',
            },
        ),
        migrations.CreateModel(
            name='Tablet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='mainapp/images', verbose_name='Изображение товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('slug', models.SlugField(unique=True)),
                ('diagonal', models.CharField(max_length=255, verbose_name='Диагональ экрана')),
                ('resolution', models.CharField(max_length=255, verbose_name='Разрешение экрана')),
                ('display_type', models.CharField(max_length=255, verbose_name='Матрица экрана')),
                ('ram', models.CharField(max_length=255, verbose_name='Оперативная память')),
                ('sd', models.BooleanField(default=True, verbose_name='Наличие слота для SD карты')),
                ('sd_volume_max', models.CharField(blank=True, max_length=255, null=True, verbose_name='Максимальный объём SD карты')),
                ('main_cam_mp', models.CharField(max_length=255, verbose_name='Главная камера')),
                ('front_cam_mp', models.CharField(max_length=255, verbose_name='Фронтальная камера')),
                ('accum_volume', models.CharField(max_length=255, verbose_name='Объём батареи')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Планшет',
                'verbose_name_plural': 'Планшеты',
            },
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='mainapp/images', verbose_name='Изображение товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('slug', models.SlugField(unique=True)),
                ('diagonal', models.CharField(max_length=255, verbose_name='Диагональ')),
                ('aspect_ratio', models.CharField(max_length=255, verbose_name='Соотношение сторон')),
                ('resolution', models.CharField(max_length=255, verbose_name='Разрешение')),
                ('matrix', models.CharField(max_length=255, verbose_name='Матрица')),
                ('screen_refresh_rate', models.CharField(max_length=255, verbose_name='Частота обновления экрана')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Монитор',
                'verbose_name_plural': 'Мониторы',
            },
        ),
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='mainapp/images', verbose_name='Изображение товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('slug', models.SlugField(unique=True)),
                ('processor_model', models.CharField(max_length=255, verbose_name='Процессор')),
                ('number_of_cores', models.CharField(max_length=255, verbose_name='Количество ядер')),
                ('processor_freq', models.CharField(max_length=255, verbose_name='Тактовая частота процессора')),
                ('ram_type', models.CharField(max_length=255, verbose_name='Тип оперативной памяти')),
                ('ram_frequency', models.CharField(max_length=255, verbose_name='Частота оперативной памяти')),
                ('ram_size', models.CharField(max_length=255, verbose_name='Объём оперативной памяти')),
                ('storage_type', models.CharField(max_length=255, verbose_name='Тип накопителя')),
                ('storage_capacity', models.CharField(max_length=255, verbose_name='Тип накопителя')),
                ('video', models.CharField(max_length=255, verbose_name='Видеокарта')),
                ('local_video_memory', models.CharField(max_length=255, verbose_name='Локальная видеопамять')),
                ('power_supply', models.CharField(max_length=255, verbose_name='Блок питания')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Компьютер',
                'verbose_name_plural': 'Компьютеры',
            },
        ),
    ]