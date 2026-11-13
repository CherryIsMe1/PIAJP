
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='completion_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data ukończenia'),
        ),
        migrations.AddField(
            model_name='game',
            name='developer',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Studio / wydawca'),
        ),
        migrations.AddField(
            model_name='game',
            name='platform',
            field=models.CharField(choices=[('PC', 'PC'), ('PS', 'PlayStation'), ('XBOX', 'Xbox'), ('NINTENDO', 'Nintendo'), ('MOBILE', 'Mobile')], default='PC', max_length=20, verbose_name='Platforma'),
        ),
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('OWNED', 'W kolekcji'), ('WISHLIST', 'Lista życzeń'), ('COMPLETED', 'Ukończona'), ('ABANDONED', 'Porzucona')], default='OWNED', max_length=20, verbose_name='Status kolekcji'),
        ),
        migrations.AddConstraint(
            model_name='game',
            constraint=models.UniqueConstraint(fields=('title', 'platform'), name='unique_game_title_platform'),
        ),
    ]
