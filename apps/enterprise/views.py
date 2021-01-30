from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from pyecharts.charts import Bar, Pie, Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType

from .models import Jobs



# Create your views here.
def edu_analysis(request):
    result = Jobs.objects.values('education').annotate(count=Count('education'))

    data = []
    for row in result:
        data.append((row['education'], row['count']))

    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))
        .add("", data)
        .set_global_opts(title_opts=opts.TitleOpts(title="学历分布"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    )
    return HttpResponse(c.render_embed())

def area_analysis(request):
    result = Jobs.objects.values('work_area').annotate(count=Count('work_area'))

    xaxis, yaxis = [], []
    for row in result:
        area = row['work_area']
        xaxis.append(area)
        yaxis.append(row['count'])

    c = (
        Line()
            .add_xaxis(xaxis)
            .add_yaxis("", yaxis, is_smooth=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="区域分布"))
    )
    return HttpResponse(c.render_embed())


def salary_analysis(request):
    result = Jobs.objects.values('min_salary').annotate(count=Count('min_salary'))

    xaxis, yaxis = [], []
    for row in result:
        xaxis.append('{:g}K'.format(row['min_salary']))
        yaxis.append(row['count'])

    c = (
        Bar({"theme": ThemeType.MACARONS})
            .add_xaxis(xaxis)
            .add_yaxis("", yaxis)
            .set_global_opts(
            title_opts={"text": "薪资待遇", "subtext": "取最低薪资计算"}
        )    )
    return HttpResponse(c.render_embed())