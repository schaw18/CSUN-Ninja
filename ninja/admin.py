from django.contrib import admin
from .models import *

admin.site.register(Section)
admin.site.register(SectionSchedule)
admin.site.register(Course)
admin.site.register(CoursesTaken)
admin.site.register(FAQ)
admin.site.register(Major)
admin.site.register(MajorCourse)
admin.site.register(DPRfile)

