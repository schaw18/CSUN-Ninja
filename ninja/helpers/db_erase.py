from ninja.models import *
def erase():
    c=Course.objects.all()
    u=User.objects.all()
    s=Section.objects.all()
    sh=SectionSchedule.objects.all()
    cr=CoursesRecommended.objects.all()
    df=DPRfile.objects.all()

    u.delete()
    c.delete()
    s.delete()
    sh.delete()
    cr.delete()
    df.delete()
    print('all deleted')
