from django.db import models
from ApiManager.models import BaseModel
from encrypted_fields.fields import EncryptedTextField
import re
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

# Create your models here.
def is_color_valid(value):
    if not re.match(r'^#[A-Fa-f0-9]{6}', value):
        raise ValueError(f"{value} is not a valid hex color code.")
    return value



class Server(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    hostname = models.CharField(max_length=100, blank=True, null=True)
    port = models.PositiveIntegerField(default=4589, validators=[MinValueValidator(1), MaxValueValidator(65535)])
    username = models.CharField(max_length=50)
    password = EncryptedTextField(max_length=100, blank=True, null=True)
    ssh_key = EncryptedTextField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='servers', blank=True)

    auth_type = models.CharField(
        max_length=20,
        choices=[
            ('password', 'Password'),
            ('key', 'SSH Key'),
        ],
        default='password'
    )

    def __str__(self):
        return self.name

class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, validators=[RegexValidator(regex=r'^#[A-Fa-f0-9]{6}')], default='#FFFFFF')

    def __str__(self):
        return self.name