from django.db import models
class Person(models.Model):
      
      name = models.CharField(max_length =20)
      age  = models.IntegerField(default =0)
      country  = models.CharField(max_length = 200)

      def __unicode__(self):
          return u'<Person  |name :%s | Age :%s>' %(self.name, self.age)
