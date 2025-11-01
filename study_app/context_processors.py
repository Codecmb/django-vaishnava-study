from .models import Course

def courses_processor(request):
    courses = Course.objects.all().order_by('order')
    return {'all_courses': courses}
