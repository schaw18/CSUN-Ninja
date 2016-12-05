from django.core import serializers
from ninja.models import SectionSchedule, Course


def serialize_by_sections(section_query):

    # gets a queryset of sections and returns serialized info
    # including course and schedule

    result =[]
    for section_obj in section_query:
        section_dict = dict()

        schedules_info =  serializers.serialize('python', SectionSchedule.objects.filter(section=section_obj))
        schedule_fields = [d['fields'] for d in schedules_info]

        course_info = serializers.serialize('python', Course.objects.filter(section=section_obj))
        course_fields = [d['fields'] for d in course_info]

        for list_element in schedule_fields:
            for k,v in list_element.items():
                section_dict[k] = v

        for list_element in course_fields:
            for k,v in list_element.items():
                section_dict[k] = v

        section_dict['class_number'] = section_obj.class_number
        section_dict['current_enrollment'] = section_obj.section_current_enrollment
        section_dict['max_enrollment'] = section_obj.section_max_enrollment

        result.append(section_dict)

    return result
