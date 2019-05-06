from django.db import models
from datetime import datetime

from DjangoUeditor.models import UEditorField
from users.models import UserInfo


class InfoCategories(models.Model):
    """
    信息版块分类
    """
    
    CLASSIFICATION = (
        (1, "一级类别"),
        (2, "二级类别"),
        (3, "三级类别"),
        (4, "四级类别"),
        (5, "五级类别"),
    )
    
    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", help_text="类别描述", verbose_name="类别描述")
    category_type = models.IntegerField(choices=CLASSIFICATION, verbose_name="类目级别", help_text="类目级别", default=1)
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_classification", on_delete=models.CASCADE)
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")
    
    class Meta:
        verbose_name = "平台信息分类"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class WeMediaArticles(models.Model):
    """
    平台自媒体文章
    """
    title = models.CharField(max_length=200, verbose_name="标题", help_text="标题")
    subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name="副标题", help_text="副标题")
    info_categories = models.ForeignKey(InfoCategories, on_delete=models.CASCADE, verbose_name="信息版块分类",
                                        help_text="信息版块分类")
    abstract = models.TextField(max_length=200, blank=True, null=True, verbose_name="摘要", help_text="摘要")
    content = UEditorField(default="", width=1000, height=300, filePath="platform_op/files/",
                           imagePath="platform_op/images/", verbose_name="正文", help_text="正文")
    attachment = models.FileField(upload_to="we_media_articles/", blank=True, null=True, verbose_name="附件", help_text="附件")
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间", help_text="发布时间")
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="作者", help_text="作者")
    #用于相关计数的字段
    read_nums = models.IntegerField(default=0, editable=True, verbose_name="阅读计数", help_text="阅读计数")
    fav_nums = models.IntegerField(default=0, editable=True, verbose_name="被收藏计数", help_text="被收藏计数")
    
    class Meta:
        verbose_name = "平台自媒体文章"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.title

# class WeMediaContentImg(models.Model):
#     """
#     平台自媒体文章正文
#     """


class WeMediaArticleFav(models.Model):
    """
    平台自媒体文章收藏记录
    """
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="user_wemedia_fav",
                                  verbose_name="收藏的用户", help_text="收藏的用户")
    wemedia_article = models.ForeignKey(WeMediaArticles, on_delete=models.CASCADE, related_name="wemedia_fav",
                                        verbose_name="收藏的平台自媒体文章", help_text="收藏的平台自媒体文章")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间", help_text="收藏时间")
    
    class Meta:
        verbose_name = "平台自媒体文章收藏管理"
        verbose_name_plural = verbose_name
        unique_together = "user_info", "wemedia_article"
    
    def __str__(self):
        return "{}收藏的{}".format(self.user_info.username, self.wemedia_article.title)


class PlatformActivity(models.Model):
    """
    平台活动
    """
    activity_title = models.CharField(max_length=200, verbose_name="活动名称", help_text="活动名称")
    activity_posters = models.ImageField(upload_to="platform_activity/", blank=True, null=True, verbose_name="封面图片", help_text="封面图片")
    activity_organizer = models.CharField(max_length=200, blank=True, null=True, verbose_name="活动发布人", help_text="活动发布人")
    activity_start_time = models.DateTimeField(default=datetime.now, editable=True, verbose_name="活动开始时间", help_text="活动开始时间")
    activity_end_time = models.DateTimeField(default=datetime.now, editable=True, verbose_name="活动结束时间", help_text="活动结束时间")
    activity_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="活动地址", help_text="活动地址")
    activity_desc = UEditorField(default="", width=1000, height=300, filePath="platform_act/files/",
                                 imagePath="platform_act/images/", verbose_name="活动详情", help_text="活动详情")
    activity_tickets = models.IntegerField(default=0, editable=True, verbose_name="门票价格", help_text="门票价格")
    meals_flag = models.BooleanField(default=False, editable=True, verbose_name="是否供餐", help_text="是否供餐")
    accommodation_flag = models.BooleanField(default=False, editable=True, verbose_name="是否提供住宿", help_text="是否提供住宿")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")
    
    class Meta:
        verbose_name = "平台活动"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.activity_title


class ActivityRegList(models.Model):
    """
    参加活动名单
    """
    SEX_CHOICE = (
        ("男", "男"),
        ("女", "女")
    )
    
    NATIONAL_CHOICE = (
        ('1', '汉族'),
        ('2', '蒙古族'),
        ('3', '回族'),
        ('4', '藏族'),
        ('5', '维吾尔族'),
        ('6', '苗族'),
        ('7', '彝族'),
        ('8', '壮族'),
        ('9', '布依族'),
        ('10', '朝鲜族'),
        ('11', '满族'),
        ('12', '侗族'),
        ('13', '瑶族'),
        ('14', '白族'),
        ('15', '土家族'),
        ('16', '哈尼族'),
        ('17', '哈萨克族'),
        ('18', '傣族'),
        ('19', '黎族'),
        ('20', '傈僳族'),
        ('21', '佤族'),
        ('22', '畲族'),
        ('23', '高山族'),
        ('24', '拉祜族'),
        ('25', '水族'),
        ('26', '东乡族'),
        ('27', '纳西族'),
        ('28', '景颇族'),
        ('29', '柯尔克孜族'),
        ('30', '土族'),
        ('31', '达斡尔族'),
        ('32', '仫佬族'),
        ('33', '羌族'),
        ('34', '布朗族'),
        ('35', '撒拉族'),
        ('36', '毛难族'),
        ('37', '仡佬族'),
        ('38', '锡伯族'),
        ('39', '阿昌族'),
        ('40', '普米族'),
        ('41', '塔吉克族'),
        ('42', '怒族'),
        ('43', '乌孜别克族'),
        ('44', '俄罗斯族'),
        ('45', '鄂温克族'),
        ('46', '崩龙族'),
        ('47', '保安族'),
        ('48', '裕固族'),
        ('49', '京族'),
        ('50', '塔塔尔族'),
        ('51', '独龙族'),
        ('52', '鄂伦春族'),
        ('53', '赫哲族'),
        ('54', '门巴族'),
        ('55', '珞巴族'),
        ('56', '基诺族'),
        ('57', '其他未标明民族'),
        ('58', '入籍外国人')
    
    )
    
    name = models.CharField(max_length=50, verbose_name="姓名", help_text="姓名")
    sex = models.CharField(max_length=10, choices=SEX_CHOICE, verbose_name="性别", help_text="性别")
    national = models.IntegerField(choices=NATIONAL_CHOICE, verbose_name="民族", help_text="民族")
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="联系方式", help_text="联系方式")
    
    class Meta:
        verbose_name = "参加活动名单"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class ActivityRegistration(models.Model):
    """
    活动报名
    """
    reg_account = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="reg_account", verbose_name="报名帐号", help_text="报名帐号")
    reg_company = models.CharField(max_length=200, blank=True, null=True, verbose_name="报名的公司", help_text="报名的公司")
    reg_number = models.IntegerField(default=0, editable=False, verbose_name="报名人数", help_text="报名人数")
    meals_number = models.IntegerField(default=0, editable=True, verbose_name="用餐人数", help_text="用餐人数")
    accommodation_number = models.IntegerField(default=0, editable=True, verbose_name="住宿人数", help_text="住宿人数")
    # 多对多字段，不会在后台显示，也不可在后台维护
    reg_list = models.ManyToManyField(ActivityRegList, related_name="reg_list", verbose_name="活动名单", help_text="活动名单")
    
    class Meta:
        verbose_name = "活动报名"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.reg_company