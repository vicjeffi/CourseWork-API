///data models

1 - admins =>
login:password

2 - groups = >
group_key:full_name([course] & [number]):specialization:course:number:isLearning(is still learning in collage)

3 - students =>
num_key:groups.group_key:last-name:first-name:father-name:isLearning(is still learning in collage)

/add-student?adm-username=admin&adm-password=123459BVA&student-name=Григорий&student-lastname=Гуськов&student-fathername=Олегович

4 - teachers =>
num_key:password:last-name:first-name:father-name:bool(is still learning in collage):{array of groups.num_key witch learning by this teacher}

//end data models

//start line

flask run --host=0.0.0.0