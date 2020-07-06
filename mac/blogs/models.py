from django.db import models

# Create your models here.
class Blog(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=70,default="")
    head0 = models.CharField(max_length=70,default="")
    chead0 = models.CharField(max_length=700,default="")
    head1 = models.CharField(max_length=70,default="")
    chead1 = models.CharField(max_length=700,default="")
    head2 = models.CharField(max_length=70,default="")
    chead2 = models.CharField(max_length=700,default="")
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to='blogs/images',default="")


    def __str__(self):
        return self.title
