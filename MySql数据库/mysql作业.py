class  <-> student  关联:class_id
teacher <-> course  关联:teacher_id
score <-> student 关联 student_id 
score <-> course  关联 course_id 


# 1、查询所有的课程的名称以及对应的任课老师姓名
# where
select 
	course.cname,teacher.tname
from 
	teacher,course
where 
	teacher.tid = course.teacher_id
	
# inner join
select 
	course.cname,teacher.tname
from 
	teacher inner join course on teacher.tid = course.teacher_id

# 2、查询学生表中男女生各有多少人
select 
	gender,count(*)
from 
	student
group by
	gender


# 3、查询物理成绩等于100的学生的姓名
# where
select 
	student.sname , score.num
from 
	score,student,course
where
	score.student_id = student.sid 
	and
	score.course_id = course.cid
	and
	course.cname = "物理"
	and
	score.num = 100
	
# inner join 
select 
	student.sname , score.num
from 
	score inner join student on  score.student_id = student.sid 
	inner join course on score.course_id = course.cid
where
	course.cname = "物理"
	and
	score.num = 100
	
	
	
# 4、查询平均成绩大于八十分的同学的姓名和平均成绩
# where 写法
select
	student_id,student.sname,avg(num)
from
	score,student
where 
	score.student_id = student.sid
group by
	student_id
having
	avg(num) > 80

# inner join
select
	student_id,student.sname,avg(num)
from
	score inner join student on score.student_id = student.sid
group by
	student_id
having
	avg(num) > 80


# 5、查询所有学生的学号，姓名，选课数，总成绩
# 选课数
select
	student_id,count(*)
from 
	score
group by 
	student_id
	
# 总成绩
select 
	student_id,sum(num)
from 
	score
group by
	student_id

# where
select 
	student_id,sname,count(*),sum(num)
from 
	score,student
where
	score.student_id = student.sid
group by
	student_id

# inner join 
select 
	student_id,sname,count(*),sum(num)
from 
	score inner join student on score.student_id = student.sid
group by
	student_id

# ( 附加所有学生 )
# right join 
select 
	student.sid,sname,count(score.course_id),sum(num)
from 
	score right join student on score.student_id = student.sid
group by
	student.sid

# left join 
select 
	student.sid,sname,count(score.course_id),sum(num)
from 
	student left join score  on score.student_id = student.sid
group by
	student.sid

# 6、 查询姓李老师的个数
select
	count(*)
from 
	teacher
where 
	tname like '李%'

# 7、 查询没有报李平老师课的学生姓名
# 1.报了李平老师课程的学生id是?
"""distinct 去重  
distinct student_id    ok
distinct(student_id)   ok
"""
select 
	distinct( student_id )
from 
	teacher,course,score
where
	teacher.tid = course.teacher_id
	and
	course.cid = score.course_id
	and 
	teacher.tname = "李平"

# 2.查询学生表,除了这个id的剩下的就是没有报李平老师课程的
select 
	student.sname
from 
	student
where 
	sid not in (1号数据)

#3.综合拼接
select
	student.sname
from 
	student
where 
	sid not in (select 
	distinct( student_id )
from 
	teacher,course,score
where
	teacher.tid = course.teacher_id
	and
	course.cid = score.course_id
	and 
	teacher.tname = "李平")


# 8、 查询物理课程的分数比生物课程的分数高的学生的学号

# 1.物理课程学生分数
select 
	score.student_id as t1_id , score.num as num , course.cid ,course.cname
from 
	course inner join score on course.cid = score.course_id
where
	course.cname = "物理"
	
# 2.生物课程学生分数
select 
	score.student_id as t2_id , score.num as num , course.cid ,course.cname
from 
	course inner join score on course.cid = score.course_id
where
	course.cname = "生物"
	
	
# 综合拼接
"""
# 格式
select 
	t1.t1_id
from 
	(1) inner join (2) on 1.student_id = 2.student_id
where
	1.num > 2.num
"""
select 
	t1.t1_id
from 
	(select 
	score.student_id as t1_id , score.num as num , course.cid ,course.cname
from 
	course inner join score on course.cid = score.course_id
where
	course.cname = "物理") as t1 inner join (select 
	score.student_id as t2_id , score.num as num , course.cid ,course.cname
from 
	course inner join score on course.cid = score.course_id
where
	course.cname = "生物") as t2 on t1.t1_id = t2.t2_id
where
	t1.num > t2.num
	
	

# 9、 查询没有同时选修物理课程和体育课程的学生姓名
# 1.找物理和体育的课程id
select 
	cid
from 
	course
where
	cname = "物理" or cname = "体育"
	
# 2.找学习体育物理课程的学生id 
select 
	student_id
from 
	score
where 
	course_id in (2,3)

# 拼装数据
select 
	student_id
from 
	score
where 
	course_id in (select 
	cid
from 
	course
where
	cname = "物理" or cname = "体育")

# 3.(同时)学习体育物理课程的学生id
select 
	student_id
from 
	score
where 
	course_id in (select 
	cid
from 
	course
where
	cname = "物理" or cname = "体育")

group by
	score.student_id
having 
	count(*) = 2

# 4.除了通过学习物理和体育的学生之外,剩下的都是没有同时学习的学生id
select	 
	sid,sname
from 
	student
where 
	sid not in (3号)
	
# 综合拼装:
select	 
	sid,sname
from 
	student
where 
	sid not in (select 
	student_id
from 
	score
where 
	course_id in (select 
	cid
from 
	course
where
	cname = "物理" or cname = "体育")

group by
	score.student_id
having 
	count(*) = 2)


	
# 10、查询挂科超过两门(包括两门)的学生姓名和班级
"""挂科<60"""
select
	student_id,student.sname,class.caption
from 
	score inner join student on score.student_id = student.sid
	inner join class on class.cid = student.class_id
where 
	num < 60
group by
	student_id
having 
	count(*) >= 2


# 11、查询选修了所有课程的学生姓名
# 1.统计所有课程总数
select count(*) from course

# 2.按照学生分类,总数量是1号查询出来的数据,等价于学了所有课程
select 
	student.sid, student.sname
from
	score inner join student on  score.student_id = student.sid
group by 
	score.student_id
having 
	count(*) = (1号)
	
# 综合拼接
select 
	student.sid, student.sname
from
	score inner join student on  score.student_id = student.sid
group by 
	score.student_id
having 
	count(*) = (select count(*) from course)



# 12、查询李平老师教的课程的所有成绩记录
# 内联
select
	score.student_id , course.cname , score.num
from 
	teacher , course , score
where
	teacher.tid = course.teacher_id
	and
	score.course_id = course.cid
	and 
	teacher.tname = "李平"

# 子查询
# 1.找李平老师的课程id
select 
	course.cid
from 
	teacher,course
where
	teacher.tid = course.teacher_id
	and
	teacher.tname = "李平"
# 2.通过课程id号 找score里面的数据
select *
from 
	score
where 
	course_id in (1号)

# 综合拼接
select 
	score.student_id ,score.num
from 
	score
where 
	course_id in (select 
	course.cid
from 
	teacher,course
where
	teacher.tid = course.teacher_id
	and
	teacher.tname = "李平")



# 13、查询全部学生都选修了的课程号和课程名
# 1.通过score表,找有成绩的学生个数
select
	count(distinct student_id)
from
	score

# 2.按照课程分类,筛选学生个数等于13的课程id
select
	course_id
from 
	score
group by
	course_id
having 
	count(*) = 13
	
# 综合拼接
select
	course_id,course.cname
from 
	score,course
where
	score.course_id = course.cid
group by
	course_id
having 
	count(*) = (select
	count(distinct student_id)
from
	score)


# 14、查询每门课程被选修的次数;
select 
	course_id,count(*)
from 
	score
group by 
	course_id

# 15、查询只选修了一门课程的学生学号和姓名
# 1.按照学生分类,统计课程个数为1
select 
	student_id
from 
	score
group by 
	student_id
having
	count(*) = 1

# 2.顺手连带一个学生表student , 通过id拿姓名

select 
	student_id,student.sname
from 
	score inner join student on score.student_id = student.sid
group by 
	student_id
having
	count(*) = 1
	
	
	
# 16、查询所有学生考出的成绩并按从高到低排序（成绩去重）
select 
	distinct num,group_concat(student_id)
from
	score
group by
	num
order by
	num desc

#  其他同学想法
select 
	avg(num),sum(num)
from 
	score
group by
	student_id
order by 
	avg(num) desc 
	

# 17、查询平均成绩大于85的学生姓名和平均成绩
# 子查询

# 1.找学生id
select 
	student_id
from 
	score
group by
	student_id
having 
	avg(num) > 85
	
# 2.找学生表对应数据
select sname 
from 
	student
where 	
	id = (1号)

# 综合拼接
select 
	sid,sname 
from 
	student
where 	
	sid = (select 
	student_id
from 
	score
group by
	student_id
having 
	avg(num) > 85)


18、查询生物成绩不及格的学生姓名和对应生物分数
select 
	student.sname,score.num,course.cname
from 
	course inner join score on course.cid = score.course_id
	inner join student on student.sid = score.student_id
where
	score.num < 60
	and
	course.cname = "生物"


19、查询在所有选修了李平老师课程的学生中，这些课程(李平老师的课程，不是所有课程)平均成绩最高的学生姓名
# 1.找李平老师教的课程id
select 
	course.cid
from 
	teacher , course
where 
	teacher.tid = course.teacher_id
	and
	teacher.tname = "李平" 
# 2 4

# 2.学习李平老师课程的学生中,按照学生分类,找平均分最高的id
select
	score.student_id , avg(num)
from 
	score
where
	score.course_id in (2,4)
group by
	score.student_id
order by 
	avg(num) desc limit 1

# 3.通过学生id 顺带着连一张student学生表,找出姓名
select
	score.student_id , student.sname  , avg(num) 
from 
	score,student
where
	score.student_id = student.sid
	and
	score.course_id in (1号)
group by
	score.student_id
order by 
	avg(num) desc limit 1
	
	
# 4综合拼接
select
	score.student_id , student.sname  , avg(num) 
from 
	score,student
where
	score.student_id = student.sid
	and
	score.course_id in (select 
	course.cid
from 
	teacher , course
where 
	teacher.tid = course.teacher_id
	and
	teacher.tname = "李平" )
group by
	score.student_id
order by 
	avg(num) desc limit 1
	
	
	
20、查询每门课程成绩最好的课程id、学生姓名和分数
# 1.找分数最大值.
select 
	course_id,max(num) as max_num
from 
	score
group by
	score.course_id

# 2.找出该分数对应的那批学生

select 
	*
from 
	score as t1 inner join student as t2 on t1.student_id  = t2.sid
	inner join (1号) as t3 on  t1.course_id = t3.course_id
	

# 综合拼接
select 
	t1.course_id , t2.sname , t3.max_num
from 
	score as t1 inner join student as t2 on t1.student_id  = t2.sid
	inner join (select 
	course_id,max(num) as max_num
from 
	score
group by
	score.course_id) as t3 on  t1.course_id = t3.course_id

where
	t1.num = t3.max_num


# 21、查询不同课程但成绩相同的课程号、学生号、成绩 
"""不同的课程 如果使用!= 相同的数据返回来又查询了一遍,翻倍,为了防止翻倍重复查询使用>或者< """
select 
	s1.student_id as s1_sid,
	s2.student_id as s2_sid,
	s1.course_id as s1_cid,
	s2.course_id as s2_cid,
	s1.num as s1_num,
	s2.num as s2_num
from 
	score as s1,
	score as s2
where 	
	s1.course_id > s2.course_id
	and
	s1.num = s2.num

# 22、查询没学过“李平”老师课程的学生姓名以及选修的课程名称 

# 23、查询所有选修了学号为2的同学选修过的一门或者多门课程的同学学号和姓名 
# 1.学号为2的学生,选了什么学科
select 
	course_id
from 
	score
where
	student_id = 2  # 1 3 4
	
# 2.学过1 3 4 学科的学生都有谁
select 
	distinct student_id,student.sname
from
	score inner join student  on score.student_id= student.sid
where 
	course_id in (1,3,4)
	
# 综合拼接
select 
	distinct student_id,student.sname
from
	score inner join student  on score.student_id= student.sid
where 
	course_id in (select 
	course_id
from 
	score
where
	student_id = 2)
	

# 24、任课最多的老师中学生单科成绩最高的课程id、学生姓名和分数

# 1.老师任何的最大数量是多少
"""任课数量为2的老师可能不止一个"""
select 
	count(*)
from	
	course
group by
	teacher_id
order by 
	count(*) desc limit 1
	
# 2.找最大任课数量为2的老师id
select 
	teacher_id
from 
	course
group by
	teacher_id
having 
	count(*) = (1号)
	
# 综合拼接
select 
	teacher_id
from 
	course
group by
	teacher_id
having 
	count(*) = (select 
	count(*)
from	
	course
group by
	teacher_id
order by 
	count(*) desc limit 1)


# 3.通过老师id 找课程
select 
	cid
from 
	course
where
	teacher_id in (2号)


# 综合拼接
# 2 4 
select 
	cid
from 
	course
where
	teacher_id in (select 
	teacher_id
from 
	course
group by
	teacher_id
having 
	count(*) = (select 
	count(*)
from	
	course
group by
	teacher_id
order by 
	count(*) desc limit 1))

# 4.通过该课程号,找其中的最大值(最大分数)
select 
	course_id,
	max(num) as max_num
from 
	score
where
	course_id in (3号)
group by
	course_id
	
# 综合拼接
select
	course_id,
	max(num) as max_num
from 
	score
where
	course_id in (select 
	cid
from 
	course
where
	teacher_id in (select 
	teacher_id
from 
	course
group by
	teacher_id
having 
	count(*) = (select 
	count(*)
from	
	course
group by
	teacher_id
order by 
	count(*) desc limit 1)))
group by
	course_id


# 5.把对应的学生姓名,最大分数拼在一起,做一次单表查询

select 
	*
from 
	score as t1 inner join student as t2 on  t1.student_id = t2.sid
	inner join (4号) as t3 on t3.course_id = t1.course_id

# 综合拼接
select 
	*
from 
	score as t1 inner join student as t2 on  t1.student_id = t2.sid
	inner join (select
	course_id,
	max(num) as max_num
from 
	score
where
	course_id in (select 
	cid
from 
	course
where
	teacher_id in (select 
	teacher_id
from 
	course
group by
	teacher_id
having 
	count(*) = (select 
	count(*)
from	
	course
group by
	teacher_id
order by 
	count(*) desc limit 1)))
group by
	course_id) as t3 on t3.course_id = t1.course_id


# 6.把分数是100分的最大值的学员查出来
select 
	*
from 
	score as t1 inner join student as t2 on  t1.student_id = t2.sid
	inner join (4号) as t3 on t3.course_id = t1.course_id
where
	t1.num = t3.max_num
	

# 综合拼接
select 
	t1.course_id,t2.sname,t3.max_num
from 
	score as t1 inner join student as t2 on  t1.student_id = t2.sid
	inner join (select
	course_id,
	max(num) as max_num
from 
	score
where
	course_id in (select 
	cid
from 
	course
where
	teacher_id in (select 
	teacher_id
from 
	course
group by
	teacher_id
having 
	count(*) = (select 
	count(*)
from	
	course
group by
	teacher_id
order by 
	count(*) desc limit 1)))
group by
	course_id) as t3 on t3.course_id = t1.course_id
where
	t1.num = t3.max_num
	
	
	