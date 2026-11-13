
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_game_completion_date_game_developer_game_platform_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='decksup',
            field=models.BooleanField(default=False, verbose_name='Wsparcie na SteamOS'),
        ),
        migrations.AddField(
            model_name='game',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6, verbose_name='Cena'),
        ),
        migrations.AlterField(
            model_name='game',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Ocena (1-10)'),
        ),
    ]
