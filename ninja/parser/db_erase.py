from ..models import *
def erase():
    c=Course.objects.all()
    s=Section.objects.all()
    sh=SectionSchedule.objects.all()

    c.delete()
    s.delete()
    sh.delete()
    print('all deleted')
