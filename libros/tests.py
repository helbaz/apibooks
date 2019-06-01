from django.test import TestCase
from .models import *


class AnimalTestCase(TestCase):
    def setUp(self):
        Libros.objects.create(titulo="test unitari", descripcion="aquest es un test unitari", autor_id=3)

    def test_ruta_imagen(self):
        libro = Libros.objects.get(titulo="test unitari")
        self.assertEqual(libro.imagen_perfil, 'static/default_book.png')
