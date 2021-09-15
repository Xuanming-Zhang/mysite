import xadmin

from apps.courses.models import Course


class CourseAdmin:
    pass


xadmin.site.register(Course, CourseAdmin)
