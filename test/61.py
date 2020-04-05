from django.contrib import admin
from models import Person
class PersonAdmin(admin.ModelAdmin):
    def old_person_column(self):
        if self.age >30:
            column ='<span style="background:#0B6121;" >'\
                    '<a href ="/person/detail/%s">%s</a></span>'%(
                        self.pk , self.name)
        else:
            column = '<span style="background:#DF0101;" >'\
                     '<a href ="/person/detail_old/%s">%s</a></span>'%(
                         self.pk , self.name)
        return column.lower()
    
    old_person_column.short_description ='Person'
    old_person_column.allow_tags        =True

    def africa_contry(self):
        if self.country in ('SENEGAL' , 'MALI', 'MAURITANIE'):
            column = '<a href ="/person/detail_contry/%s">%s</a></span>'%(
                        self.pk , self.country)
        else:
            column = '<a href ="/person/detail_contry/%s">%s</a></span>'%(
                        self.pk , self.country)
        return column.lower()
            
    africa_contry.short_description ='Africa'
    africa_contry.allow_tags         =True


    def name_column(self):
        return self.name.lower()

    def country_column(self):
        return self.country.lower()
        
    list_display = ('pk' , name_column , country_column ,
                    old_person_column ,
                    africa_contry )
    fields = ['name']
    
    class Meta:
        css = {
              'all': (
            'css/person.css',)

        }
        js = (
        'js/person.js',
        
    )
admin.site.register(Person, PersonAdmin)
      
