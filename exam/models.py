from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save



# Create your models here.
class College(models.Model):
    clg_name = models.CharField(max_length=300)

    def __str__(self):
        return self.clg_name

class Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.DO_NOTHING, related_name='exam')

    def __str__(self):
        return self.exam_name


class Question(models.Model):
    CATEGORY = (
        ('Aptitude', 'Aptitude'),
        ('Programming', 'Programming')
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam')
    question_text = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY, default="None")
    answer = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return self.question_text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    option_value1 = models.CharField(max_length=1, default="A")
    option_text1 = models.CharField(max_length = 300)
    option_value2 = models.CharField(max_length=1,default="B")
    option_text2 = models.CharField(max_length = 300)
    option_value3 = models.CharField(max_length=1,default="C")
    option_text3 = models.CharField(max_length = 300)
    option_value4 = models.CharField(max_length=1,default="D")
    option_text4 = models.CharField(max_length = 300)

    def __str__(self):
        return self.question.question_text + " : " + self.option_text1 + ":" + self.option_text2 + ":" + self.option_text3 + ":" + self.option_text4



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.DO_NOTHING, related_name='college')
    roll_no = models.CharField(max_length=15)




def student_profile(sender, created, instance, **kwargs):
    if created:
        if instance.is_superuser == True:
            group = Group.objects.get(name='admin')
            instance.groups.add(group)
            print("True Again")

        else:
            group = Group.objects.get(name='student')
            instance.groups.add(group)
            Student.objects.create(
                user = instance, 
                college = instance.college,
                roll_no = instance.roll_no
            )   
post_save.connect(student_profile, sender=User)



class Record(models.Model):
    student_id = models.CharField(max_length=10)
    exam_id = models.CharField(max_length=10)
    question_id = models.CharField(max_length=10)
    answer = models.CharField(max_length=1, default='N')