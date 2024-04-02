from django.db import models

# Create your models here.

class Basemodel (models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated+at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    class College(BaseModel):
        college_name = models.CharField(max_length=150)

        def__str__(self):
            return self.college_name
    
    class Program(BaseModel):
        prog_name = models.CharField
