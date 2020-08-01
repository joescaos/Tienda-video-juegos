from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid

categoria = (
    ('Juegos de accion', 'Juegos de accion'),
    ('Juegos de simulacion', 'Juegos de simulacion'),
    ('Juegos de deportes', 'Juegos de deportes'),
    ('Juegos de aventura', 'Juegos de aventura'),
    ('Juegos de plataformas', 'Juegos de plataformas'),
    ('Juegos de puzzle', 'Juegos de puzzle'),
)
class Game(models.Model):
    nombre = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='games/', null=True)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    categoria = models.CharField(choices=categoria, max_length=80, null=True)
    existencia = models.PositiveIntegerField(null=True)
    slug = models.SlugField(null=False, blank=False, unique=True)

    '''def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Game, self).save(*args, **kwargs)'''
 
    def __str__(self):
        return self.nombre

def set_slug(sender, instance, *args, **kwargs):
    if instance.nombre and not instance.slug:
        slug = slugify(instance.nombre)
        
        while Game.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.nombre, str(uuid.uuid4())[:8])
            )
    instance.slug = slugify(instance.nombre)

pre_save.connect(set_slug, sender=Game)