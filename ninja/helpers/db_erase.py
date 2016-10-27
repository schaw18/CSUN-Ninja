from ninja.models import *
def erase():
    c=Course.objects.all()
    u=User.objects.all()
    s=Section.objects.all()
    sh=SectionSchedule.objects.all()

    u.delete()
    c.delete()
    s.delete()
    sh.delete()
    print('all deleted')
