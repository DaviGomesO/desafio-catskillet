from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    icon = models.CharField(max_length=100, verbose_name='Ícone')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        ordering = ['name']
        verbose_name = 'Categoria'

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS = [('P', 'Pendente'),
              ('C', 'Concluída'),
              ('A', 'Em andamento')]
    title = models.CharField(max_length=100, verbose_name='Título')
    description = models.TextField(blank=True, verbose_name='Descrição')
    execution_date = models.DateField(verbose_name='Data de execução')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    status = models.CharField(max_length=1, choices=STATUS, default='P', verbose_name='Status')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Dono da tarefa', related_name='tarefas')
    categories = models.ManyToManyField(Category, verbose_name='Categorias')

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return self.title
