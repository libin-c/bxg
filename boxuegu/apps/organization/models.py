from datetime import  datetime

from django.db import models

# Create your models here.


class CityDict(models.Model):
    """城市字典"""
    name = models.CharField(max_length=20, verbose_name='城市')
    # 城市描述：备用不一定展示出来
    desc = models.TextField(verbose_name='城市描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    """课程学校"""
    name = models.CharField(max_length=50, verbose_name='学校名称')
    # 学校类别:
    category = models.CharField(max_length=20, choices=( ('pxjg', '培训学校'), ('gr', '个人'), ('gx', '高校') ), default='pxjg', verbose_name='学校类别' )
    # 学校描述，后面会替换为富文本展示
    desc = models.TextField(verbose_name='学校描述')
    tag = models.CharField(default=u'全国知名', max_length=10, verbose_name=u'学校标签')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(default='', upload_to='org/%Y/%m', verbose_name='封面图', max_length=100)
    address = models.CharField(max_length=150, verbose_name='学校地址')
    # 一个城市可以有很多课程学校，通过将city设置外键，变成课程学校的一个字段
    # 可以让我们通过学校找到城市
    city = models.ForeignKey(CityDict, verbose_name='所在城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    students = models.IntegerField(default=0, verbose_name='学习人数')

    class Meta:
        verbose_name = '课程学校'
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def course_nums(self):
        return self.course_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """讲师"""
    # 一个学校会有很多老师，所以我们在讲师表添加外键并把课程学校名称保存下来
    # 可以使我们通过讲师找到对应的学校
    org = models.ForeignKey(CourseOrg, verbose_name='所属学校')
    name = models.CharField(max_length=50, verbose_name='教师名字')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='公司职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    age = models.IntegerField(default=30, verbose_name='年龄')
    image = models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='头像', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def get_course_nums(self):
        return self.course_set.all().count()

    def __str__(self):
        return self.name
